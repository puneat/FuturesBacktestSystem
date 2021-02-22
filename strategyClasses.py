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
import talib
from talib import MA_Type
from pyalgotrade.talibext import indicator



class BO_RSI_SO_talib():
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
        self.numStdDev = numStdDev
        self.bBandsPeriod = bBandsPeriod
        self.rsiPeriod = rsiPeriod
        self.soPeriod = soPeriod
        self.soDPeriod = soDPeriod



        #indicators to use
        self.overBoughtThreshold = overBoughtThreshold
        self.overSoldThreshold = overSoldThreshold

    def enterLongSignal(self, extPriceBarDS, extPriceDS):
        upper, middle, lower = indicator.BBANDS(extPriceDS,
                                                count = 100,
                                                timeperiod = self.bBandsPeriod,
                                                matype = MA_Type.SMA,
                                                nbdevup = self.numStdDev,
                                                nbdevdn = self.numStdDev)
        fastk, fastd = indicator.STOCHF(extPriceBarDS,
                                        count=100,
                                        fastk_period = self.soPeriod,
                                        fastd_period = self.soDPeriod,
                                        fastd_matype = MA_Type.SMA)
        
        rsi = indicator.RSI(extPriceDS,
                            count = 100,
                            timeperiod = self.rsiPeriod)

        longEntryFilter_1 = rsi[-1] <= self.overSoldThreshold
        longEntryFilter_2 = fastd[-1] <= self.overSoldThreshold
        longEntryFilter_3 = cross.cross_below(extPriceDS, lower) > 0
        return longEntryFilter_1 and longEntryFilter_2 and longEntryFilter_3

    def exitLongSignal(self, longPos, extPriceBarDS, extPriceDS):
        upper, middle, lower = indicator.BBANDS(extPriceDS,
                                                count = 100,
                                                timeperiod = self.bBandsPeriod,
                                                matype = MA_Type.SMA,
                                                nbdevup = self.numStdDev,
                                                nbdevdn = self.numStdDev)

        longExitFilter_1 = cross.cross_above(extPriceDS, middle) > 0
        longExitFilter_2 = longPos.exitActive()
        return longExitFilter_1 and not longExitFilter_2

    def enterShortSignal(self,extPriceBarDS, extPriceDS):
        upper, middle, lower = indicator.BBANDS(extPriceDS,
                                                count = 100,
                                                timeperiod = self.bBandsPeriod,
                                                matype = MA_Type.SMA,
                                                nbdevup = self.numStdDev,
                                                nbdevdn = self.numStdDev)
        
        fastk, fastd = indicator.STOCHF(extPriceBarDS,
                                        count=100,
                                        fastk_period = self.soPeriod,
                                        fastd_period = self.soDPeriod,
                                        fastd_matype = MA_Type.SMA)
        
        rsi = indicator.RSI(extPriceDS,
                            count = 100,
                            timeperiod = self.rsiPeriod)

        shortEntryFilter_1 = rsi[-1] >= self.overBoughtThreshold
        shortEntryFilter_2 = fastd[-1] >= self.overBoughtThreshold
        shortEntryFilter_3 = cross.cross_above(extPriceDS, upper) > 0
        return shortEntryFilter_1 and shortEntryFilter_2 and shortEntryFilter_3

    def exitShortSignal(self, shortPos, extPriceBarDS, extPriceDS):
        upper, middle, lower = indicator.BBANDS(extPriceDS,
                                                count = 100,
                                                timeperiod = self.bBandsPeriod,
                                                matype = MA_Type.SMA,
                                                nbdevup = self.numStdDev,
                                                nbdevdn = self.numStdDev)

        shortExitFilter_1 = cross.cross_below(extPriceDS, middle) > 0
        shortExitFilter_2 = shortPos.exitActive()
        return shortExitFilter_1 and not shortExitFilter_2

    
    
class HAMMER_HANGMAN_talib():
    def __init__(self, #fixed
               priceDS, #fixed
               priceBarDS,  #fixed
               bBandsPeriod = 22, #custom
               numStdDev = 3): #custom
    # prices
        self.priceDS = priceDS
        self.priceBarDS = priceBarDS
        self.numStdDev = numStdDev
        self.bBandsPeriod = bBandsPeriod

    def enterLongSignal(self, extPriceBarDS, extPriceDS):
        longEntryFilter_1 = indicator.CDLHAMMER(extPriceBarDS, count=100)
        return longEntryFilter_1[-1]==100

    def exitLongSignal(self, longPos, extPriceBarDS, extPriceDS):
        upper, middle, lower = indicator.BBANDS(extPriceDS,
                                                count = 100,
                                                timeperiod = self.bBandsPeriod,
                                                matype = MA_Type.SMA,
                                                nbdevup = self.numStdDev,
                                                nbdevdn = self.numStdDev)
        
        longExitFilter_1 = cross.cross_above(extPriceDS, middle) > 0
        longExitFilter_2 = longPos.exitActive()
        return longExitFilter_1 and not longExitFilter_2

    def enterShortSignal(self,extPriceBarDS, extPriceDS):
        shortEntryFilter_1 = indicator.CDLHANGINGMAN(extPriceBarDS, count=100)
        return shortEntryFilter_1[-1]==-100

    def exitShortSignal(self, shortPos, extPriceBarDS, extPriceDS):
        upper, middle, lower = indicator.BBANDS(extPriceDS,
                                                count = 100,
                                                timeperiod = self.bBandsPeriod,
                                                matype = MA_Type.SMA,
                                                nbdevup = self.numStdDev,
                                                nbdevdn = self.numStdDev)
        
        shortExitFilter_1 = cross.cross_below(extPriceDS, middle) > 0
        shortExitFilter_2 = shortPos.exitActive()
        return shortExitFilter_1 and not shortExitFilter_2
