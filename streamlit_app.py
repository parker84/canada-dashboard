import streamlit as st
import os
import pandas as pd
from plotly import express as px
from pathlib import Path
from constants import COUNTRY_CODES_W_FLAGS
import coloredlogs, logging
from tqdm import tqdm
from decouple import config
logger = logging.getLogger(__name__)
coloredlogs.install(level=config('LOG_LEVEL', 'INFO'))

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Canada Dashboard',
    page_icon='🍁',
    layout='wide',
    initial_sidebar_state='collapsed'
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

def get_and_combine_data_from_folder(folder):
    logger.info(f'Getting data from {folder} 📂...')
    dfs = []
    for file in os.listdir(f'./data/{folder}'):
        if file.endswith('.csv'):
            df = pd.read_csv(f'./data/{folder}/{file}')
            dfs.append(df)
    combined_df = pd.concat(dfs)
    logger.info(f'Finished getting data from {folder} ✅')
    return combined_df 

@st.cache_data
def get_gdp_data():
    raw_gdp_df = get_and_combine_data_from_folder('gdp')
    gdp_df = raw_gdp_df.rename(columns={
        'countryiso3code': 'Country',
        'date': 'Year',
        'value': 'GDP'
    }).dropna(subset=['GDP'])
    gdp_df['Country'] = gdp_df['Country'].replace(COUNTRY_CODES_W_FLAGS)
    gdp_df['Year'] = pd.to_numeric(gdp_df['Year'])
    gdp_df['GDP (T)'] = round(gdp_df['GDP'] / 1e12, 1)
    gdp_df['GDP'] = (gdp_df['GDP'] / 1e9).round(0) * 1e9
    return gdp_df.sort_values(by='Year', ascending=False)    

@st.cache_data
def get_population_data():
    raw_population_df = get_and_combine_data_from_folder('population')
    population_df = raw_population_df.rename(columns={
        'countryiso3code': 'Country',
        'date': 'Year',
        'value': 'Population'
    }).dropna(subset=['Population'])
    population_df['Country'] = population_df['Country'].replace(COUNTRY_CODES_W_FLAGS)
    population_df['Year'] = pd.to_numeric(population_df['Year'])
    population_df['Population (M)'] = round(population_df['Population'] / 1e6, 1)
    population_df['Population'] = (population_df['Population'] / 1e6).round(0) * 1e6
    return population_df.sort_values(by='Year', ascending=False)

@st.cache_data()
def get_countries(df):
    countries = list(COUNTRY_CODES_W_FLAGS.values())
    countries += [
        val for val in df['Country'].tolist()
        if val not in countries
    ]
    return countries

def plot_metric_by_group(
        metric_df, 
        var_to_group_by_col, 
        metric_col,
        bar_chart=True,
        hover_data=None,
        text_col=None
    ):
    col1, col2 = st.columns(2)
    bar_metric_df = metric_df[metric_df[metric_col].isnull() == False]
    max_year = bar_metric_df['Year'].max()
    bar_metric_df = bar_metric_df[
        bar_metric_df['Year'] == max_year
    ]
    bar_metric_df = bar_metric_df.sort_values(by=metric_col, ascending=False)
    category_order = ['CAN 🇨🇦'] + [ # put Canada first
        val for val in
        bar_metric_df[var_to_group_by_col].tolist()
        if val != 'CAN 🇨🇦'
    ]
    category_orders={
        var_to_group_by_col: category_order
    }
    with col1:
        p = px.line(
                metric_df,
                x='Year',
                y=metric_col,
                color=var_to_group_by_col,
                title=f'Yearly {metric_col} by {var_to_group_by_col}',
                hover_data=hover_data,
                category_orders=category_orders,

            )
        st.plotly_chart(p, use_container_width=True)
    with col2:
        if bar_chart:
            p = px.bar(
                    bar_metric_df,
                    y=var_to_group_by_col,
                    x=metric_col,
                    orientation='h',
                    title=f'{metric_col} by {var_to_group_by_col} (Year = {int(max_year)})',
                    hover_data=hover_data,
                    category_orders=category_orders,
                    text=text_col
                )
        else:
            p = px.pie(
                bar_metric_df,
                names=var_to_group_by_col,
                values=metric_col,
                title=f'{metric_col} by {var_to_group_by_col} (Year = {int(max_year)})',
                hole=0.4,
                category_orders=category_orders,
                hover_data=hover_data
            )
        st.plotly_chart(p, use_container_width=True)
        return category_orders

