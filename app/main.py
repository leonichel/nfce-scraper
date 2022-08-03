from unities_codes import UNITIES_DECODE 
import re
import requests
from fastapi import FastAPI
from bs4 import BeautifulSoup
from datetime import datetime

HEADERS = requests.utils.default_headers()
HEADERS.update({'User-Agent': 'My User Agent 1.0'})

app = FastAPI()

@app.get('/nfce')
async def read_nfce(nfce_url: str = ''):
	request = requests.get(nfce_url, headers=HEADERS)
	soup = BeautifulSoup(request.text, 'html.parser')

	store = soup.find_all('div', class_='txtTopo')[0].text
	cnpj = [item.text.replace('\n\t\t    CNPJ:\n\t\t    ', '').replace('\n', '').replace('\t', '') for item in soup.find_all('div', class_='text')][0]
	address = [item.text.replace('\n\t\t    CNPJ:\n\t\t    ', '').replace('\n', '').replace('\t', '') for item in soup.find_all('div', class_='text')][1]
	quantity = int([item.get_text() for item in soup.find_all('span', class_='totalNumb')][0])
	price_total = float([item.get_text() for item in soup.find_all('span', class_='totalNumb txtMax')][0].replace(',', '.'))
	payment_method = [item.get_text() for item in soup.find_all('label', class_='tx')][0]
	date = datetime.strptime(soup.find_all(text=re.compile('Via Consumidor'))[0].replace('  - Via Consumidor\n\n     ', ''), '%d/%m/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
	key = [item.get_text() for item in soup.find_all('span', class_='chave')][0]

	customer_document = None
	customer_name = None
	try:
		customer_document = [item.get_text() for item in soup.find_all('li') if 'CPF' in item.get_text()][0].replace('\nCPF: ', '').replace('\n    ', '')
		customer_name = [item.get_text() for item in soup.find_all('li') if 'Nome' in item.get_text()][0].replace('\nNome: ', '').replace('\n    ', '')
	except Exception: 
		pass

	items = [item.get_text() for item in soup.find_all('span', class_='txtTit2')]
	codes = [int(item.get_text().split(': ')[1].replace(')', '')) for item in soup.find_all('span', class_='RCod')]
	unities = [UNITIES_DECODE[item.get_text().replace('UN: ', '').replace('\n', '').replace(' ', '').upper()] if item.get_text().replace('UN: ', '').replace('\n', '').replace(' ', '').upper() in UNITIES_DECODE else 'unidade' for item in soup.find_all('span', class_='RUN')]
	amounts = [float(item.get_text().replace(' ', '').replace('Qtde.:', '').replace('\n', '').replace(',', '.')) for item in soup.find_all('span', class_='Rqtd')]
	unity_prices = [float(item.get_text().replace(u'\xa0', u'').replace('\nVl. Unit.:', '').replace(' ', '').replace('\n', '').replace(',', '.')) for item in soup.find_all('span', class_='RvlUnit')]
	prices = [float(item.get_text().replace(',', '.')) for item in soup.find_all('span', class_='valor')]

	items_data = {
		'item': items,
		'id': codes,
		'unity': unities,
		'amount': amounts,
		'unity_price': unity_prices,
		'price': prices
	}	

	items_list = [dict(zip(items_data,t)) for t in zip(*items_data.values())]

	nfce_data = {
		'store': store,
		'cnpj': cnpj,
		'address': address,
		'quantity': quantity,
		'price_total': price_total,
		'payment_method': payment_method,
		'date': date,
		'key': key,
		'customer_document': customer_document,
		'customer_name': customer_name,
		'items': items_list
	}

	return nfce_data
