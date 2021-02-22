import pandas as pd
import numpy as np
from pandas import datetime
import matplotlib.pyplot as plt
from datetime import datetime

def process_data(path, saveName, getReturn=False):
    # path = self.interval + '/' + self.product + name + '.csv'
    df = pd.read_csv(path)
    df.rename(columns={'Last': 'Close','Timestamp':'Date Time'}, inplace=True)
    df['Adj Close']=df['Close']
    df.drop(labels='Unnamed: 0', axis=1,inplace=True)
    df['Date Time'] = pd.to_datetime(df['Date Time'], infer_datetime_format= True)
    df.set_index(keys='Date Time',inplace=True)

    save_path = saveName + '.csv'
    df.to_csv(save_path)

    if getReturn:
        return df
    
def metrics(tradesAnalyzer):
  print("")
  print("Total trades: %d" % (tradesAnalyzer.getCount()))
  if tradesAnalyzer.getCount() > 0:
    profits = tradesAnalyzer.getAll()
    print("Avg. profit: $%2.f" % (profits.mean()))
    print("Profits std. dev.: $%2.f" % (profits.std()))
    print("Max. profit: $%2.f" % (profits.max()))
    print("Min. profit: $%2.f" % (profits.min()))
    returns = tradesAnalyzer.getAllReturns()
    print("Avg. return: %2.f %%" % (returns.mean() * 100))
    print("Returns std. dev.: %2.f %%" % (returns.std() * 100))
    print("Max. return: %2.f %%" % (returns.max() * 100))
    print("Min. return: %2.f %%" % (returns.min() * 100))
    
  print("")
  print("Profitable trades: %d" % (tradesAnalyzer.getProfitableCount()))
  if tradesAnalyzer.getProfitableCount() > 0:
    profits = tradesAnalyzer.getProfits()
    print("Avg. profit: $%2.f" % (profits.mean()))
    print("Profits std. dev.: $%2.f" % (profits.std()))
    print("Max. profit: $%2.f" % (profits.max()))
    print("Min. profit: $%2.f" % (profits.min()))
    returns = tradesAnalyzer.getPositiveReturns()
    print("Avg. return: %2.f %%" % (returns.mean() * 100))
    print("Returns std. dev.: %2.f %%" % (returns.std() * 100))
    print("Max. return: %2.f %%" % (returns.max() * 100))
    print("Min. return: %2.f %%" % (returns.min() * 100))
  print("")
  print("Unprofitable trades: %d" % (tradesAnalyzer.getUnprofitableCount()))
  if tradesAnalyzer.getUnprofitableCount() > 0:
    losses = tradesAnalyzer.getLosses()
    print("Avg. loss: $%2.f" % (losses.mean()))
    print("Losses std. dev.: $%2.f" % (losses.std()))
    print("Max. loss: $%2.f" % (losses.min()))
    print("Min. loss: $%2.f" % (losses.max()))
    returns = tradesAnalyzer.getNegativeReturns()
    print("Avg. return: %2.f %%" % (returns.mean() * 100))
    print("Returns std. dev.: %2.f %%" % (returns.std() * 100))
    print("Max. return: %2.f %%" % (returns.max() * 100))
    print("Min. return: %2.f %%" % (returns.min() * 100))
    
# process_data('/gdrive/My Drive/Project/Soy2021/15M/1Sc1.csv', 'ZS_C1_15m')
# process_data('/gdrive/My Drive/Project/Soy2021/15M/1Sc2.csv', 'ZS_C2_15m')
# process_data('/gdrive/My Drive/Project/Soy2021/15M/1Sc3.csv', 'ZS_C3_15m')
# process_data('/gdrive/My Drive/Project/Soy2021/15M/1Sc1-1Sc2.csv', 'ZS_C1C2_15m')
# process_data('/gdrive/My Drive/Project/Soy2021/15M/1Sc2-1Sc3.csv', 'ZS_C2C3_15m')
