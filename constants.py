

CORE_URLS_PER_COUNTRY = {
    'gdp_per_capita': 'https://api.worldbank.org/v2/countries/{country}/indicators/NY.GDP.PCAP.CD?format=json',
    # 'consumer_price_index': 'http://api.worldbank.org/v2/countries/{country}/indicator/FP.CPI.TOTL?format=json',
    'gdp': 'http://api.worldbank.org/v2/countries/{country}/indicator/NY.GDP.MKTP.CD?format=json',
    # 'gdp_growth_rate': 'http://api.worldbank.org/v2/countries/{country}/indicator/NY.GDP.MKTP.KD.ZG?format=json',
    # 'house_price_index': 'http://api.worldbank.org/v2/countries/{country}/indicator/NY.GDP.MKTP.CD?format=json',
    'population': 'http://api.worldbank.org/v2/countries/{country}/indicator/SP.POP.TOTL?format=json',
    # 'government_debt': 'http://api.worldbank.org/v2/countries/{country}/indicator/GC.DOD.TOTL.GD.ZS?format=json',
    # 'population_growth_rate': 'http://api.worldbank.org/v2/countries/{country}/indicator/SP.POP.GROW?format=json',
    # 'labour_force_participation_rate': 'http://api.worldbank.org/v2/countries/{country}/indicator/SL.TLF.CACT.ZS?format=json',
    # 'unemployment_rate': 'http://api.worldbank.org/v2/countries/{country}/indicator/SL.UEM.TOTL.ZS?format=json',
    # 'exports': 'http://api.worldbank.org/v2/countries/{country}/indicator/NE.EXP.GNFS.CD?format=json',
    # 'imports': 'http://api.worldbank.org/v2/countries/{country}/indicator/NE.IMP.GNFS.CD?format=json',
}

EXTRA_URLS_PER_COUNTRY = {
    'trade_balance': 'http://api.worldbank.org/v2/countries/{country}/indicator/NE.TRD.GNFS.ZS?format=json',
    'net_migration_rate': 'http://api.worldbank.org/v2/countries/{country}/indicator/SM.POP.NETM?format=json',
    'birth_rate': 'http://api.worldbank.org/v2/countries/{country}/indicator/SP.DYN.CBRT.IN?format=json',
    'population_density': 'http://api.worldbank.org/v2/countries/{country}/indicator/EN.POP.DNST?format=json',
    'urban_population': 'http://api.worldbank.org/v2/countries/{country}/indicator/SP.URB.TOTL.IN.ZS?format=json',
    'life_expectancy': 'http://api.worldbank.org/v2/countries/{country}/indicator/SP.DYN.LE00.IN?format=json',
    'mortality_rate': 'http://api.worldbank.org/v2/countries/{country}/indicator/SH.DYN.MORT?format=json',
    'fertility_rate': 'http://api.worldbank.org/v2/countries/{country}/indicator/SP.DYN.TFRT.IN?format=json',
    'gini_index': 'http://api.worldbank.org/v2/countries/{country}/indicator/SI.POV.GINI?format=json',
    'hdi': 'http://api.worldbank.org/v2/countries/{country}/indicator/HDI?format=json',
    'gni': 'http://api.worldbank.org/v2/countries/{country}/indicator/NY.GNP.MKTP.CD?format=json',
    'gni_per_capita': 'http://api.worldbank.org/v2/countries/{country}/indicator/NY.GNP.PCAP.CD?format=json',
    'poverty_rate': 'http://api.worldbank.org/v2/countries/{country}/indicator/SI.POV.DDAY?format=json',
    'education_expenditure': 'http://api.worldbank.org/v2/countries/{country}/indicator/SE.XPD.TOTL.GD.ZS?format=json',
    'health_expenditure': 'http://api.worldbank.org/v2/countries/{country}/indicator/SH.XPD.CHEX.GD.ZS?format=json',
    'military_expenditure': 'http://api.worldbank.org/v2/countries/{country}/indicator/MS.MIL.XPND.GD.ZS?format=json',
    'internet_users': 'http://api.worldbank.org/v2/countries/{country}/indicator/IT.NET.USER.ZS?format=json',
    'mobile_subscriptions': 'http://api.worldbank.org/v2/countries/{country}/indicator/IT.CEL.SETS.P2?format=json',
    'electricity_consumption': 'http://api.worldbank.org/v2/countries/{country}/indicator/EG.USE.ELEC.KH.PC?format=json',
    'co2_emissions': 'http://api.worldbank.org/v2/countries/{country}/indicator/EN.ATM.CO2E.KT?format=json',
    'forest_area': 'http://api.worldbank.org/v2/countries/{country}/indicator/AG.LND.FRST.ZS?format=json',
    'arable_land': 'http://api.worldbank.org/v2/countries/{country}/indicator/AG.LND.ARBL.ZS?format=json',
    'cereal_yield': 'http://api.worldbank.org/v2/countries/{country}/indicator/AG.YLD.CREL.KG?format=json',
    'food_production_index': 'http://api.worldbank.org/v2/countries/{country}/indicator/AG.PRD.FOOD.XD?format=json',
    'life_satisfaction': 'http://api.worldbank.org/v2/countries/{country}/indicator/AG.LND.ARBL.ZS?format=json',
    'happiness_index': 'http://api.worldbank.org/v2/countries/{country}/indicator/AG.LND.ARBL.ZS?format=json',
}

CORE_URLS_ALL_COUNTRIES = {
    key: val.replace('/{country}', '')
    for key, val in CORE_URLS_PER_COUNTRY.items()
}

