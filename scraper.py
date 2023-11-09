# Extract the 12 cheapest beers from Bavaria from "www.biermarket.de" and save them in a csv file.
import csv
import requests
from bs4 import BeautifulSoup


def parse_response(parser, beer_data):
    beer_listings = parser.find_all("div", class_="webing-product-name")
    price_info_listings = parser.find_all('div', class_='product-price-info')
    for beer, price_info in zip(beer_listings, price_info_listings):
        beer_name = beer.find('a', class_="product-name").text.strip()
        try:
            price_per_liter = float(price_info.find('span', class_='price-unit-reference').text.strip()[1:].split("\xa0")[0].replace(",","."))
        except: 
            price_per_liter = float("inf")
        try:
            price_per_unit = float(price_info.find('span', class_='product-price').text.strip().split("\xa0")[0].replace(",","."))
        except:
            price_per_unit = float("inf")
        beer_data.append([beer_name, price_per_liter, price_per_unit])


def extract_all_beer_data():
    beer_data = []
    url = 'https://www.biermarket.de/bier/deutsches-bier/bayern/?order=price-asc&p='
    i=0
    while True :
        response = requests.get(url+str(i))
        i=i+1
        parser = BeautifulSoup(response.text, "html.parser")
        if len(parser.find_all("div", class_="webing-product-name"))==0:
            break
        parse_response(parser, beer_data)
    beer_data.sort(key=lambda x: x[1])
    return beer_data[:12]

def extract_cheapest_12_beers():
    beer_data = []
    url = 'https://www.biermarket.de/bier/deutsches-bier/bayern/?order=price-asc&p='
    i=0
    while True :
        # the page already returns 12 cheapest products but check in case they change it and a next page should be parsed
        if len(beer_data)>=12:
            break
        response = requests.get(url+str(i))
        i=i+1
        parser = BeautifulSoup(response.text, "html.parser")
        parse_response(parser, beer_data)
    return beer_data[:12]


def save_csv_files(name, cheapest_beers):
    with open(name, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Beer Name',  'price_per_liter', 'price_per_unit'])
        csv_writer.writerows(cheapest_beers)

if __name__=="__main__":
    beer_data = extract_cheapest_12_beers()
    save_csv_files('cheapest_beers_bavaria_by_price_per_unit.csv', beer_data)

    # this is optional and was not required, I wanted to return 12 cheapest beers by their price per liter
    # for that all beer data need to be extacted not only the first 12
    beer_data = extract_all_beer_data()
    save_csv_files('cheapest_beers_bavaria_by_price_per_liter.csv', beer_data)