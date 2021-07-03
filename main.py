import requests
import os
from twilio.rest import Client

alpha_v_url = "https://www.alphavantage.co/query"
ALPHA_V_KEY = os.environ.get("ALPHA_V_KEY")
print(ALPHA_V_KEY)
news_api_url = "https://newsapi.org/v2/everything"
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
twilio_sid = os.environ.get("TWILIO_SID")
twilio_token = os.environ.get("TWILIO_TOKEN")
twilio_phone = os.environ.get("TWILIO_PHONE")
test_phone = os.environ.get("TEST_PHONE")

stocks_dict = {
    "Tesla": "TSLA",
    "Apple": "AAPL",
    "Disney": "DIS"
}

for (name, symbol) in stocks_dict.items():
    stock_name = name
    stock_symbol = symbol

    alpha_parameters = {
        "function": "TIME_SERIES_DAILY",
        "symbol": stock_symbol,
        "apikey": ALPHA_V_KEY
    }

    news_api_parameters = {
        "q": stock_name,
        "apiKey": NEWS_API_KEY,
        "sortBY": "popularity"
    }


    # Alpha Vantage API
    r_alpha_v = requests.get(alpha_v_url, alpha_parameters)
    r_alpha_v.raise_for_status()
    alpha_v_data = r_alpha_v.json()
    print(alpha_v_data)
    closing_price_list = [float(data['4. close']) for (date, data) in alpha_v_data['Time Series (Daily)'].items()]
    latest_close_price = closing_price_list[0]
    previous_close_price = closing_price_list[1]

    percent_diff = ((latest_close_price - previous_close_price) / previous_close_price) * 100

    up_down_symbol = "🔺"
    if percent_diff < 0:
        up_down_symbol = "🔻"
    print(f"\n{stock_name}: ${latest_close_price} {up_down_symbol}{abs(percent_diff)}% from ${previous_close_price}"
          f"\nTOP 3 ARTICLES:")

    # News API + SMS Send
    r_news = requests.get(news_api_url, news_api_parameters)
    r_news.raise_for_status()
    news_data = r_news.json()['articles']

    for n in range(0, 3):
        title = news_data[n]['title']
        description = news_data[n]['description']
        url = news_data[n]['url']
        print(f"    Title: {title} | Brief: {description}\n | URL: {url}")

        if abs(percent_diff) > 5:
            client = Client(twilio_sid, twilio_token)
            message = client.messages \
                            .create(
                                 body=f"\n\n{stock_symbol}: ${latest_close_price}"
                                      f"{up_down_symbol}{round(abs(percent_diff), 1)}%\n\n"
                                      f"Headline: {title}\n\n"
                                      f"Brief: {description}\n"
                                      f"URL: {url}",
                                 from_=twilio_phone,
                                 to=test_phone
                             )

            print(message.status)
        else:
            print("No SMS sent - stock movement stable.\n")
