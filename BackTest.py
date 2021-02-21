from pyalgotrade.broker.backtesting import Broker
from pyalgotrade.barfeed.csvfeed import GenericBarFeed
from pyalgotrade.bar import Frequency
from pyalgotrade import strategy
from pyalgotrade import plotter
from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade.stratanalyzer import returns
from pyalgotrade import broker as basebroker

class BacktestSystem(strategy.BacktestingStrategy):
    def __init__(self,
                 feed,
                 instrument,
                 strategyClass,
                 payupTicks = 1,
                 stopLossTicks=8,
                 tickValue = 0.25,
                 startingMoney = 100000, # in cents
                 GTC = False,
                 AON = False,
                 lotSize = 1,
                 printOrders = True
                 ):
        super(BacktestSystem, self).__init__(feed, startingMoney)

        # strategy params
        self.__instrument = instrument
        self.GTC = GTC
        self.AON = AON
        self.lotSize = lotSize
        self.stopLossTicks = stopLossTicks
        self.payupTicks = payupTicks
        self.tickValue = tickValue
        self.startingMoney = startingMoney
        self.strategyClass = strategyClass
        self.printOrders = printOrders

        #position params
        self.__longPos = None
        self.__shortPos = None

    def onEnterCanceled(self, position):
        if self.__longPos == position:
            self.__longPos = None
        elif self.__shortPos == position:
            self.__shortPos = None
        else:
            assert(False)

    def onExitOk(self, position):
        if self.__longPos == position:
            self.__longPos = None
        elif self.__shortPos == position:
            self.__shortPos = None
        else:
            assert(False)

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        position.exitMarket()

    def onOrderUpdated(self, order):
        if self.printOrders:
            action = order.getAction()
            price = order.getAvgFillPrice()
            qty = order.getFilled()

            if action==1:
                orderType = 'Long Position Entry'
            elif action==2:
                orderType = 'Short Position Exit'
            elif action==3:
                orderType = 'Long Position Exit'
            elif action==4:
                orderType = 'Short Position Entry'

            execInfo = order.getExecutionInfo()
            if price is None:
                self.info("%s order %d updated - %s Status" %
                          (orderType,
                          order.getId(),
                          basebroker.Order.State.toString(order.getState())
                          ))
            else:
                self.info("%s order %d updated - Status: %s - %d lots at Price: \u00a2 %.2f" %
                          (orderType,
                          order.getId(),
                          basebroker.Order.State.toString(order.getState()),
                          qty,
                          price
                          ))
        else:
          pass
        
    def onBars(self, bars):
        # Wait for enough bars to be available to calculate SMA and RSI.
        for signal in self.strategyClass.ControlSignals:
            if signal[-1] is None:
                return

        bar = bars[self.__instrument]
        closeDs = self.getFeed().getDataSeries(self.__instrument).getCloseDataSeries()
        barDs = self.getFeed().getDataSeries(self.__instrument)

        if self.__longPos is not None:
            if self.strategyClass.exitLongSignal(self.__longPos, barDs, closeDs):
                self.__longPos.exitMarket()

        elif self.__shortPos is not None:
            if self.strategyClass.exitShortSignal(self.__shortPos, barDs, closeDs):
                self.__shortPos.exitMarket()

        else:
            if self.strategyClass.enterLongSignal(barDs, closeDs):
                self.__longPos = self.enterLongStopLimit(self.__instrument,
                                                         bar.getClose() - (self.tickValue*self.stopLossTicks) - (self.tickValue*self.payupTicks),
                                                         bar.getClose() - (self.tickValue*self.payupTicks),
                                                         self.lotSize,
                                                         goodTillCanceled = self.GTC,
                                                         allOrNone = self.AON)
                
            elif self.strategyClass.enterShortSignal(barDs, closeDs):
                self.__shortPos = self.enterShortStopLimit(self.__instrument,
                                                           bar.getClose() + (self.tickValue*self.stopLossTicks) + (self.tickValue*self.payupTicks),
                                                           bar.getClose() + (self.tickValue*self.payupTicks),
                                                           self.lotSize,
                                                           goodTillCanceled = self.GTC,
                                                           allOrNone = self.AON)
