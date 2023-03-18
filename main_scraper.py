from bs4 import BeautifulSoup
import requests
import datetime
import csv
import telegram
import time
import pyshorteners

# Insert the telegram bot token
TOKEN = 'TOKEN BOT TELEGRAM'

# Insert name channel with @
CHAT_ID = '@name-channel'

# Insert Name Amazon Affiliate
AMAZON_AFFILIATE_CODE = 'YOUR-AFFILIATE-NAME'

# Insert product to find
search_term = 'PRODUTC TO FIND'

URL = f'https://www.amazon.it/s?k={search_term}&tag={AMAZON_AFFILIATE_CODE}'
HEADERS = ({
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 44.0.2403.157 Safari / 537.36',
    'Accept-Language': 'en-US, en;q=0.5'})

webpage = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(webpage.content, "lxml")

# Find the first 10 products in the search results
search_results = soup.find_all('div', {'data-component-type': 's-search-result'})[:10]

# Set to store the links of already found products
found_links = set()

# Initialize the Telegram bot object
bot = telegram.Bot(TOKEN)

# Initialize the shortener object
shortener = pyshorteners.Shortener()

for product in search_results:
    # Get the product URL
    product_link = 'https://www.amazon.it' + product.find('a', {'class': 'a-link-normal'}).get('href') + '&tag=pakyita0c-21'

    # If the product has already been found, skip it
    if product_link in found_links:
        continue
    else:
        found_links.add(product_link)

    # Get product data
    webpage = requests.get(product_link, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "lxml")

    product_title_element = soup.find("span", attrs={"id": 'productTitle'})
    product_title = product_title_element.string.strip().replace(',', '') if product_title_element else "NA"

    print(product_title)  # Print the product title to the console

    product_price_element = soup.find("span", attrs={'class': 'a-offscreen'})
    product_price = product_price_element.string.strip() if product_price_element else "NA"

    print(product_price)  # Print te product price on the console

    time_now = datetime.datetime.now().strftime('%d %b, %Y %H:%M:%S')

    # Check if product data is valid and not 'NA'
    if 'NA' not in (product_title, product_price):
        # Accorcia il link del prodotto
        shortened_link = shortener.tinyurl.short(product_link)

        # Add affiliate name with shortlink
        affiliate_link = f'{shortened_link}?tag={AMAZON_AFFILIATE_CODE}'

        # Send short lint to Telegram
        message = f'*PRODOTTO*: {product_title}\n*PREZZO*: {product_price}\n*LINK DI ACQUISTO*: {affiliate_link}'
        bot.send_message(chat_id=CHAT_ID, text=message, parse_mode=telegram.ParseMode.MARKDOWN)

       # Add data to file CSV
    with open('amazon_products.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.datetime.now().strftime("%d-%m-%Y"), datetime.datetime.now().strftime("%H:%M:%S"), product_title, product_price, product_link])

    # Delay the request to avoid IP blocking - it is recommended to set a delay of 30 seconds between each request to avoid getting blocked by Amazon
    time.sleep(30)