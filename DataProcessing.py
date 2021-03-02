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
    
def metrics(tradesAnalyzer, stratObj, sharpeObj, drawdownObj, retObj, printResult=False):

  p_p = tradesAnalyzer.getProfits()
  l_l = tradesAnalyzer.getLosses()
  a_p = tradesAnalyzer.getAll()

  a_r = tradesAnalyzer.getAllReturns()
  p_r = tradesAnalyzer.getPositiveReturns()
  l_r = tradesAnalyzer.getNegativeReturns()

  overall = [tradesAnalyzer.getCount(), tradesAnalyzer.getProfitableCount(), tradesAnalyzer.getUnprofitableCount(),
             (stratObj.getResult()-stratObj.startingMoney)/stratObj.tickValue,
             sharpeObj.getSharpeRatio(0.0002),
             drawdownObj.getMaxDrawDown()*10000,
             tradesAnalyzer.getProfitableCount()/tradesAnalyzer.getCount()*100,
             tradesAnalyzer.getUnprofitableCount()/tradesAnalyzer.getCount()*100,
             a_p.mean()*4, p_p.mean()*4, l_l.mean()*4,
             a_p.std()*4, p_p.std()*4, l_l.std()*4,
             a_p.max()*4, p_p.max()*4, l_l.max()*4,
             a_p.min()*4, p_p.min()*4, l_l.min()*4
             ]
  if printResult:
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
    
  return overall

def cumulativeReturnsPlot(cum_ret):
  price=[]
  for i in range(0, cum_ret.__len__()):
    price.append(cum_ret.__getitem__(i))

  mydict = {'date':cum_ret.getDateTimes(),
            'ret':price}

  mydict = pd.DataFrame(mydict)
  mydict.set_index(keys='date',inplace=True)
  target = mydict.groupby(mydict.index.date).mean()*100000/0.25

  # fig = plt.figure(figsize=[15,6])
  # ax = fig.add_axes([0,0,1,1])
  plt.plot(target)
  plt.xlabel('Time (daily)')
  plt.ylabel('Cumulative Ticks')
  plt.title('Daily Cumulative Returns')
  plt.show()
    
# process_data('/gdrive/My Drive/Project/Soy2021/15M/1Sc1.csv', 'ZS_C1_15m')
# process_data('/gdrive/My Drive/Project/Soy2021/15M/1Sc2.csv', 'ZS_C2_15m')
# process_data('/gdrive/My Drive/Project/Soy2021/15M/1Sc3.csv', 'ZS_C3_15m')
# process_data('/gdrive/My Drive/Project/Soy2021/15M/1Sc1-1Sc2.csv', 'ZS_C1C2_15m')
# process_data('/gdrive/My Drive/Project/Soy2021/15M/1Sc2-1Sc3.csv', 'ZS_C2C3_15m')
