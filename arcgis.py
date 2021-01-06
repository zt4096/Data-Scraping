print('Importing Libraries...')
from selenium import webdriver
from selenium.webdriver.common.action_chains  import ActionChains
import time
import os
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--start-maximized")
df = pd.read_csv('platlot.csv')

platlots = list(df['Plat-Lot '])
print(len(platlots),'plat-lot found.')
def findelem(xpath):
    return driver.find_element_by_xpath(f'//{xpath}')
def findelems(xpath):
    return driver.find_elements_by_xpath(f'//{xpath}')
driver = webdriver.Chrome(options=options)
summary = []
for plat_lot in platlots:
    print(f'Searching data for {plat_lot}...')
    driver.get('https://cranston.maps.arcgis.com/apps/webappviewer/index.html?id=bb961d0b19454c30b3435f43acfc784d')
    myElem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,'//div[@id="jimu_dijit_CheckBox_0"]')))
    time.sleep(5)
    cb = findelem('div[@id="jimu_dijit_CheckBox_0"]')
    driver.execute_script("arguments[0].click();", cb)
    time.sleep(1)
    ok = findelem('button[@title="OK"]')
    driver.execute_script("arguments[0].click();", ok)
    time.sleep(3)
    findelem('input[@class="searchInput"]').clear()
    findelem('input[@class="searchInput"]').send_keys(plat_lot)
    time.sleep(1)
    findelem('input[@class="searchInput"]').send_keys(Keys.ENTER)
    time.sleep(5)
    res = driver.execute_script("return document.documentElement.outerHTML")
    soup = BeautifulSoup(res,'html.parser')
    output = []
    # for i in driver.find_elements_by_xpath('//div[@class="mainSection"]/descendant-or-self::span'):
    try:
        output.append([soup.find('div',{'class':'header'}).text])
        summary.append([soup.find('div',{'class':'header'}).text])
    except:
        print(f'Data not found for {plat_lot}.')
        continue
    for i in soup.find('div',{'class':'mainSection'}).findAll('span'):
        if i.text!= ' ' and i.text!='':
            output.append([i.text.strip()])
    os.mkdir(plat_lot)
    file = f'{plat_lot}/{plat_lot}_results.csv'
    outfile = open(file, "w")
    for row in output:
        outfile.write('"' + '","'.join(row) + '"\n')
    outfile.close()

    click_here = findelem('a[text()="Click Here"]').get_attribute('href')
    driver.get(click_here)
    myElem = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID,'lblPropCardTitle')))
    time.sleep(2)
    pdf_links = [(i.text,i.get_attribute('href')) for i in findelems('a[contains(@id,"DLPropCards_c")]')]
    print('Downloading pdf files...')
    for pdf_link in pdf_links:
        filename = Path(f'{plat_lot}/{pdf_link[0]}.pdf')
        url = pdf_link[1]
        response = requests.get(url)
        filename.write_bytes(response.content)

    output = []
    table = findelem('table[@id="GridView1"]')
    rows = table.find_elements_by_tag_name('tr')
    for row in rows:
        output.append(['{}'.format(x.text) for x in row.find_elements_by_tag_name('td')])
    file = os.path.join(f'{plat_lot}/{plat_lot}_title_card.csv')
    outfile = open(file, "w")
    for row in output:
        outfile.write('"' + '","'.join(row) + '"\n')
    outfile.close()
    print(f'Scraping completed for {plat_lot}.')

outfile = open('summary_document.csv', "w")
for row in summary:
    outfile.write('"' + '","'.join(row) + '"\n')
outfile.close()
print('summary_document.csv saved.')
driver.close()
print('Scraping completed.')