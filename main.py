from info import *
import requests
import smtplib
from twilio.rest import Client
import pandas as pd

pd.options.display.float_format = '{:.5f}'.format

GMAIL_SMTP = "smtp.gmail.com"
STOCK = "DOGE-USD"
COMPANY_NAME = "Dogecoin"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

NEWS_PARAMS = {
    "q": ("DOGE", "+dogecoin"),
    "language": "en",
    "sortBy": "relevancy"
}
STOCK_PARAMS = {
    "function": "DIGITAL_CURRENCY_DAILY",
    "symbol": "DOGE",
    "market": "USD",
    "apikey": STOCK_API_KEY
}
lola = {
    "name": "lola",
    "age": "30"
}

stock_request = requests.get(url=STOCK_ENDPOINT, params=STOCK_PARAMS)
data = stock_request.json()["Time Series (Digital Currency Daily)"]
data_list = [value for (key, value) in data.items()]

yesterday_closing_price = float(data_list[0]["4a. close (USD)"])
day_before_yesterday_closing_price = float(data_list[1]["4a. close (USD)"])
difference = abs((yesterday_closing_price - day_before_yesterday_closing_price))
difference_percentage = (difference / yesterday_closing_price) * 100

headers = {
    "X-Api-Key": NEWS_API_KEY
}
news_items = []


def get_news():
    news_request = requests.get(url=NEWS_ENDPOINT, params=NEWS_PARAMS, headers=headers)
    news_data = news_request.json()
    news_articles = news_data["articles"]
    sliced_news = news_articles[:3]

    for i in range(3):
        title = (sliced_news[i]["title"])
        description = (sliced_news[i]["description"])
        url = (sliced_news[i]["url"])
        news_items.append(f"Title: {title}," + f" Description: {description}," + f" URL: {url}")


def send_email():
    with smtplib.SMTP(GMAIL_SMTP, port=587) as connection:
        connection.starttls()
        connection.login(user=EMAIL_ADD, password=EMAIL_PASS)
        for i in range(3):
            connection.sendmail(
                from_addr=EMAIL_ADD,
                to_addrs=EMAIL_TO,
                msg=f"Subject: DOGECOIN NEWS!\n\nSee below: {news_items[i]}"
            )
        connection.close()


def send_sms():
    client = Client(TWILIO_SID, TWILIO_API_KEY)
    for i in range(3):
        message = client.messages \
            .create(body=f"DOGECOIN NEWS: {news_items[i]}", from_=TWILIO_TRIAL_NUM, to=TWILIO_TO_NUM)

        print(message.sid)


if difference_percentage >= .025:
    get_news()
    send_email()
    send_sms()
