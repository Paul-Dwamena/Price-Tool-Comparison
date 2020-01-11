import os,sys

import requests
import json
import sqlite3
from collections import namedtuple
from re import sub
from bs4 import BeautifulSoup
from flask import Flask, jsonify, render_template, request
from scraper import *
from flask_cors import CORS



app = Flask(__name__,
            static_folder = "./dist",
            template_folder = ".")
CORS(app)

JUMIA_URL = os.getenv('JUMIA_URL', 'https://www.jumia.com.gh/catalog/?q=')
MELCOM_URL = os.getenv('MELCOM_URL', 'https://www.melcomonline.com/catalogsearch/result/?q=')
ZOOBAR_URL = os.getenv('ZOOBAR_URL', 'https://www.zoobashop.com/catalogsearch/result/?cat=&q=')
SUPERPRICE_URL = os.getenv('SUPERPRICE_URL', 'https://www.superprice.com/catalogsearch/result/?q=')
EMPTY_LIST = []

urls = [JUMIA_URL,MELCOM_URL,ZOOBAR_URL,SUPERPRICE_URL]

@app.route('/search/<term>/', methods=['GET'])
def search_products(term=None):
    jumiaurl = JUMIA_URL + sub(r"\s+", '+', str(term))
    melcom_url= MELCOM_URL + sub(r"\s+", '+', str(term))
    zoobarurl = ZOOBAR_URL + str(term)
    superpriceurl= SUPERPRICE_URL + str(term)
    print(jumiaurl)
    results = parse_zoobar(zoobarurl)+parse_jumia(jumiaurl)+parse_melcom(melcom_url)+parse_superprice(superpriceurl)

    return jsonify(results), 200



@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home_page(path):
	return render_template('index.html'),200

def parse_all(soup,STORE):
    titles = parse_titles(soup,STORE)
    images = parse_images(soup,STORE)
    prices = parse_prices(soup,STORE)
    product_urls = parse_product_urls(soup,STORE)
    source = STORE
    search_results = []
    for search_result in zip(titles, images, prices, product_urls):
        search_results.append({
            'title': search_result[0],
            'image': search_result[1],
            'price': search_result[2],
            'url': search_result[3],
            'source': source,
        })
    return search_results


def parse_jumia(url, sort=None):
    '''
    This function parses the page and returns list of products
    '''
    #print(url)
    STORE = "jumia"
    try:
        data = requests.get(url).text
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(e)
        sys.exit(1)
    soup = BeautifulSoup(data, 'lxml')
    #print(soup)
    table_present = soup.find('section', {'class': 'products -mabaya'})
    if table_present is None:
        return EMPTY_LIST
    return parse_all(soup,STORE)

def parse_melcom(url, sort=None):
    '''
    This function parses the page and returns list of products
    '''
    #print(url)
    STORE = "melcom"
    try:
        data = requests.get(url).text
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(e)
        sys.exit(1)
    soup = BeautifulSoup(data, 'lxml')
    #print(soup)
    table_present = soup.find('div', {'class': 'products wrapper single-line-name grid products-grid'})
    if table_present is None:
        return EMPTY_LIST
    return parse_all(soup,STORE)

def parse_zoobar(url, sort=None):
    '''
    This function parses the page and returns list of products
    '''
    #print(url)
    STORE = "zoobar"
    try:
        data = requests.get(url).text
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(e)
        sys.exit(1)
    soup = BeautifulSoup(data, 'lxml')
    #print(soup)
    table_present = soup.find('div', {'class': 'category-product products wrapper grid products-grid'})
    if table_present is None:
        return EMPTY_LIST
    return parse_all(soup,STORE)


def parse_superprice(url, sort=None):
    '''
    This function parses the page and returns list of products
    '''
    #print(url)
    STORE = "superprice"
    data = requests.get(url).text
    soup = BeautifulSoup(data, 'lxml')
    #print(soup)
    table_present = soup.find('ol', {'class': 'product-grid row'})
    if table_present is None:
        return EMPTY_LIST
    return parse_all(soup,STORE)

def parse_titles(soup,STORE):
    switcher = {
        'jumia': parse_jumia_name,
        'melcom': parse_melcom_name,
        'zoobar': parse_zooba_name,
        'superprice': parse_superprice_name
	    
    }
    # Get the function from switcher dictionary
    func = switcher.get(STORE, lambda: "Store is not supported yet")
    # Execute the function
    titles = func(soup)
    return titles



def parse_images(soup,STORE):
    switcher = {
        'jumia': parse_image_jumia,
        'melcom': parse_melcom_image,
        'zoobar': parse_zooba_image,
        'superprice': parse_superprice_image
        
    }
    # Get the function from switcher dictionary
    func = switcher.get(STORE, lambda: "Store is not supported yet")
    # Execute the function
    images = func(soup)
    return images


def parse_prices(soup,STORE):
    switcher = {
        'jumia': parse_price_jumia,
        'melcom': parse_melcom_price,
        'zoobar': parse_zooba_prices,
        'superprice': parse_superprice_price
    }
    # Get the function from switcher dictionary
    func = switcher.get(STORE, lambda: "Store is not supported yet")
    # Execute the function
    images = func(soup)
    return images



def parse_product_urls(soup,STORE):
    switcher = {
        'jumia': parse_url_jumia,
        'melcom': parse_melcom_url,
        'zoobar': parse_zooba_url,
        'superprice': parse_superprice_url
    }
    # Get the function from switcher dictionary
    func = switcher.get(STORE, lambda: "Store is not supported yet")
    # Execute the function
    urls = func(soup)
    return urls




if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
