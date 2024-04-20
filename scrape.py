import requests
from constants import CORE_URLS_PER_COUNTRY, CORE_COUNTRIES_TO_SCRAPE_INITIALLY, COUNTRY_CODES_W_FLAGS
import coloredlogs, logging
from tqdm import tqdm
import pandas as pd
import os
from decouple import config
logger = logging.getLogger(__name__)
coloredlogs.install(level=config('LOG_LEVEL', 'INFO'))

def get_data_per_country(country: str, url :str) -> pd.DataFrame:
    try:
        logger.info(f'Getting page 1 of {country} - url: {url}...')
        response = requests.get(url.format(country=country))
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data[1])
        if data[0]['pages'] > 1:
            for page in range(2, data[0]['pages'] + 1):
                logger.info(f'Getting page {page} of {country} - url: {url}...')
                response = requests.get(url.format(country=country), params={'page': page})
                response.raise_for_status()
                data = response.json()
                df = pd.concat([df, pd.DataFrame(data[1])])
        return df
    except requests.exceptions.HTTPError as err:
        logger.error(err)
        return None

def scrape_core_metrics_for_core_countries():
    logger.info('Getting core metrics for core countries...')
    if not os.path.exists('./data'):
        os.makedirs('./data')
    for metric in tqdm(CORE_URLS_PER_COUNTRY):
        metric_folder_path = f'./data/{metric}'
        if not os.path.exists(metric_folder_path):
            os.mkdir(metric_folder_path)
        logger.info(f'Getting data for {metric}...')
        for country in CORE_COUNTRIES_TO_SCRAPE_INITIALLY:
            logger.info(f'Getting data for {country}...')
            df = get_data_per_country(country, CORE_URLS_PER_COUNTRY[metric])
            if df is None:
                logger.warning(f'No data found for {COUNTRY_CODES_W_FLAGS[country]} ❌')
                continue
            else:
                df.to_csv(f'{metric_folder_path}/{country}.csv', index=False)
                logger.info(f'Saved {metric_folder_path}/{country}.csv 💾')
        logger.info(f'Done getting data for {metric}! ✅')
    logger.info('Done getting all core metrics for core countries! ✅ 🎉')

if __name__ == '__main__':
    scrape_core_metrics_for_core_countries()