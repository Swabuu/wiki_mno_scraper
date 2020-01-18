from bs4 import BeautifulSoup
import requests
import re

def clean(t):
	word1 = " ".join(re.findall("[a-zA-Z0-9\.]+", t))
	return word1

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

	countries = soup.find_all(class_='mw-headline')

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

with open('List_of_mobile_network_operators.csv', 'w') as wf:

	for i in final_list:
		if len(i) > 2:
			wf.write(';'.join(i) + '\n')

