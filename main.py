from IPython.lib.security import passwd
import datetime as dt
import pandas as pd
import matpotilib.pyplot as plt
from thetadata import ThetaClient, OptionReqType, OptionRight, DateRange

def create_signals(ticker, exp_date, client):
  transactions = {
      "transaction_date": [],
      "tiker": [],
      "strike": [],
      "exp_date": [],
      "transaction_type": []
  }

  strikes = client.get_strikes(ticker, exp_date)
  for strike in strikes: 
    try:
      data = client.get_hist_option(
          req=OptionReqType.EOD,
          root=ticker,
          exp=exp_date,
          strike=strike,
          right=OptionRight.Call,
          date_range=DateRange(exp_date - dt.timedelta(90), exp_date)
      )
      # we download the data
      if len(data) > 10:
        data.columns = ["Open", "High", "Low", "Close", "Volume", "Count", "Date"]
        data.set_index("Date", inplace=True)
        data['Signal'] = data['Volume'] > data['Volume'].mean() + 3 * date ["Volume"].std()
        selected_data = data[data['Signal']]

# if we find trades or days that have volume 3 times the standart deviation 

        for index, rox in selected_data.iterrows():
          transactions['transaction_date'].append(index)
          transactions['ticker'].append(ticker)
          transactions['strike'].append(strike)
          transactions['exp_date'].append(exp_date)
          transactions['transaction_tyte'].append("buy")

# we are gonna print the data in the transactions

# we gonna repeat for put options now

try:
      data = client.get_hist_option(
          req=OptionReqType.EOD,
          root=ticker,
          exp=exp_date,
          strike=strike,
          right=OptionRight.Put,
          date_range=DateRange(exp_date - dt.timedelta(90), exp_date)
      )
      # we download the data
      if len(data) > 10:
        data.columns = ["Open", "High", "Low", "Close", "Volume", "Count", "Date"]
        data.set_index("Date", inplace=True)
        data['Signal'] = data['Volume'] > data['Volume'].mean() + 3 * date ["Volume"].std()
        selected_data = data[data['Signal']]

# if we find trades or days that have volume 3 times the standart deviation 

        for index, rox in selected_data.iterrows():
          transactions['transaction_date'].append(index)
          transactions['ticker'].append(ticker)
          transactions['strike'].append(strike)
          transactions['exp_date'].append(exp_date)
          transactions['transaction_tyte'].append("sell")

# we are gonna print the data in the transactions


pd.DataFrame(transactions).to_csv("transactions.csv")


def backtest(ticker, exp_date, client):
  df = pd.read_csv("transactions.csv")
  df = df.sort_values(by="transactions_date")
  df.set_index("transaction_date", inplace=True)
  df.drop(['Unnamed: 0']), axis=1, inplace=True)

  strikes = sorted(set(df.strike.values))
  total_profit = 0
  for strike in strikes:
     data = client.get_hist_option(
          req=OptionReqType.EOD,
          root=ticker,
          exp=exp_date,
          strike=strike,
          right=OptionRight.Call,
          date_range=DateRange(exp_date - dt.timedelta(90), exp_date)
      )
     
     data.columns = ["Open", "High", "Low", "Close", "Volume", "Count", "Date"]
        data.set_index("Date", inplace=True)
        
        plt.plot(data.index, data.Close)
        buy_data = df[df.transaction_type == "buy"]
        buy_data = buy_data[buy_data.strike == strike]
        filtered_data = data[data.index.isin(buy_data.index)]
        plt.scatter(filtered_data.index, filtered_data.Close, marker="^", color="green")


        plt.plot(data.index, data.Close)
        buy_data = df[df.transaction_type == "sell"]
        buy_data = buy_data[buy_data.strike == strike]
        filtered_data = data[data.index.isin(buy_data.index)]
        plt.scatter(filtered_data.index, filtered_data.Close, marker="v", color="red")

        plt.show()

        amount_owned = 0
        profit = 0

        for idx, row in df[df.strike == strike].interrows()
          if row.transaction_type = "buy":
            amount_owned += 1
            profi -= data[data.index == idx]['Close'].values[0]
          else:
              if amount_owned > 0:
                profit = data[data.index = idx]['Close'].values[0] * amount_owned
                 amount_owned = 0

        profit +=  amount_owned * data.iloc[-1]['Close']
        print(f"profit: {round(profit,2)}")
        total_profit += profit

      print("Total Profit: ", round(total_profit, 2))

client = ThetaClient(username="accounts@email.com", 
                     passwd=open("sec.txt", "r").read())

with client.connect():
  ticker = "BMY"
  exp_dates = client.get_expirations(ticker)

  for exp_date in exp_dates [390:400]
    try 
       create_signals(ticker, exp_date, client)
       backtest(ticker, exp_date, client)
    except:
      continue
