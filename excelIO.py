
import xlwings as xw
from CoinDelta import eprint, coindelta
import time
from time import gmtime, strftime

from FPaths import EXCEL_PATH
import sys, logging

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

def fillcoindelta_inrvals(ob, cur):
    wb = xw.Book(EXCEL_PATH)
    sht = wb.sheets['Coindelta - Orderbook']
    try:
        if cur == 'btc':
            sht.range('d6').value = ob['asks']  # btc inr
            sht.range('b6').value = ob['bids']  # btc inr
        elif cur == 'eth':
            sht.range('h6').value = ob['asks']  # btc inr
            sht.range('f6').value = ob['bids']  # btc inr
        elif cur == 'ltc':
            sht.range('j6').value = ob['bids']  # btc inr
            sht.range('l6').value = ob['asks']  # btc inr
        elif cur == 'omg':
            sht.range('n6').value = ob['bids']  # btc inr
            sht.range('p6').value = ob['asks']  # btc inr
        elif cur == 'qtum':
            sht.range('r6').value = ob['bids']  # btc inr
            sht.range('t6').value = ob['asks']  # btc inr
        elif cur == 'xrp':
            sht.range('v6').value = ob['bids']  # btc inr
            sht.range('x6').value = ob['asks']  # btc inr
        elif cur == 'bch':
            sht.range('z6').value = ob['bids']  # btc inr
            sht.range('ab6').value = ob['asks']  # btc inr
        return True
    except Exception, e:
        eprint("Error in coindelta orderbook excel entry : %s" % e)
        return False


def fillcoindelta_btcvals(ob, cur):
    wb = xw.Book(EXCEL_PATH)
    sht = wb.sheets['Coindelta - Orderbook']
    try:
        if cur == 'eth':
            sht.range('d31').value = ob['asks']  # btc inr
            sht.range('b31').value = ob['bids']  # btc inr
        elif cur == 'ltc':
            sht.range('f31').value = ob['bids']  # btc inr
            sht.range('h31').value = ob['asks']  # btc inr
        elif cur == 'omg':
            sht.range('j31').value = ob['bids']  # btc inr
            sht.range('l31').value = ob['asks']  # btc inr
        elif cur == 'qtum':
            sht.range('n31').value = ob['bids']  # btc inr
            sht.range('p31').value = ob['asks']  # btc inr
        elif cur == 'xrp':
            sht.range('r31').value = ob['bids']  # btc inr
            sht.range('t31').value = ob['asks']  # btc inr

        return True
    except Exception, e:
        eprint("Error in coindelta orderbook excel entry : %s" % e)
        return False


def work1(curlist=['btc', 'eth', 'ltc', 'omg', 'qtum', 'xrp', 'bch']):
    c = coindelta()
    while True:
        print("INR Orderbook processing at %s" %
              strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        for cur in curlist:
            try:
                ob = c.getOrderBook(cur)  # 10 sec inside
                tries = 0
                while tries < 5:
                    
                    exflag = fillcoindelta_inrvals(ob, cur)
                    if exflag:
                        break
                    else:

                        time.sleep(2)
                        tries += 1
                        print("Retrying .. try no : %i" % tries)
                if tries == 5:
                    eprint(" Failed to update excel after 5 tries for %s " % cur)

            except Exception, e:
                eprint("Error occured : %s" % e)


def work2(curlist=['eth', 'ltc', 'omg', 'qtum', 'xrp']):
    c = coindelta(1)  # btc market
    while True:
        print("BTC Orderbook processing at %s" %
              strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        for cur in curlist:
            try:
                ob = c.getOrderBook(cur)  # 10 sec inside
                tries = 0
                while tries < 5:
                    print("Retrying .. try no : %i" % tries)
                    exflag = fillcoindelta_btcvals(ob, cur)
                    if exflag:
                        break
                    else:
                        time.sleep(2)
                        tries += 1
                if tries == 5:
                    eprint(" Failed to update excel after 5 tries for %s " % cur)

            except Exception, e:
                eprint("Error occured : %s" % e)
