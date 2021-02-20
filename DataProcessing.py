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