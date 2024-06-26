import os
import pandas as pd
import streamlit as st
from constants import COUNTRY_CODES_W_FLAGS
import coloredlogs, logging
from decouple import config
from scrape import scrape_core_metrics_for_core_countries
logger = logging.getLogger(__name__)
coloredlogs.install(level=config('LOG_LEVEL', 'INFO'))

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
    gdp_df['GDP (T-int)'] = round(gdp_df['GDP'] / 1e12, 2)
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
def get_labour_force_participation_rate():
    raw_lfpr_df = get_and_combine_data_from_folder('labour_force_participation_rate')
    lfpr_df = raw_lfpr_df.rename(columns={
        'countryiso3code': 'Country',
        'date': 'Year',
        'value': 'Labour Force Participation Rate'
    }).dropna(subset=['Labour Force Participation Rate'])
    lfpr_df['Country'] = lfpr_df['Country'].replace(COUNTRY_CODES_W_FLAGS)
    lfpr_df['Year'] = pd.to_numeric(lfpr_df['Year'])
    lfpr_df['Labour Force Participation Rate (%)'] = lfpr_df['Labour Force Participation Rate'].round(1)
    lfpr_df['Labour Force Participation Rate (%-str)'] = [
        f'{round(val, 1)}%' for val in
        lfpr_df['Labour Force Participation Rate (%)']
    ]
    lfpr_df['Labour Force Participation Rate'] = (lfpr_df['Labour Force Participation Rate'] / 100).round(3)
    return lfpr_df.sort_values(by='Year', ascending=False)

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
    raw_gdp_df = get_and_combine_data_from_folder('gdp')
    gdp_df = raw_gdp_df.rename(columns={
        'countryiso3code': 'Country',
        'date': 'Year',
        'value': 'GDP'
    }).dropna(subset=['GDP'])
    gdp_df['Country'] = gdp_df['Country'].replace(COUNTRY_CODES_W_FLAGS)
    gdp_df['Year'] = pd.to_numeric(gdp_df['Year'])
    gdp_df_prev_year = gdp_df.copy()[['Country', 'Year', 'GDP']]
    gdp_df_prev_year['Year'] = gdp_df_prev_year['Year'] + 1
    gdp_growth_rate_df = gdp_df.merge(
        gdp_df_prev_year,
        on=['Country', 'Year'],
        how='left',
        suffixes=('', '_prev')
    )
    gdp_growth_rate_df['GDP Growth Rate'] = 100 * ((gdp_growth_rate_df['GDP'] / gdp_growth_rate_df['GDP_prev']) - 1)
    gdp_growth_rate_df['Year'] = pd.to_numeric(gdp_growth_rate_df['Year'])
    gdp_growth_rate_df['GDP Growth Rate (%)'] = gdp_growth_rate_df['GDP Growth Rate'].round(1)
    gdp_growth_rate_df['GDP Growth Rate (%-str)'] = [
        f'{round(val, 1)}%' for val in
        gdp_growth_rate_df['GDP Growth Rate (%)']
    ]
    gdp_growth_rate_df['GDP Growth Rate'] = (gdp_growth_rate_df['GDP Growth Rate'] / 100).round(3)
    return gdp_growth_rate_df.sort_values(by='Year', ascending=False)

@st.cache_data()
def get_population_growth_rate():
    raw_population_growth_rate_df = get_and_combine_data_from_folder('population_growth_rate')
    population_growth_rate_df = raw_population_growth_rate_df.rename(columns={
        'countryiso3code': 'Country',
        'date': 'Year',
        'value': 'Population Growth Rate'
    }).dropna(subset=['Population Growth Rate'])
    population_growth_rate_df['Country'] = population_growth_rate_df['Country'].replace(COUNTRY_CODES_W_FLAGS)
    population_growth_rate_df['Year'] = pd.to_numeric(population_growth_rate_df['Year'])
    population_growth_rate_df['Population Growth Rate (%)'] = population_growth_rate_df['Population Growth Rate'].round(1)
    population_growth_rate_df['Population Growth Rate (%-str)'] = [
        f'{round(val, 1)}%' for val in
        population_growth_rate_df['Population Growth Rate (%)']
    ]
    population_growth_rate_df['Population Growth Rate'] = (population_growth_rate_df['Population Growth Rate'] / 100).round(3)
    return population_growth_rate_df.sort_values(by='Year', ascending=False)

@st.cache_data()
def get_unemployment_rate():
    raw_unemployment_rate_df = get_and_combine_data_from_folder('unemployment_rate')
    unemployment_rate_df = raw_unemployment_rate_df.rename(columns={
        'countryiso3code': 'Country',
        'date': 'Year',
        'value': 'Unemployment Rate'
    }).dropna(subset=['Unemployment Rate'])
    unemployment_rate_df['Country'] = unemployment_rate_df['Country'].replace(COUNTRY_CODES_W_FLAGS)
    unemployment_rate_df['Year'] = pd.to_numeric(unemployment_rate_df['Year'])
    unemployment_rate_df['Unemployment Rate (%)'] = unemployment_rate_df['Unemployment Rate'].round(1)
    unemployment_rate_df['Unemployment Rate (%-str)'] = [
        f'{round(val, 1)}%' for val in
        unemployment_rate_df['Unemployment Rate (%)']
    ]
    unemployment_rate_df['Unemployment Rate'] = (unemployment_rate_df['Unemployment Rate'] / 100).round(3)
    return unemployment_rate_df.sort_values(by='Year', ascending=False)

