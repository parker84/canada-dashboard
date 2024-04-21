import streamlit as st
import os
import pandas as pd
from plotly import express as px
from constants import COUNTRY_CODES_W_FLAGS
import coloredlogs, logging
from decouple import config
from scrape import scrape_core_metrics_for_core_countries
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

def check_if_data_exists(folder):
    logger.info(f'Checking if data exists in {folder}...')
    if not os.path.exists(f'./data/{folder}'):
        logger.warning('No data found. Scrape the data first.')
        return False
    else:
        logger.info('Data found! ✅')
        return True

def get_and_combine_data_from_folder(folder):
    data_exists = check_if_data_exists(folder)
    if not data_exists:
        logger.info('Scraping the data...')
        scrape_core_metrics_for_core_countries()
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
    gdp_df['GDP (T-int)'] = round(gdp_df['GDP'] / 1e12, 1)
    gdp_df['GDP (T)'] = [
        f'${val:,.1f}T' for val in
        gdp_df['GDP (T-int)']
    ]
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
    population_df['Population (M-int)'] = round(population_df['Population'] / 1e6, 1)
    population_df['Population (M)'] = [
        f'{val:,.1f}M' for val in
        population_df['Population (M-int)']
    ]
    population_df['Population'] = (population_df['Population'] / 1e6).round(0) * 1e6
    return population_df.sort_values(by='Year', ascending=False)

@st.cache_data
def get_gdp_per_capita():
    raw_gdp_per_capita_df = get_and_combine_data_from_folder('gdp_per_capita')
    gdp_per_capita_df = raw_gdp_per_capita_df.rename(columns={
        'countryiso3code': 'Country',
        'date': 'Year',
        'value': 'GDP per Capita'
    }).dropna(subset=['GDP per Capita'])
    gdp_per_capita_df['Country'] = gdp_per_capita_df['Country'].replace(COUNTRY_CODES_W_FLAGS)
    gdp_per_capita_df['Year'] = pd.to_numeric(gdp_per_capita_df['Year'])
    gdp_per_capita_df['GDP per Capita (k-int)'] = round(gdp_per_capita_df['GDP per Capita'] / 1e3, 1)
    gdp_per_capita_df['GDP per Capita (k)'] = [
        f'${val:,.0f}k' for val in
        gdp_per_capita_df['GDP per Capita (k-int)']
    ]
    gdp_per_capita_df['GDP per Capita'] = (gdp_per_capita_df['GDP per Capita'] / 1e3).round(0) * 1e3
    return gdp_per_capita_df.sort_values(by='Year', ascending=False)

@st.cache_data()
def get_government_debt():
    raw_government_debt_df = get_and_combine_data_from_folder('government_debt')
    government_debt_df = raw_government_debt_df.rename(columns={
        'countryiso3code': 'Country',
        'date': 'Year',
        'value': 'Government Debt vs GDP'
    }).dropna(subset=['Government Debt vs GDP'])
    government_debt_df['Country'] = government_debt_df['Country'].replace(COUNTRY_CODES_W_FLAGS)
    government_debt_df['Year'] = pd.to_numeric(government_debt_df['Year'])
    government_debt_df['Government Debt vs GDP (%)'] = government_debt_df['Government Debt vs GDP'].round(0)
    government_debt_df['Government Debt vs GDP (%-str)'] = [
        f'{int(val)}%' for val in
        government_debt_df['Government Debt vs GDP (%)']
    ]
    government_debt_df['Government Debt vs GDP'] = (government_debt_df['Government Debt vs GDP'] / 100).round(2)
    return government_debt_df.sort_values(by='Year', ascending=False)

@st.cache_data()
def get_consumer_price_index():
    raw_cpi_df = get_and_combine_data_from_folder('consumer_price_index')
    cpi_df = raw_cpi_df.rename(columns={
        'countryiso3code': 'Country',
        'date': 'Year',
        'value': 'Consumer Price Index'
    }).dropna(subset=['Consumer Price Index'])
    cpi_df['Country'] = cpi_df['Country'].replace(COUNTRY_CODES_W_FLAGS)
    cpi_df['Year'] = pd.to_numeric(cpi_df['Year'])
    cpi_df['Consumer Price Index (%)'] = cpi_df['Consumer Price Index'].round(0)
    cpi_df['Consumer Price Index (%-str)'] = [
        f'{int(val)}%' for val in
        cpi_df['Consumer Price Index (%)']
    ]
    cpi_df['Consumer Price Index'] = (cpi_df['Consumer Price Index'] / 100).round(2)
    return cpi_df.sort_values(by='Year', ascending=False)

