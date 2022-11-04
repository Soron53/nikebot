from os import urandom
import tarfile
from bs4 import BeautifulSoup
from pyrsistent import m
from regex import P
import requests;
import re;
import twitter;
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from numpy import size
import requests, json

class NikeScraper():
    def __init__(self, url):
        self.url = url
        self.data = self.get_data()
        products: dict = self.data['props']['pageProps']['initialState']['Threads']['products']
        self.serial_numbers = list(products.keys())

    def get_data(self) -> json:
        r = requests.get(self.url)
        content = r.text
        data = '{"props' + content.split('props')[1].split('"customServer":')[0] + '"customServer":true}'
        return json.loads(data)

    def get_products_data(self) -> json:
        return self.data['props']['pageProps']['initialState']['Threads']['products']

    def get_product_data(self, serial_number) -> json:
        if serial_number in self.serial_numbers:
            return self.get_products_data()[serial_number]
        else:
            return None

    def get_product_name(self, serial_number) -> str:
        if serial_number in self.serial_numbers:
            return self.get_product_data(serial_number)['fullTitle']
        else:
            return None

    def get_products_name(self) -> list:
        names = {}
        for serial_number in self.serial_numbers:
            names[serial_number] = self.get_product_name(serial_number)
        return names
    
    def get_product_price(self, serial_number) -> float:
        if serial_number in self.serial_numbers:
            return self.get_product_data(serial_number)['currentPrice']
        else:
            return None

    def get_product_skus(self, serial_number) -> list:
        return self.get_product_data(serial_number)['skus']
    
    def get_products_skus(self) -> list:
        skus = {}
        for serial_number in self.serial_numbers:
            skus[serial_number] = self.get_product_skus(serial_number)
        return skus

    def get_product_image(self, serial_number) -> str:
        if serial_number in self.serial_numbers:
            return self.get_product_data(serial_number)['nodes'][0]['nodes'][0]['properties']['squarishURL']
        else:
            return None
    
    def get_product_color(self, serial_number) -> str:
        if serial_number in self.serial_numbers:
            return self.get_product_data(serial_number)['colorDescription']
        else:
            return None

    def get_products_color(self) -> list:
        colors = {}
        for serial_number in self.serial_numbers:
            colors[serial_number] = self.get_product_color(serial_number)
        return colors

    def get_product_sizes_disponibility(self, serial_number) -> list:
        serial_number = 'CW2288-111'
        skus = self.get_product_skus(serial_number)
        sizes = {}
        taille = [] 
        sizes['sizes'] = {}
        for sku in skus:
            result = requests.get("https://api.nike.com/deliver/available_skus/v1/{}".format(sku['skuId']))
            if result.status_code == 200:
                formatted_sku = {}
                formatted_sku['size'] = sku['localizedSize']
                formatted_sku['availability'] = {}
                formatted_sku['availability']['state'] = result.json()['available']
                formatted_sku['availability']['level'] = result.json()['level']
                sizes[str(formatted_sku['size'])] =  formatted_sku['availability']['state']
                if formatted_sku['availability']['state'] == True: 
                    taille.append(formatted_sku['size'])        
        #print(taille)
        return taille

        
    
    def get_products_sizes_disponibility(self) -> list:
        sizes = {}
        for serial_number in self.serial_numbers:
            sizes = self.get_product_sizes_disponibility(serial_number)
            print(sizes)
        return sizes
    
    def r_the_twitte(self,listechaus,newchauss):
            taille = listechaus
            taille = str(taille)
            taille = taille.replace("[", "")
            taille = taille.replace("]", "")
            taille = taille.replace("'", "")
            taille = taille.replace(",", " ")
            print(taille)
            print("Stock disponible sur le site Nike : " + taille)
            newchauss = str(newchauss)
            newchauss = newchauss.replace("[", "")
            newchauss = newchauss.replace("]", "")
            newchauss = newchauss.replace("'", "")
            newchauss = newchauss.replace(",", " ")
            print("Nouvelle taille disponible : " + newchauss)
            nike.postStatus("Nike Air Force 1\nStock disponible sur le site Nike : " + taille + "\nNouvelle taille disponible : " + newchauss + " https://www.nike.com/fr/t/chaussure-air-force-1-07-pour-GjGXSP/CW2288-111")
            return taille
    
    def new_stock(sef,oldstock,listechaus):
        if  listechaus == oldstock:
            print("Pas de nouveauté")
            return oldstock
        else:
            newchauss = []
            for i in listechaus:
                if i not in oldstock:
                    newchauss.append(i)
            oldstock = listechaus
            nike.r_the_twitte(listechaus,newchauss)
            return oldstock

    def postStatus(self ,Update):
            status = api.PostUpdate(Update)
            print(status)

if __name__ == "__main__":
    api = twitter.Api(consumer_key='NgcuDGyLpfsGWrkpF6vMCTRgv',
                    consumer_secret='mtdA56faYK1qmUW7S5vmhhXXhwUCfmxGfKSqVQSlrKK2HyjOWt',
                    access_token_key='1583145793317486613-w8Ck5OBRQau73lFpM36YbP40uj8ici',
                    access_token_secret='uR5XFThdY3UyzxJCROkacKYTgQwJQtKDlHs0OIKAu3b4E')
    nike = NikeScraper("https://www.nike.com/fr/t/chaussure-air-force-1-07-pour-GjGXSP/CW2288-111")
    oldstock = []
    i = 0
    while i < 100:
        listechaus = nike.get_products_sizes_disponibility()
        print(oldstock)
        oldstock = nike.new_stock(oldstock,listechaus)
        sleep(10800)
        

   
    

    