@st.cache_data()
def get_trade_balance():
    raw_trade_balance_df = get_and_combine_data_from_folder('trade_balance')
    trade_balance_df = raw_trade_balance_df.rename(columns={
        'countryiso3code': 'Country',
        'date': 'Year',
        'value': 'Trade Balance'
    }).dropna(subset=['Trade Balance'])
    trade_balance_df['Country'] = trade_balance_df['Country'].replace(COUNTRY_CODES_W_FLAGS)
    trade_balance_df['Year'] = pd.to_numeric(trade_balance_df['Year'])
    trade_balance_df['Trade Balance (%)'] = trade_balance_df['Trade Balance'].round(1)
    trade_balance_df['Trade Balance (%-str)'] = [
        f'{round(val, 1)}%' for val in
        trade_balance_df['Trade Balance (%)']
    ]
    trade_balance_df['Trade Balance'] = (trade_balance_df['Trade Balance'] / 100).round(3)
    return trade_balance_df.sort_values(by='Year', ascending=False)

@st.cache_data()
def get_exports():
    raw_exports_df = get_and_combine_data_from_folder('exports')
    exports_df = raw_exports_df.rename(columns={
        'countryiso3code': 'Country',
        'date': 'Year',
        'value': 'Exports'
    }).dropna(subset=['Exports'])
    exports_df['Country'] = exports_df['Country'].replace(COUNTRY_CODES_W_FLAGS)
    exports_df['Year'] = pd.to_numeric(exports_df['Year'])
    exports_df['Exports (T-int)'] = round(exports_df['Exports'] / 1e12, 2)
    exports_df['Exports (T)'] = [
        f'${val:,.2f}T' for val in
        exports_df['Exports (T-int)']
    ]
    exports_df['Exports'] = (exports_df['Exports'] / 1e9).round(0) * 1e9
    return exports_df.sort_values(by='Year', ascending=False)

@st.cache_data()
def get_imports():
    raw_imports_df = get_and_combine_data_from_folder('imports')
    imports_df = raw_imports_df.rename(columns={
        'countryiso3code': 'Country',
        'date': 'Year',
        'value': 'Imports'
    }).dropna(subset=['Imports'])
    imports_df['Country'] = imports_df['Country'].replace(COUNTRY_CODES_W_FLAGS)
    imports_df['Year'] = pd.to_numeric(imports_df['Year'])
    imports_df['Imports (T-int)'] = round(imports_df['Imports'] / 1e12, 2)
    imports_df['Imports (T)'] = [
        f'${val:,.2f}T' for val in
        imports_df['Imports (T-int)']
    ]
    imports_df['Imports'] = (imports_df['Imports'] / 1e9).round(0) * 1e9
    return imports_df.sort_values(by='Year', ascending=False)

@st.cache_data()
def get_birth_rate():
    raw_birth_rate_df = get_and_combine_data_from_folder('birth_rate')
    birth_rate_df = raw_birth_rate_df.rename(columns={
        'countryiso3code': 'Country',
        'date': 'Year',
        'value': 'Birth Rate'
    }).dropna(subset=['Birth Rate'])
    birth_rate_df['Country'] = birth_rate_df['Country'].replace(COUNTRY_CODES_W_FLAGS)
    birth_rate_df['Year'] = pd.to_numeric(birth_rate_df['Year'])
    birth_rate_df['Birth Rate'] = birth_rate_df['Birth Rate'].round(1)
    return birth_rate_df.sort_values(by='Year', ascending=False)

@st.cache_data()
def get_death_rate():
    raw_death_rate_df = get_and_combine_data_from_folder('death_rate')
    death_rate_df = raw_death_rate_df.rename(columns={
        'countryiso3code': 'Country',
        'date': 'Year',
        'value': 'Death Rate'
    }).dropna(subset=['Death Rate'])
    death_rate_df['Country'] = death_rate_df['Country'].replace(COUNTRY_CODES_W_FLAGS)
    death_rate_df['Year'] = pd.to_numeric(death_rate_df['Year'])
    death_rate_df['Death Rate'] = death_rate_df['Death Rate'].round(1)
    return death_rate_df.sort_values(by='Year', ascending=False)

@st.cache_data()
def get_life_expectancy():
    raw_life_expectancy_df = get_and_combine_data_from_folder('life_expectancy')
    life_expectancy_df = raw_life_expectancy_df.rename(columns={
        'countryiso3code': 'Country',
        'date': 'Year',
        'value': 'Life Expectancy'
    }).dropna(subset=['Life Expectancy'])
    life_expectancy_df['Country'] = life_expectancy_df['Country'].replace(COUNTRY_CODES_W_FLAGS)
    life_expectancy_df['Year'] = pd.to_numeric(life_expectancy_df['Year'])
    life_expectancy_df['Life Expectancy'] = life_expectancy_df['Life Expectancy'].round(1)
    return life_expectancy_df.sort_values(by='Year', ascending=False)