@st.cache_data()
def get_gdp_growth_rate():
    raw_gdp_growth_rate_df = get_and_combine_data_from_folder('gdp_growth_rate')
    gdp_growth_rate_df = raw_gdp_growth_rate_df.rename(columns={
        'countryiso3code': 'Country',
        'date': 'Year',
        'value': 'GDP Growth Rate'
    }).dropna(subset=['GDP Growth Rate'])
    gdp_growth_rate_df['Country'] = gdp_growth_rate_df['Country'].replace(COUNTRY_CODES_W_FLAGS)
    gdp_growth_rate_df['Year'] = pd.to_numeric(gdp_growth_rate_df['Year'])
    gdp_growth_rate_df['GDP Growth Rate (%)'] = gdp_growth_rate_df['GDP Growth Rate'].round(1)
    gdp_growth_rate_df['GDP Growth Rate (%-str)'] = [
        f'{round(val, 1)}%' for val in
        gdp_growth_rate_df['GDP Growth Rate (%)']
    ]
    gdp_growth_rate_df['GDP Growth Rate'] = (gdp_growth_rate_df['GDP Growth Rate'] / 100).round(3)
    return gdp_growth_rate_df.sort_values(by='Year', ascending=False)

@st.cache_data()
def get_countries(df):
    countries = list(COUNTRY_CODES_W_FLAGS.values())
    countries += [
        val for val in df['Country'].tolist()
        if val not in countries
    ]
    countries = [country for country in countries if country in df['Country'].unique().tolist()]
    return countries

def plot_metric_by_group(
        metric_df, 
        var_to_group_by_col, 
        metric_col,
        bar_chart=True,
        text_col=None,
        tickformat=None
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
            category_orders=category_orders,
            hover_data=['Year', metric_col, var_to_group_by_col]
        )
        p.update_yaxes(tickformat=tickformat)
        st.plotly_chart(p, use_container_width=True)
    with col2:
        if bar_chart:
            p = px.bar(
                bar_metric_df,
                y=var_to_group_by_col,
                x=metric_col,
                orientation='h',
                title=f'{metric_col} by {var_to_group_by_col} (Year = {int(max_year)})',
                hover_data={text_col: False, var_to_group_by_col: True, metric_col: True},
                category_orders=category_orders,
                text=text_col
            )
            p.update_xaxes(tickformat=tickformat)
        else:
            p = px.pie(
                bar_metric_df,
                names=var_to_group_by_col,
                values=metric_col,
                title=f'{metric_col} by {var_to_group_by_col} (Year = {int(max_year)})',
                hole=0.4,
                category_orders=category_orders,
                hover_data={text_col: False, var_to_group_by_col: True, metric_col: True},
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

def create_section_for_metric(
        metric_df,
        selected_countries,
        to_year,
        from_year,
        section_title='Annual GDP',
        metric_col_name='GDP (T-int)',
        chart_col_name='GDP',
        text_col_name='GDP (T)',
        format_metric_str='${:,.1f}T',
        metric_delta_color='normal',
        chart_tick_format='$.2s'
):
    filtered_metric_df = metric_df[
        (metric_df['Country'].isin(selected_countries))
        & (metric_df['Year'] <= to_year)
        & (from_year <= metric_df['Year'])
    ]
    max_year_filtered_df = filtered_metric_df[filtered_metric_df['Year'] == to_year].sort_values(by=metric_col_name, ascending=False)

    st.header(section_title, divider='gray')

    countries = ['CAN 🇨🇦'] + [
        val for val in
        max_year_filtered_df['Country']
        if val != 'CAN 🇨🇦'
    ]
    cols = st.columns(len(selected_countries))
    i = 0
    for country in countries:
        with cols[i]:
            show_metric(
                filtered_metric_df[filtered_metric_df['Country'] == country],
                metric_col_name,
                title=country,
                format_str=format_metric_str,
                delta_color=metric_delta_color,
            )
        i += 1

    plot_metric_by_group(
        filtered_metric_df,
        'Country',
        bar_chart=True,
        metric_col=chart_col_name,
        text_col=text_col_name,
        tickformat=chart_tick_format
    )

# -----------------------------------------------------------------------------
# Load the data.
gdp_df = get_gdp_data()
population_df = get_population_data()
gdp_per_capita_df = get_gdp_per_capita()
government_debt_df = get_government_debt()
consumer_price_index_df = get_consumer_price_index()
gdp_growth_rate_df = get_gdp_growth_rate()

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
        [   
            'GDP / Capita 💰',
            'GDP 💰', 
            'Population 👥',
            'Government Debt 💳',
            'Consumer Price Index 🛒',
            'GDP Growth Rate 📈'
        ],
    )

