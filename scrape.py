import requests

# ----------GDP per Capita----------
# CAN
url = 'https://api.worldbank.org/v2/countries/CAN/indicators/NY.GDP.PCAP.CD?format=json'
# TODO: need to iterate over all pages of the response
response = requests.get(url)
print(response.json())

# US
url = 'https://api.worldbank.org/v2/countries/USA/indicators/NY.GDP.PCAP.CD?format=json'
response = requests.get(url)
print(response.json())


# -----------Consumer Price Index-----------
# CAN
url = "http://api.worldbank.org/v2/countries/CAN/indicator/FP.CPI.TOTL?format=json"
response = requests.get(url)
print(response.json())

# US
url = "http://api.worldbank.org/v2/countries/USA/indicator/FP.CPI.TOTL?format=json"
response = requests.get(url)
print(response.json())


# -----------Unemployment Rate-----------
# CAN
url = "http://api.worldbank.org/v2/countries/CAN/indicator/SL.UEM.TOTL.ZS?format=json"
response = requests.get(url)
print(response.json())

# US
url = "http://api.worldbank.org/v2/countries/USA/indicator/SL.UEM.TOTL.ZS?format=json"
response = requests.get(url)
print(response.json())


# -----------GDP-----------
# CAN
url = "http://api.worldbank.org/v2/countries/CAN/indicator/NY.GDP.MKTP.CD?format=json"
response = requests.get(url)
print(response.json())

# US
url = "http://api.worldbank.org/v2/countries/USA/indicator/NY.GDP.MKTP.CD?format=json"
response = requests.get(url)
print(response.json())


# -----------GDP Growth Rate-----------
# CAN
url = "http://api.worldbank.org/v2/countries/CAN/indicator/NY.GDP.MKTP.KD.ZG?format=json"
response = requests.get(url)
print(response.json())

# US
url = "http://api.worldbank.org/v2/countries/USA/indicator/NY.GDP.MKTP.KD.ZG?format=json"
response = requests.get(url)
print(response.json())



# ----------Labor Force Participation Rate----------
# CAN
url = "http://api.worldbank.org/v2/countries/CAN/indicator/SL.TLF.CACT.ZS?format=json"
response = requests.get(url)
print(response.json())

# US
url = "http://api.worldbank.org/v2/countries/USA/indicator/SL.TLF.CACT.ZS?format=json"
response = requests.get(url)
print(response.json())


# -----------Government Debt-----------
# CAN
url = "http://api.worldbank.org/v2/countries/CAN/indicator/GC.DOD.TOTL.GD.ZS?format=json"
response = requests.get(url)
print(response.json())

# US
url = "http://api.worldbank.org/v2/countries/USA/indicator/GC.DOD.TOTL.GD.ZS?format=json"
response = requests.get(url)
print(response.json())


# -----------Exports-----------
# CAN
url = "http://api.worldbank.org/v2/countries/CAN/indicator/NE.EXP.GNFS.CD?format=json"
response = requests.get(url)
print(response.json())

# US
url = "http://api.worldbank.org/v2/countries/USA/indicator/NE.EXP.GNFS.CD?format=json"
response = requests.get(url)
print(response.json())

# -----------Imports-----------
# CAN
url = "http://api.worldbank.org/v2/countries/CAN/indicator/NE.IMP.GNFS.CD?format=json"
response = requests.get(url)
print(response.json())

# US
url = "http://api.worldbank.org/v2/countries/USA/indicator/NE.IMP.GNFS.CD?format=json"
response = requests.get(url)
print(response.json())
