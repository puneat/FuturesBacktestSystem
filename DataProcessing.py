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
    
# process_data('/gdrive/My Drive/Project/Soy2021/15M/1Sc1.csv', 'ZS_C1_15m')
# process_data('/gdrive/My Drive/Project/Soy2021/15M/1Sc2.csv', 'ZS_C2_15m')
# process_data('/gdrive/My Drive/Project/Soy2021/15M/1Sc3.csv', 'ZS_C3_15m')
# process_data('/gdrive/My Drive/Project/Soy2021/15M/1Sc1-1Sc2.csv', 'ZS_C1C2_15m')
# process_data('/gdrive/My Drive/Project/Soy2021/15M/1Sc2-1Sc3.csv', 'ZS_C2C3_15m')
