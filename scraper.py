from bs4 import BeautifulSoup
import requests
import re, time

def clean(t):
    word1 = re.sub(r'\[[0-9]+\]', '', t)
    word1 = " ".join(re.findall(r'[a-zA-Z0-9\.\%]+', word1))
    return word1

# Creating TS for unique file name
ts = str(int(time.time()))

apac = 'https://en.wikipedia.org/wiki/List_of_mobile_network_operators_of_the_Asia_Pacific_region'
emea = 'https://en.wikipedia.org/wiki/List_of_mobile_network_operators_of_the_Middle_East_and_Africa'
europe = 'https://en.wikipedia.org/wiki/List_of_mobile_network_operators_of_Europe'
americas = 'https://en.wikipedia.org/wiki/List_of_mobile_network_operators_of_the_Americas'

regions = [apac, emea, europe, americas]

final_list = []

for region in regions:

    res = requests.get(region)

    html = res.text

    soup = BeautifulSoup(html, 'html.parser')

    countries = soup.find_all(class_='mw-heading')

    for i, country in enumerate(countries):
        c = country.text
        t = country.findNext('table', class_='wikitable')

        try:
            rows = t.find_all('tr')
            for r in rows:
                temp = [clean(x.text) for x in r.find_all('td')]
                final_list.append([c] + temp)
        except Exception as e:
            pass
for i in final_list:
    if len(i) > 2:
        try:
            if i[4] == '' or i[4] == 'Not Yet Available' or i[4] == 'Not Available' or i[4] == 'N/A' or i[4] == '(Information not available)' or i[4] == '?' or i[4] == '-':
                i[4] = 'NA'
            print(i)
        except Exception as e:
            print(e)
with open(ts + '_List_of_mobile_network_operators.csv', 'w') as wf:
    # Write headers
    wf.write('Country;Rank;Operator;Technology;Subscribers;Owner\n')

    for i in final_list:
        if len(i) > 2:
            wf.write(';'.join(i).encode('ascii', 'ignore').decode('ascii') + '\n')
