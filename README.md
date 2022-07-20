# NFC-e Scraper

API to extract data from NFC-e (Brazilian electronic consumer invoice) data.

Documentation: https://nfce-scraper.herokuapp.com/docs

## How it works?

* Request example: 

~~~ sh
curl -X 'GET' \
  'https://nfce-scraper.herokuapp.com/nfce?nfce_url=<nfce_url>' \
  -H 'accept: application/json'
~~~

* Output example: 
~~~ javascript 
[
  {
    "item": "TOMADA 2P T 10A 250V 4X2 COMPOSE BR 1327",
    "id": 156725,
    "unity": "UN",
    "amount": 1,
    "unity_price": 16.27,
    "price": 16.27
  },
  {
    "item": "TOMADA 2TOM 2P T 20A 250V 4X2 COMPOSE BR",
    "id": 156727,
    "unity": "UN",
    "amount": 1,
    "unity_price": 26.04,
    "price": 26.04
  },
  {
    "item": "VEDA ROSCA 18X10 54501854 TIGRE",
    "id": 1225,
    "unity": "UN",
    "amount": 1,
    "unity_price": 6.26,
    "price": 6.26
  }
]
~~~

## Where to get an NFC-e URL? 

Brazilian consumer invoices contain a QR code, which, when scanned, generates an entry URL for this API. They are like: http://www.fazenda.pr.gov.br/nfce/qrcode?p=<nfce-code>.

## Test it out

~~~ sh
git clone https://github.com/leonichel/nfce-scraper.git
cd nfce-scraper
docker build -t nfce-scraper-image -f Dockerfile . 
docker run -d --name nfce-scraper-container -p 80:80 nfce-scraper-image
~~~
