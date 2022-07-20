from fastapi import FastAPI
from bs4 import BeautifulSoup
import requests

HEADERS = requests.utils.default_headers()
HEADERS.update({'User-Agent': 'My User Agent 1.0'})

app = FastAPI()

@app.get('/nfce')
async def read_nfce(nfce_url: str = ''):
	request = requests.get(nfce_url, headers=HEADERS)
	soup = BeautifulSoup(request.text, 'html.parser')
	items = [item.get_text() for item in soup.find_all('span', class_='txtTit2')]
	codes = [int(item.get_text().split(': ')[1].replace(')', '')) for item in soup.find_all('span', class_='RCod')]
	unity = ['KG' if item.get_text().find('KG') != -1 else 'UN' for item in soup.find_all('span', class_='RUN')]
	amount = [float(item.get_text().replace(' ', '').replace('Qtde.:', '').replace('\n', '').replace(',', '.')) for item in soup.find_all('span', class_='Rqtd')]
	unity_price = [float(item.get_text().replace(u'\xa0', u'').replace('\nVl. Unit.:', '').replace(' ', '').replace('\n', '').replace(',', '.')) for item in soup.find_all('span', class_='RvlUnit')]
	price = [float(item.get_text().replace(',', '.')) for item in soup.find_all('span', class_='valor')]
	data = {
    'item': items,
    'id': codes,
    'unity': unity,
    'amount': amount,
    'unity_price': unity_price,
    'price': price
		}	
	data_list = [dict(zip(data,t)) for t in zip(*data.values())]

	return data_list