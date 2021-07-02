import requests
from twilio.rest import Client

tesla_symbol = "TSLA"
apple_symbol = "AAPL"

alpha_v_url = "https://www.alphavantage.co/query"
ALPHA_V_KEY = "RXB5X5ZP30LEIHLC"
news_api_url = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "8b8e7106d253444780ad459c18da8e92"
twilio_sid = "ACb39d08fa73108b010c7170ce6892c653"
twilio_token = "e931192b3370831e3d06edf4363f6228"
twilio_phone = "+12514395722"
test_phone = "+61432111467"

alpha_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": tesla_symbol,
    "apikey": ALPHA_V_KEY
}

news_api_parameters = {
    "q": "tesla",
    "apiKey": NEWS_API_KEY
}

r_alpha_v = requests.get(alpha_v_url, alpha_parameters)
r_alpha_v.raise_for_status()
alpha_v_data = r_alpha_v.json()

closing_price_list = [float(data['4. close']) for (date, data) in alpha_v_data['Time Series (Daily)'].items()]
print(closing_price_list[:2])
percent_diff = (abs(closing_price_list[0] - closing_price_list[1]) / closing_price_list[1]) * 100
print(f"{percent_diff}% difference")

# if percent_diff > 5:
#     print("Print News")
#
# else:
#     print("Not significant")

r_news = requests.get(news_api_url, news_api_parameters)
r_news.raise_for_status()
news_data = r_news.json()['articles']

for n in range(0, 3):
    title = news_data[n]['title']
    description = news_data[n]['description']
    url = news_data[n]['url']
    print(title, description, url)

