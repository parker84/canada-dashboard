import streamlit as st
from plotly import express as px
from constants import COUNTRY_CODES_W_FLAGS
import coloredlogs, logging
from decouple import config
from get_data import (
    get_gdp_data,
    get_population_data,
    get_gdp_per_capita,
    get_government_debt,
    get_consumer_price_index,
    get_gdp_growth_rate,
    get_population_growth_rate,
    get_labour_force_participation_rate,
    get_unemployment_rate,
    get_exports,
    get_imports
)
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
population_growth_rate_df = get_population_growth_rate()
labour_force_participation_rate_df = get_labour_force_participation_rate()
unemployment_rate_df = get_unemployment_rate()
exports_df = get_exports()
imports_df = get_imports()

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
            'GDP Growth Rate 📈',
            'Population Growth Rate 📈',
            'Labour Force Participation Rate 💼',
            'Unemployment Rate 🛋️',
            'Exports ➡️',
            'Imports ⬅️',
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

elif metric == 'Population Growth Rate 📈':
    create_section_for_metric(
        metric_df=population_growth_rate_df,
        selected_countries=selected_countries,
        to_year=to_year,
        from_year=from_year,
        section_title='Population Growth Rate',
        metric_col_name='Population Growth Rate (%)',
        chart_col_name='Population Growth Rate',
        text_col_name='Population Growth Rate (%-str)',
        format_metric_str='{:.1f}%',
        metric_delta_color='normal',
        chart_tick_format=".1%"
    )

elif metric == 'Labour Force Participation Rate 💼':
    create_section_for_metric(
        metric_df=labour_force_participation_rate_df,
        selected_countries=selected_countries,
        to_year=to_year,
        from_year=from_year,
        section_title='Labour Force Participation Rate',
        metric_col_name='Labour Force Participation Rate (%)',
        chart_col_name='Labour Force Participation Rate',
        text_col_name='Labour Force Participation Rate (%-str)',
        format_metric_str='{:.1f}%',
        metric_delta_color='normal',
        chart_tick_format=".1%"
    )

elif metric == 'Unemployment Rate 🛋️':
    create_section_for_metric(
        metric_df=unemployment_rate_df,
        selected_countries=selected_countries,
        to_year=to_year,
        from_year=from_year,
        section_title='Unemployment Rate',
        metric_col_name='Unemployment Rate (%)',
        chart_col_name='Unemployment Rate',
        text_col_name='Unemployment Rate (%-str)',
        format_metric_str='{:.1f}%',
        metric_delta_color='inverse',
        chart_tick_format=".1%"
    )

elif metric == 'Exports ➡️':
    create_section_for_metric(
        metric_df=exports_df,
        selected_countries=selected_countries,
        to_year=to_year,
        from_year=from_year,
        section_title='Exports',
        metric_col_name='Exports (T-int)',
        chart_col_name='Exports',
        text_col_name='Exports (T)',
        format_metric_str='${:,.2f}T',
        metric_delta_color='normal',
        chart_tick_format='$.3s'
    )

elif metric == 'Imports ⬅️':
    create_section_for_metric(
        metric_df=imports_df,
        selected_countries=selected_countries,
        to_year=to_year,
        from_year=from_year,
        section_title='Imports',
        metric_col_name='Imports (T-int)',
        chart_col_name='Imports',
        text_col_name='Imports (T)',
        format_metric_str='${:,.2f}T',
        metric_delta_color='normal',
        chart_tick_format='$.3s'
    )

st.caption('Data from the [World Bank Open Data](https://data.worldbank.org/) API.')