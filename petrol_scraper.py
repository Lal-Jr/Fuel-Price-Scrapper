import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import csv
import numpy as np

URL = "https://www.newsrain.in/petrol-diesel-prices"
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

articles = soup.find_all('article')

place = []
petrolPrice = []
dieselPrice = []

for article in articles:
    state = article.find("div", class_='fuel-title')
    city = state.find("small", class_="center")
    placeName = state.contents[0].strip() + "-" + city.contents[0].strip()
    place.append(placeName)
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
        if productName == "Petrol":
            petrolPrice.append(productPrice)
        else:
            dieselPrice.append(productPrice)

columnName = ["Place", "Petrol_Price", "Diesel_Price"]

df = pd.DataFrame([place, petrolPrice,
                  dieselPrice], index=columnName)
df = df.T
df.to_csv('fuelprice.csv')

# x = []
# y = []

# with open('fuelprice.csv', 'r') as file:
#     plots = csv.reader(file, delimiter=',')

#     for row in plots:
#         x.append(row[1])
#         y.append(row[2])

# plt.bar(x, y, color='g', label="Fuel")
# plt.xlabel('Place')
# plt.ylabel('Price')
# plt.title('Fuel Price Comparison')
# plt.legend()
# plt.show()

index = np.arange(36)
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1])
ax.bar(index, petrolPrice, color='r')
ax.bar(index, dieselPrice, color='b')
ax.set_ylabel('Price')
ax.set_title('Fuel Price Comparison')
ax.set_xticks(index)
ax.set_yticks(np.arange(80, 111, 2))
ax.legend(labels=['Petrol', 'Diesel'])
plt.show()
