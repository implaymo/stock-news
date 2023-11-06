import requests
from dotenv import load_dotenv
import os
import random
from json_data import api_data
from twilio.rest import Client


def configure():
    load_dotenv()

configure()

#####################################################################################################################

# STOCK = "TSLA"
# COMPANY_NAME = "Tesla Inc"
# API_KEY_STOCK = os.getenv("API_KEY_STOCK")
# MY_PHONE = os.getenv("MY_PHONE")
API_KEY_NEWS = os.getenv("API_KEY_NEWS")
account_sid = os.getenv("account_sid")
auth_token = os.getenv("auth_token")
client = Client(account_sid, auth_token)


# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
# parameters= {
#     "function": "TIME_SERIES_DAILY",
#     "symbol": "TSLA",
#     "apikey": API_KEY
# }
# response_stock = requests.get("https://www.alphavantage.co/query", params=parameters)
# response_stock.raise_for_status()
# data = response.json()

##################################################################################################################



## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
parameters_news = {
    "q": "Tesla",
    "apiKey": API_KEY_NEWS
}

response_news = requests.get("https://newsapi.org/v2/everything", params=parameters_news)
response_news.raise_for_status()

data_news = response_news.json()

all_news = []
for i in range(3):
    news = data_news["articles"][i]
    news_title = news["title"]
    news_description = news["description"]
    news_tuple = (news_title, news_description)
    all_news.append(news_tuple)


## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 




########################### API data, because I have reached the max api requests per day ############################################


# Gets markets dates to compare
last_market_date = list(api_data["Time Series (Daily)"].keys())[0]
previous_market_date = list(api_data["Time Series (Daily)"].keys())[1]
# Gets open days from markets dates
last_day_open_data = float(api_data["Time Series (Daily)"][last_market_date]["1. open"].strip("'"))
previous_day_open_data = float(api_data["Time Series (Daily)"][previous_market_date]["1. open"].strip("'"))

# Compares the difference between last day and previous day
percentage_difference = previous_day_open_data * 0.05
difference_values = last_day_open_data - previous_day_open_data
if last_day_open_data > previous_day_open_data:
    print(f"Tesla: 🔺{percentage_difference}%")
    print(f"Headline: {all_news[0][0]}")
    print(f"Brief: {all_news[0][1]}")
else:
    print(f"Tesla: 🔻{percentage_difference}%")