def show_metric(
        df, 
        y_col, 
        format_str='{:,}M', 
        delta_color='normal', 
        title=None, 
        help=None, 
        calc_per_change=True
    ):
        if title is None:
            title = y_col
        if calc_per_change:
            try:
                percentage_change = (
                    100 * ((df[y_col].iloc[0] / df[y_col].iloc[1]) - 1)
                )
                delta='{change}% (YoY)'.format(
                    change=round(percentage_change, 2)
                )
            except Exception as err:
                print('❌' + str(err))
                delta = None
        else: 
            delta = None
        st.metric(
            title,
            value=format_str.format(df[y_col].iloc[0]),
            delta=delta,
            delta_color=delta_color,
            help=help
        )

# -----------------------------------------------------------------------------
# Load the data.
gdp_df = get_gdp_data()
population_df = get_population_data()

# -----------------------------------------------------------------------------
# Setup the dashboard.
        
st.title('Canada 🍁 Dashboard')

st.caption('This dashboard compares key economic indicators for Canada against other global superpowers.')


# -----------------------------------------------------------------------------
# Filters.
min_value = gdp_df['Year'].min()
max_value = gdp_df['Year'].max()


from_year, to_year = st.sidebar.slider(
    'Which years are you interested in?',
    min_value=min_value,
    max_value=max_value,
    value=[min_value, max_value]
)
st.sidebar.caption("Want to say thanks? \n[Buy me a coffee ☕](https://www.buymeacoffee.com/brydon)")

gdp_df_max_year = gdp_df[gdp_df['Year'] == to_year].sort_values(by='GDP', ascending=False)
countries = get_countries(gdp_df_max_year)

if not len(countries):
    st.warning("Select at least one country")

col1, col2 = st.columns(2)

with col1:
    metric = st.selectbox(
        'Metric',
        ['GDP 💰', 'Population 👥'], # TODO: add more metrics
    )

with col2:
    selected_countries = st.multiselect(
        'Select Countries',
        countries,
        default=['CAN 🇨🇦', 'USA 🇺🇸']
    )

# -----------------------------------------------------------------------------
# Show the data.

if metric == 'GDP 💰':
    # Filter the data
    filtered_gdp_df = gdp_df[
        (gdp_df['Country'].isin(selected_countries))
        & (gdp_df['Year'] <= to_year)
        & (from_year <= gdp_df['Year'])
    ]
    max_year_filtered_df = filtered_gdp_df[filtered_gdp_df['Year'] == to_year].sort_values(by='GDP', ascending=False)

    st.header('Annual GDP by Country', divider='gray')

    ''

    cols = st.columns(len(selected_countries))
    i = 0
    countries = ['CAN 🇨🇦'] + [
        val for val in
        max_year_filtered_df['Country']
        if val != 'CAN 🇨🇦'
    ]
    for country in countries:
        with cols[i]:
            show_metric(
                filtered_gdp_df[filtered_gdp_df['Country'] == country],
                'GDP (T)',
                title=country,
                format_str='${:,.1f}T',
                delta_color='normal',
            )
        i += 1

    plot_metric_by_group(
        filtered_gdp_df,
        'Country',
        bar_chart=True,
        metric_col='GDP',
        text_col='GDP (T)'
    )

elif metric == 'Population 👥': # TODO: consider refactoring to use a function
    # Filter the data
    filtered_population_df = population_df[
        (population_df['Country'].isin(selected_countries))
        & (population_df['Year'] <= to_year)
        & (from_year <= population_df['Year'])
    ]
    max_year_filtered_df = filtered_population_df[filtered_population_df['Year'] == to_year].sort_values(by='Population', ascending=False)

    st.header('Annual Population by Country', divider='gray')

    ''

    cols = st.columns(len(selected_countries))
    i = 0
    for country in max_year_filtered_df['Country']:
        with cols[i]:
            show_metric(
                filtered_population_df[filtered_population_df['Country'] == country],
                'Population (M)',
                title=country,
                format_str='{:,.1f}M',
                delta_color='normal',
            )
        i += 1

    plot_metric_by_group(
        filtered_population_df,
        'Country',
        bar_chart=True,
        metric_col='Population',
        text_col='Population (M)' # TODO: add units to the text col
    )

st.caption('Data from the [World Bank Open Data](https://data.worldbank.org/) API.')