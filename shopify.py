headers = {
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
}

import requests
import json
from bs4 import BeautifulSoup
import sys
import csv
import os

i = 1
url = input('Enter shopify website link, such as flashepic.com: ')
if 'http' not in url:
    weburl = 'https://' + url
else:
    weburl = url
results = []
while True:
    res = requests.get(f'{weburl}/products.json?page={i}',headers=headers)
    products = json.loads(res.text)['products']
    if len(products) == 0:
        break
    for product in products:
        name = product['title']
        description=BeautifulSoup(product['body_html'],'lxml').text
        image = product['images'][0]['src']
        price = float(product['variants'][0]['price']) * 0.7
        price = str(round(price,2))
        tax_status = 'taxable'
        tax_product_shipping_class = 'Class 1'
        results=[[name,description,price,image]]
        if os.path.exists(f'{url}_data.csv'):
            newfile = False
        else:
            newfile = True
        with open(f'{url}_data.csv','a',newline='',encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            if newfile:
                writer.writerows([['Product Name', 'Product Description', 'Price', 'Product Image']])
            writer.writerows(results)
    i+=1
    sys.stdout.write(".")
    sys.stdout.flush()