with col2:
    selected_countries = st.multiselect(
        'Select Countries',
        countries,
        default=['CAN 🇨🇦', 'USA 🇺🇸']
    )

# -----------------------------------------------------------------------------
# Show the data.

if metric == 'GDP / Capita 💰':
    create_section_for_metric(
        metric_df=gdp_per_capita_df,
        selected_countries=selected_countries,
        to_year=to_year,
        from_year=from_year,
        section_title='Annual GDP per Capita',
        metric_col_name='GDP per Capita (k-int)',
        chart_col_name='GDP per Capita',
        text_col_name='GDP per Capita (k)',
        format_metric_str='${:,.0f}k',
        metric_delta_color='normal',
        chart_tick_format='$.2s'
    )

elif metric == 'GDP 💰':
    create_section_for_metric(
        metric_df=gdp_df,
        selected_countries=selected_countries,
        to_year=to_year,
        from_year=from_year,
        section_title='Annual GDP',
        metric_col_name='GDP (T-int)',
        chart_col_name='GDP',
        text_col_name='GDP (T)',
        format_metric_str='${:,.1f}T',
        metric_delta_color='normal',
        chart_tick_format='$.2s'
    )

elif metric == 'Population 👥':
    create_section_for_metric(
        metric_df=population_df,
        selected_countries=selected_countries,
        to_year=to_year,
        from_year=from_year,
        section_title='Population',
        metric_col_name='Population (M-int)',
        chart_col_name='Population',
        text_col_name='Population (M)',
        format_metric_str='{:,.1f}M',
        metric_delta_color='normal',
        chart_tick_format=None
    )

elif metric == 'Government Debt 💳':
    create_section_for_metric(
        metric_df=government_debt_df,
        selected_countries=selected_countries,
        to_year=to_year,
        from_year=from_year,
        section_title='Government Debt vs GDP',
        metric_col_name='Government Debt vs GDP (%)',
        chart_col_name='Government Debt vs GDP',
        text_col_name='Government Debt vs GDP (%-str)',
        format_metric_str='{:.0f}%',
        metric_delta_color='inverse',
        chart_tick_format=".0%"
    )

elif metric == 'Consumer Price Index 🛒':
    create_section_for_metric(
        metric_df=consumer_price_index_df,
        selected_countries=selected_countries,
        to_year=to_year,
        from_year=from_year,
        section_title='Consumer Price Index (vs 2010)',
        metric_col_name='Consumer Price Index (%)',
        chart_col_name='Consumer Price Index',
        text_col_name='Consumer Price Index (%-str)',
        format_metric_str='{:.0f}%',
        metric_delta_color='inverse',
        chart_tick_format=".0%"
    )

elif metric == 'GDP Growth Rate 📈':
    create_section_for_metric(
        metric_df=gdp_growth_rate_df,
        selected_countries=selected_countries,
        to_year=to_year,
        from_year=from_year,
        section_title='GDP Growth Rate',
        metric_col_name='GDP Growth Rate (%)',
        chart_col_name='GDP Growth Rate',
        text_col_name='GDP Growth Rate (%-str)',
        format_metric_str='{:.1f}%',
        metric_delta_color='normal',
        chart_tick_format=".1%"
    )

st.caption('Data from the [World Bank Open Data](https://data.worldbank.org/) API.')