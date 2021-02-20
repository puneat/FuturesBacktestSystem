from pyalgotrade.barfeed.csvfeed import GenericBarFeed
from pyalgotrade.bar import Frequency
from pyalgotrade import strategy
from pyalgotrade.technical import ma
from pyalgotrade.technical import rsi
from pyalgotrade.technical import cross
from pyalgotrade.technical.bollinger import BollingerBands
from pyalgotrade.technical.macd import MACD
from pyalgotrade.technical.stoch import StochasticOscillator
from pyalgotrade.broker.backtesting import Broker
from pyalgotrade.technical.vwap import VWAP
from pyalgotrade import plotter
from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade.stratanalyzer import returns
from pyalgotrade import broker as basebroker

class BB_SO_RSI_strategy():
    def __init__(self, #fixed
               priceDS, #fixed
               priceBarDS,  #fixed
               bBandsPeriod = 22, #custom
               numStdDev = 3, #custom
               rsiPeriod = 14, #custom
               soPeriod = 14,
               soDPeriod = 3,
               overBoughtThreshold = 80, #custom
               overSoldThreshold = 20): #custom
    # prices
        self.priceDS = priceDS
        self.priceBarDS = priceBarDS

        #indicators to use
        self.rsi = rsi.RSI(self.priceDS, rsiPeriod)
        self.bbands = BollingerBands(self.priceDS, bBandsPeriod, numStdDev)
        self.so = StochasticOscillator(self.priceBarDS, soPeriod, soDPeriod)
        self.overBoughtThreshold = overBoughtThreshold
        self.overSoldThreshold = overSoldThreshold
        
        self.controlSignal_1 = self.so.getD()
        self.controlSignal_2 = self.rsi
        self.ControlSignals = [ self.controlSignal_1, self.controlSignal_2 ]


    def enterLongSignal(self):
        longEntryFilter_1 = cross.cross_below(self.priceDS, self.bbands.getLowerBand()) > 0
        longEntryFilter_2 = self.rsi[-1] <= self.overSoldThreshold
        longEntryFilter_3 = self.so.getD()[-1] <= self.overSoldThreshold
        return longEntryFilter_1 and longEntryFilter_2 and longEntryFilter_3

    def exitLongSignal(self, longPos):
        longExitFilter_1 = cross.cross_above(self.priceDS, self.bbands.getMiddleBand()) > 0
        longExitFilter_2 = longPos.exitActive()
        return longExitFilter_1 and not longExitFilter_2

    def enterShortSignal(self):
        shortEntryFilter_1 = cross.cross_above(self.priceDS, self.bbands.getUpperBand()) > 0
        shortEntryFilter_2 = self.rsi[-1] >= self.overBoughtThreshold
        shortEntryFilter_3 = self.so.getD()[-1] >= self.overBoughtThreshold
        return shortEntryFilter_1 and shortEntryFilter_2 and shortEntryFilter_3

    def exitShortSignal(self, shortPos):
        shortExitFilter_1 = cross.cross_below(self.priceDS, self.bbands.getMiddleBand()) > 0
        shortExitFilter_2 = shortPos.exitActive()
        return shortExitFilter_1 and not shortExitFilter_2
