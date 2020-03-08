import requests
from bs4 import BeautifulSoup

url = "https://www.gov.uk/government/publications/coronavirus-covid-19-number-of-cases-in-england/coronavirus-covid-19-number-of-cases-in-england"

url = "https://web.archive.org/web/20200306192042/https://www.gov.uk/government/publications/coronavirus-covid-19-number-of-cases-in-england/coronavirus-covid-19-number-of-cases-in-england"

response = requests.get(url)
soup = BeautifulSoup(response.text, features="html5lib")

json = "{"
for tr in soup.find_all('tr')[1:]:
    tds = tr.find_all('td')
    json += "\"%s\": %s," % (tds[0].text, tds[1].text)
json += "}";
print(json);
