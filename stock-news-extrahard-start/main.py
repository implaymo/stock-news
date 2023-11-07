import requests
from dotenv import load_dotenv
import os
import random
from twilio.rest import Client


def configure():
    load_dotenv()


configure()

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
API_KEY_STOCK = os.getenv("API_KEY_STOCK")
MY_PHONE = os.getenv("MY_PHONE")
API_KEY_NEWS = os.getenv("API_KEY_NEWS")
account_sid = os.getenv("account_sid")
auth_token = os.getenv("auth_token")
twilio_num = os.getenv("twilio_num")
my_number = os.getenv("my_number")

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "TSLA",
    "apikey": API_KEY_STOCK
}
response_stock = requests.get("https://www.alphavantage.co/query", params=parameters)
response_stock.raise_for_status()
data = response_stock.json()

news_params = {
    "q": "Tesla",
    "apiKey": API_KEY_NEWS
}

response_news = requests.get("https://newsapi.org/v2/everything", params=news_params)
response_news.raise_for_status()

data_news = response_news.json()

all_news = []
for i in range(3):
    news = data_news["articles"][i]
    news_title = news["title"]
    news_description = news["description"]
    news_tuple = (news_title, news_description)
    all_news.append(news_tuple)


def send_message(stock_percentage, headline, brief):
    client = Client(account_sid, auth_token)
    message_body = f"{stock_percentage}\n{headline}\n{brief}"
    message = client.messages \
        .create(
        body=message_body,
        from_=twilio_num,
        to=my_number
    )
    print(message.status)


def stock_messages(percentage, tuple_list):
    for tuple_list in all_news:
        headline = f"Headline: {tuple_list[0]}"
        brief = f"Brief: {tuple_list[1]}"
        send_message(stock_percentage, headline, brief)


# Gets markets dates to compare
last_market_date = list(data["Time Series (Daily)"].keys())[0]
day_before_last_marked_day = list(data["Time Series (Daily)"].keys())[1]
# Gets open days from markets dates
last_day_close_value = float(data["Time Series (Daily)"][last_market_date]["4. close"].strip("'"))
day_before_last_day_close_value = float(data["Time Series (Daily)"][day_before_last_marked_day]["4. close"].strip("'"))

# Compares the difference between last day and previous day
percentage_difference = round(((last_day_close_value - day_before_last_day_close_value) / last_day_close_value) * 100,
                              2)
if percentage_difference > 0:
    stock_percentage = f"Tesla: 🔺{percentage_difference}%"
    stock_messages(stock_percentage, all_news)

else:
    stock_percentage = f"Tesla: 🔻{percentage_difference}%"
    stock_messages(stock_percentage, all_news)