EXTRA_URLS_ALL_COUNTRIES = {
    key: val.replace('/{country}', '')
    for key, val in EXTRA_URLS_PER_COUNTRY.items()
}

CORE_COUNTRIES_TO_SCRAPE_INITIALLY = [
    'CAN',
    'USA',
    'CHN',
    'IND',
    'JPN',
    'RUS',
    'GBR',
    'BRA',
    'DEU',
    'FRA',
    'ITA',
    'GRC',
    'WLD',
    'AUS',
    'SGP',
    'LUX',
    'CHE',
    'NOR',
    'SWE',
    'DNK',
    'ISL',
    'QAT',
    'IRL',
]

COUNTRY_CODES_W_FLAGS = {
    'CAN': 'CAN 🇨🇦',
    'USA': 'USA 🇺🇸',
    'CHN': 'CHN 🇨🇳',
    'IND': 'IND 🇮🇳',
    'JPN': 'JPN 🇯🇵',
    'RUS': 'RUS 🇷🇺',
    'GBR': 'GBR 🇬🇧',
    'BRA': 'BRA 🇧🇷', 
    'FRA': 'FRA 🇫🇷',
    'ITA': 'ITA 🇮🇹',
    'GRC': 'GRC 🇬🇷',
    'WLD': 'WLD 🌍',
    'DEU': 'DEU 🇩🇪',  # Germany
    'AUS': 'AUS 🇦🇺',  # Australia
    'ESP': 'ESP 🇪🇸',  # Spain
    'MEX': 'MEX 🇲🇽',  # Mexico
    'KOR': 'KOR 🇰🇷',  # South Korea
    'IDN': 'IDN 🇮🇩',  # Indonesia
    'TUR': 'TUR 🇹🇷',  # Turkey
    'SAU': 'SAU 🇸🇦',  # Saudi Arabia
    'IRN': 'IRN 🇮🇷',  # Iran
    'CHE': 'CHE 🇨🇭',  # Switzerland
    'NLD': 'NLD 🇳🇱',  # Netherlands
    'SWE': 'SWE 🇸🇪',  # Sweden
    'POL': 'POL 🇵🇱',  # Poland
    'BEL': 'BEL 🇧🇪',  # Belgium
    'ARG': 'ARG 🇦🇷',  # Argentina
    'NOR': 'NOR 🇳🇴',  # Norway
    'AUT': 'AUT 🇦🇹',  # Austria
    'ARE': 'ARE 🇦🇪',  # United Arab Emirates
    'ISR': 'ISR 🇮🇱',
    'ZAF': 'ZAF 🇿🇦',
    'SGP': 'SGP 🇸🇬',
    'MYS': 'MYS 🇲🇾',
    'PHL': 'PHL 🇵🇭',
    'COL': 'COL 🇨🇴',
    'CHL': 'CHL 🇨🇱',
    'EGY': 'EGY 🇪🇬',
    'PAK': 'PAK 🇵🇰',
    'VNM': 'VNM 🇻🇳',
    'PER': 'PER 🇵🇪',
    'ROU': 'ROU 🇷🇴',
    'CZE': 'CZE 🇨🇿',    
    'PRT': 'PRT 🇵🇹',
    'DNK': 'DNK 🇩🇰',
    'FIN': 'FIN 🇫🇮',
    'HUN': 'HUN 🇭🇺',
    'NZL': 'NZL 🇳🇿',
    'GTM': 'GTM 🇬🇹',
    'HRV': 'HRV 🇭🇷',
    'URY': 'URY 🇺🇾',
    'SVN': 'SVN 🇸🇮',
    'LUX': 'LUX 🇱🇺',
    'SVK': 'SVK 🇸🇰',
    'EST': 'EST 🇪🇪',
    'LVA': 'LVA 🇱🇻',
    'LTU': 'LTU 🇱🇹',
    'CRI': 'CRI 🇨🇷',
    'PAN': 'PAN 🇵🇦',
    'BGR': 'BGR 🇧🇬',
    'CYP': 'CYP 🇨🇾',
    'MLT': 'MLT 🇲🇹',
    'ISL': 'ISL 🇮🇸',
    'LIE': 'LIE 🇱🇮',
    'MCO': 'MCO 🇲🇨',
    'AND': 'AND 🇦🇩',
    'MNE': 'MNE 🇲🇪',
    'SRB': 'SRB 🇷🇸',
    'ALB': 'ALB 🇦🇱',
    'MKD': 'MKD 🇲🇰',
    'BIH': 'BIH 🇧🇦',
    'KAZ': 'KAZ 🇰🇿',
    'BLR': 'BLR 🇧🇾',
    'UKR': 'UKR 🇺🇦',
    'MDA': 'MDA 🇲🇩',
    'ARM': 'ARM 🇦🇲',
    'GEO': 'GEO 🇬🇪',
    'AZE': 'AZE 🇦🇿',
    'UZB': 'UZB 🇺🇿',
    'TJK': 'TJK 🇹🇯',
    'KGZ': 'KGZ 🇰🇬',
    'TKM': 'TKM 🇹🇲',
    'TUR': 'TUR 🇹🇷',
    'IRQ': 'IRQ 🇮🇶',
    'SYR': 'SYR 🇸🇾',
    'JOR': 'JOR 🇯🇴',
    'LBN': 'LBN 🇱🇧',
    'PSE': 'PSE 🇵🇸',
    'YEM': 'YEM 🇾🇪',
    'OMN': 'OMN 🇴🇲',
    'QAT': 'QAT 🇶🇦',
    'BHR': 'BHR 🇧🇭',
    'KWT': 'KWT 🇰🇼',
    'IRL': 'IRL 🇮🇪',
}