import requests
from bs4 import BeautifulSoup
import csv

URL = "https://www.newsrain.in/petrol-diesel-prices"
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

articles = soup.find_all('article')

for article in articles:
    state = article.find("div", class_='fuel-title')
    city = state.find("small", class_="center")
    print(state.contents[0].strip() + "-" + city.contents[0].strip())
    fuelcontent = article.find('div', class_="fuel-content")
    products = fuelcontent.find_all("div", {"itemprop": "product"})
    for product in products:
        productName = product.find(
            "h3", {"itemprop": "name"}).contents[0].strip()
        productPrice = product.find(
            "span", class_="price_tag").contents[0].strip()
        productCurrency = product.find(
            "i", {"itemprop": "priceCurrency"})["content"]
        priceChange = product.find(
            "span", class_="changed-price").contents[0].strip()
        increment = product.find("span", class_="increment")
        if increment == None:
            priceChangeSign = "+"
        else:
            priceChangeSign = "-"
        print("  " + productName + " " + productPrice + " " +
              productCurrency + "/ltr" + " " + priceChangeSign+priceChange)
