from bs4 import BeautifulSoup

import requests

def parse_jumia_name(soup):
    names=soup.find_all('span',class_="name")
    names[:]=[name.get_text() for name in names]
    return names

def parse_image_jumia(soup):
    images = soup.find_all("div", class_="image-wrapper")
    images[:] = [image.img.get('data-src') for image in images]
    return images

def parse_price_jumia(soup):
    prices = soup.find_all("span", class_="price-box ri")
    prices[:] = [price.span.find("span", dir="ltr").get('data-price') for price in prices]
    return prices

def parse_url_jumia(soup):
    urls = soup.find_all("div", class_="sku -gallery")
    urls[:] = [url.a.get('href') for url in urls]
    return urls


def parse_zooba_name(soup):
    names=soup.find_all('div',class_='product details product-item-details box-info')
    names[:]=[name.a.text.strip() for name in names]
    return names

def parse_zooba_image(soup):
    images=soup.find_all('div',class_='product-item-info')
    images[:]=[image.div.div.a.img['src'] for image in images]
    return images

def parse_zooba_prices(soup):
    prices=soup.find_all('div',class_='price-box price-final_price')
    prices[:] = [price.span.find("span", class_="price-wrapper").get('data-price-amount') for price in prices]
    return prices

def parse_zooba_url(soup):
    urls=soup.find_all('div',class_='product details product-item-details box-info')
    urls[:]=[url.a['href'] for url in urls]
    return urls

def parse_superprice_name(soup):
    names=soup.find_all('div',class_='product-info-bottom')
    names[:]=[name.h3.a.text.strip() for name in names]
    return names

def parse_superprice_image(soup):
    images=soup.find_all('span',class_='image0 image-switch')
    images[:]=[image.span.find("span",class_="product-image-wrapper").img['src'].strip() for image in images]
    return images

def parse_superprice_price(soup):
    prices=soup.find_all('div',class_='price-box price-final_price')
    prices[:] = [price.span.find("span", class_="price-wrapper").get('data-price-amount') for price in prices]
    return prices

def parse_superprice_url(soup):
    urls=soup.find_all('div',class_='product-info-bottom')
    urls[:]=[url.h3.a['href'] for url in urls]
    return urls

def parse_melcom_name(soup):
    names=soup.find_all('strong', class_='product name product-item-name')
    names[:]=[name.a.text.strip() for name in names]
    return names

def parse_melcom_image(soup):
    images=soup.find_all('span',class_='product-image-wrapper')
    images[:]=[image.img['src'].strip() for image in images]
    return images

def parse_melcom_url(soup):
    urls=soup.find_all('strong', class_='product name product-item-name')
    urls[:]=[url.a['href'] for url in urls]
    return urls

def parse_melcom_price(soup):
    prices=soup.find_all('div',class_='price-box price-final_price')
    prices[:] = [price.span.find("span", class_="price-wrapper").get('data-price-amount') for price in prices]
    return prices



