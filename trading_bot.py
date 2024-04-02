from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies import Strategy
from lumibot.traders import Trader
from alpaca_trade_api import REST
from timedelta import Timedelta

from datetime import datetime

from sentiment_analysis import get_news_sentiment

from strategies import one_buy_strategy,buy_sell_sentiment_strategy,short_long_sentiment_strategy

API_KEY="" #Your Alpaca api key
API_SECRET ="" #your api secret
BASE_URL = "https://paper-api.alpaca.markets/v2"

ALPACA_CREDS ={
    "API_KEY":API_KEY,
    "API_SECRET":API_SECRET,
    "PAPER":True
}

class MLTrader(Strategy):
    def initialize(self,symbol:str="SPY",cash_at_risk:float=0.5):
        self.symbol = symbol
        self.sleeptime ="24H"
        self.last_trade = None
        self.cash_at_risk = cash_at_risk
        self.quantity_long = 0
        self.quantity_short = 0
        self.api = REST(key_id= API_KEY, secret_key= API_SECRET, base_url=BASE_URL)

    def position_sizing(self):
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)
        quantity = round(cash*self.cash_at_risk / last_price,0)
        return cash,last_price,quantity

    def get_dates(self):
        today= self.get_datetime()
        days_prior = today - Timedelta(days = 5) 
        return today.strftime("%Y-%m-%d"),days_prior.strftime("%Y-%m-%d")


    def get_sentiment_news(self):
        today,days_prior = self.get_dates()
        news = self.api.get_news(symbol=self.symbol,
                                 start=days_prior,
                                 end=today)

        news = [new.__dict__["_raw"]["headline"] for new in news]

        probability, sentiment = get_news_sentiment(news)
        return probability, sentiment
        

    def on_trading_iteration(self):
        cash,last_price,quantity = self.position_sizing()
        probability, sentiment = self.get_sentiment_news()

        buy_sell_sentiment_strategy(self,cash,last_price,quantity,probability,sentiment)

        short_long_sentiment_strategy(self,cash,last_price,quantity,probability,sentiment)


start_date = datetime(2020,1,1)
end_date = datetime(2023,12,31)
broker = Alpaca(ALPACA_CREDS)


strategy = MLTrader(name="mlstrat",broker=broker,
                    parameters={"symbol":"SPY","cash_at_risk":0.5})
strategy.backtest(YahooDataBacktesting,start_date,end_date,
                  parameters={"symbol":"SPY","cash_at_risk":0.5})

# trader = Trader()
# trader.add_strategy(strategy)
# trader.run_all()