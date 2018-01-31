import xlwings
import xlwings as xw
import numpy as np
import asyncio
from FPaths import EXCEL_PATH, BINANCELOG
import time
import ccxt.async as ccxt
from time import gmtime, strftime
import logging
import sys


class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """

    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
    filename=BINANCELOG,
    filemode='a'
)


async def getbinanceob():
    binex = ccxt.binance()
    outdic = dict()
    exlist = ['LTC/ETH', 'OMG/ETH', 'QTUM/ETH', 'XRP/ETH', 'BCH/ETH', 'NEO/ETH', 'ETH/BTC', 'LTC/BTC',
              'OMG/BTC', 'QTUM/BTC', 'XRP/BTC', 'BCH/BTC', 'NEO/BTC', 'GAS/BTC', 'LTC/BNB', 'NEO/BNB']
    for ex in exlist:
        try:
            outdic[ex] = await binex.fetch_order_book(ex)
        except BaseException as e:
            print("Error in fetching binance order book %s: %s" % (ex, e))

    return outdic


async def getkukoin():
    kuex = ccxt.kucoin()
    outdic = dict()
    exlist = ['GAS/NEO', "GAS/BTC", 'NEO/BTC', 'NEO/USDT', 'NEO/ETH',
              'QTUM/NEO',	'QTUM/BTC', 'LTC/NEO', 'LTC/BTC', 'LTC/ETH']  # , 'GAS/USD'

    for ex in exlist:
        try:
            outdic[ex] = await kuex.fetch_order_book(ex)
        except BaseException as e:
            print("Error in fetching kukoin order book %s: %s" % (ex, e))

    return outdic


def fillkuvals(obdict, wb):
    shtkukoin = wb.sheets['Kucoin - Orderbook ']
    _kukoin_sheet = {
        'GAS/NEO': {'bids': shtkukoin.range('b6'), 'asks': shtkukoin.range('d6')},
        'GAS/BTC': {'bids': shtkukoin.range('f6'), 'asks': shtkukoin.range('h6')},
        # 'GAS/USD': {'bids': shtkukoin.range('j6'), 'asks': shtkukoin.range('l6')},
        'NEO/BTC': {'bids': shtkukoin.range('n6'), 'asks': shtkukoin.range('p6')},
        'NEO/USDT': {'bids': shtkukoin.range('r6'), 'asks': shtkukoin.range('t6')},
        'NEO/ETH': {'bids': shtkukoin.range('v6'), 'asks': shtkukoin.range('x6')},
        'QTUM/NEO': {'bids': shtkukoin.range('z6'), 'asks': shtkukoin.range('ab6')},
        'QTUM/BTC': {'bids': shtkukoin.range('ad6'), 'asks': shtkukoin.range('af6')},
        'QTUM/ETH': {'bids': shtkukoin.range('ah6'), 'asks': shtkukoin.range('aj6')},
        'LTC/NEO': {'bids': shtkukoin.range('al6'), 'asks': shtkukoin.range('an6')},
        'LTC/BTC': {'bids': shtkukoin.range('ap6'), 'asks': shtkukoin.range('ar6')},
        'LTC/ETH': {'bids': shtkukoin.range('at6'), 'asks': shtkukoin.range('av6')}
    }
    try:
        for k in _kukoin_sheet:
            if k in obdict:
                _kukoin_sheet[k]['bids'].value = obdict[k]['bids']
                _kukoin_sheet[k]['asks'].value = obdict[k]['asks']

        return True
    except BaseException as e:
        print ("Error in filling excel value for kukoin:%s" % e)
        return False


def fillbinancevals(obdict, wb):
    shtbinance = wb.sheets['Binance - Orderbook']

    _binance_sheet = {
        'LTC/ETH': {'bids': shtbinance.range('b6'),
                    'asks': shtbinance.range('d6')},
        'OMG/ETH':  {'bids': shtbinance.range('f6'),
                     'asks': shtbinance.range('h6')},
        'QTUM/ETH':  {'bids': shtbinance.range('j6'),
                      'asks': shtbinance.range('l6')},
        'XRP/ETH':  {'bids': shtbinance.range('n6'),
                     'asks': shtbinance.range('p6')},
        'BCH/ETH':  {'bids': shtbinance.range('r6'),
                     'asks': shtbinance.range('t6')},
        'NEO/ETH':  {'bids': shtbinance.range('v6'),
                     'asks': shtbinance.range('x6')},
        'ETH/BTC':  {'bids': shtbinance.range('z6'),
                     'asks': shtbinance.range('ab6')},
        'LTC/BTC':  {'bids': shtbinance.range('ad6'),
                     'asks': shtbinance.range('af6')},
        'OMG/BTC':  {'bids': shtbinance.range('ah6'),
                     'asks': shtbinance.range('aj6')},
        'QTUM/BTC':  {'bids': shtbinance.range('al6'),
                      'asks': shtbinance.range('an6')},
        'XRP/BTC': {'bids': shtbinance.range('ap6'),
                    'asks': shtbinance.range('ar6')},
        'BCH/BTC': {'bids': shtbinance.range('at6'),
                    'asks': shtbinance.range('av6')},
        'NEO/BTC': {'bids': shtbinance.range('ax6'),
                    'asks': shtbinance.range('az6')},
        'GAS/BTC': {'bids': shtbinance.range('bb6'),
                    'asks': shtbinance.range('bd6')},
        'LTC/BNB': {'bids': shtbinance.range('bf6'),
                    'asks': shtbinance.range('bh6')},
        'NEO/BNB': {'bids': shtbinance.range('bj6'),
                    'asks': shtbinance.range('bl6')}
    }
    try:
        for k in _binance_sheet:
            _binance_sheet[k]['bids'].value = obdict[k]['bids']
            _binance_sheet[k]['asks'].value = obdict[k]['asks']

        return True
    except BaseException as e:
        print ("Error in filling excel value for binance:%s" % e)
        return False


def fillexcel(wb):
    """FIll excel sheel with exchange order book

    Arguments:
        wb {workbook} -- xlwings workbook object
    """

    obdict = asyncio.get_event_loop().run_until_complete(getbinanceob())

    tries = 0
    while tries < 5:

        flg = fillbinancevals(obdict, wb)
        if flg:
            break
        else:
            time.sleep(3)
            tries += 1
        if tries == 5:
            print(" Failed to update excel for binance after 5 tries")
    kobdict = asyncio.get_event_loop().run_until_complete(getkukoin())
    tries = 0
    while tries < 5:

        flg = fillkuvals(kobdict, wb)
        if flg:
            break
        else:
            time.sleep(3)
            tries += 1
        if tries == 5:
            print(" Failed to update excel for kukoin after 5 tries")


if __name__ == "__main__":
    stdout_logger = logging.getLogger('STDOUT')
    sl = StreamToLogger(stdout_logger, logging.INFO)
    #sys.stdout = sl

    stderr_logger = logging.getLogger('STDERR')
    sl = StreamToLogger(stderr_logger, logging.ERROR)
    #sys.stderr = sl
    wb = xw.Book(EXCEL_PATH)

    while True:
        try:
            print("Binance Orderbook processing at %s" %
                  strftime("%Y-%m-%d %H:%M:%S", gmtime()))
            fillexcel(wb)
            time.sleep(2)
        except BaseException as e:
            print(e)
