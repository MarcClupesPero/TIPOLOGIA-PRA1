from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time
import requests
#Activa el driver i obre la pàgina principal
driver = webdriver.Chrome(
        'C:/Users/marcc/Desktop/UOC/TIPOLOGIA I CICLE DE VIDA/chromedriver_win32')

url = 'https://www.nike.com/ca/w/sale-3yaep'
driver.get(url)

#Fem una petició HTTP per a confirmar que la resposta és de tipus 2XX
page = requests.get(url)
print(page)

#apreta el botó d'acceptar cookies per a poder fer scroll a la pàgina
button = driver.find_element(By.XPATH, '//*[@id="gen-nav-commerce-header-v2"]/div[1]/div/div[2]/div/div[2]/div[2]/button').click()


#Va fent scroll a la pàgina fins que arriba al final
last_height = driver.execute_script('return document.body.scrollHeight')
while True:
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(3)
    new_height = driver.execute_script('return document.body.scrollHeight')
    if new_height == last_height:
        break
    last_height = new_height

#Importa el HTML de la pàgina a python  
soup = BeautifulSoup(driver.page_source, 'lxml')

#agafa el HTML de cada producte
product_card = soup.find_all('div', class_ = 'product-card__body')

#Genera un dataframe
df = pd.DataFrame({'Link':[''], 'Nom':[''], 'Detalls':[''], 'Colors':[''], 'Descompte':['']})

#Agafa els detalls de cada producte a la pàgina i ho afegeix com a files al dataframe
for product in product_card:
    try:
        link = product.find('a', class_ = 'product-card__link-overlay').get('href')
        nom_producte = product.find('div', class_ = 'product-card__title').text
        quantitat_colors = product.find('div', class_ = 'product-card__count-item').text
        detalls = product.find('div', class_ = 'product-card__subtitle').text
        descompte = product.find('div', class_ = 'product-price__perc css-1qwsg2u').text
        df = df.append({'Link':link, 'Nom':nom_producte, 'Detalls':detalls, 'Colors':quantitat_colors,'Descompte':descompte},
                     ignore_index = True)
    except:
        pass

#exporta el dataframe com a .csv
df.to_csv('C:/Users/marcc/Desktop/UOC/TIPOLOGIA I CICLE DE VIDA/PRA1.csv')



