import xlwings
import xlwings as xw
import numpy as np
import asyncio
from FPaths import EXCEL_PATH, BINANCELOG
import time
import ccxt.async as ccxt
from time import gmtime, strftime
import logging, sys


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


async def getexchanges():
    ex = ccxt.binance()
    ob0 = await ex.fetch_order_book('LTC/ETH')
    ob1 = await ex.fetch_order_book('OMG/ETH')
    ob2 = await ex.fetch_order_book('QTUM/ETH')
    ob3 = await ex.fetch_order_book('XRP/ETH')
    ob4 = await ex.fetch_order_book('BCH/ETH')
    ob5 = await ex.fetch_order_book('ETH/BTC')
    ob6 = await ex.fetch_order_book('LTC/BTC')
    ob7 = await ex.fetch_order_book('OMG/BTC')
    ob8 = await ex.fetch_order_book('QTUM/BTC')
    ob9 = await ex.fetch_order_book('XRP/BTC')
    ob10 = await ex.fetch_order_book('BCH/BTC')

    return (ob0, ob1, ob2, ob3, ob4, ob5, ob6, ob7, ob8, ob9, ob10)


def fillvals(ob0, ob1, ob2, ob3, ob4, ob5, ob6, ob7, ob8, ob9, ob10):

    try:
        b0 = np.array(ob0['bids'])
        sht['b6'].value = b0
        sht.range('d6').value = np.array(ob0['asks'])

        sht['f6'].value = np.array(ob1['bids'])
        sht.range('h6').value = np.array(ob1['asks'])

        b2 = np.array(ob2['bids'])
        sht['j6'].value = b2
        sht.range('l6').value = np.array(ob2['asks'])

        b3 = np.array(ob3['bids'])
        sht['n6'].value = b3
        sht.range('p6').value = np.array(ob3['asks'])

        b4 = np.array(ob4['bids'])
        sht['r6'].value = b4
        sht.range('t6').value = np.array(ob4['asks'])

        b5 = np.array(ob5['bids'])
        sht['v6'].value = b5
        sht.range('x6').value = np.array(ob5['asks'])

        b6 = np.array(ob6['bids'])
        sht['z6'].value = b6
        sht.range('ab6').value = np.array(ob6['asks'])

        b7 = np.array(ob7['bids'])
        sht['ad6'].value = b7
        sht.range('af6').value = np.array(ob7['asks'])

        b8 = np.array(ob8['bids'])
        sht['ah6'].value = b8
        sht.range('aj6').value = np.array(ob8['asks'])

        b9 = np.array(ob9['bids'])
        sht['al6'].value = b9
        sht.range('an6').value = np.array(ob9['asks'])

        b10 = np.array(ob10['bids'])
        sht['ap6'].value = b10
        sht.range('ar6').value = np.array(ob10['asks'])

        return True
    except BaseException as e:
        print ("Error in filling excel value for binance:%s" % e)
        return False


def fillexcel():

    (ob0, ob1, ob2, ob3, ob4, ob5, ob6, ob7, ob8, ob9,
     ob10) = asyncio.get_event_loop().run_until_complete(getexchanges())

    tries = 0
    while tries < 5:

        flg = fillvals(ob0, ob1, ob2, ob3, ob4, ob5, ob6, ob7, ob8, ob9, ob10)
        if flg:
            break
        else:
            time.sleep(3)
            tries += 1
        if tries == 5:
            print(" Failed to update excel for binance after 5 tries")


if __name__ == "__main__":
    stdout_logger = logging.getLogger('STDOUT')
    sl = StreamToLogger(stdout_logger, logging.INFO)
    sys.stdout = sl

    stderr_logger = logging.getLogger('STDERR')
    sl = StreamToLogger(stderr_logger, logging.ERROR)
    sys.stderr = sl
    wb = xw.Book(EXCEL_PATH)
    sht = wb.sheets['Binance - Orderbook']
    while True:
        try:
            print("Binance Orderbook processing at %s" %
                  strftime("%Y-%m-%d %H:%M:%S", gmtime()))
            fillexcel()
            time.sleep(2)
        except BaseException as e:
            print(e)
