from __future__ import print_function
from lxml import html
import numpy as np
import pdb
import time
import splinter
import threading

import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
import logging

def pfloat(val):
    
    if "," in val:
        return float(val.replace(',',""))
    else:
        return float(val)
    

class coindelta(object):
    def __init__(self, btcmkt= 0):
        self.browser = splinter.Browser('chrome', headless= False)
        # self.browser.driver.maximize_window()
        self.browser.visit('https://coindelta.com/market?active=BTC-INR')
        self.browser.driver.maximize_window()
        for i in range(8):
            
            print("waiting " + "."*i)
            print("%i sec remaining"%(8 -i))
            time.sleep(1)
        if btcmkt:
            self.mktbtc = True
            self.browser.find_by_xpath('//*[@id="market"]/section/div/div[2]/div[1]/div/div/div[1]/div/ul/li[2]/a').click()
        else:
            self.mktbtc = False
        # time.sleep(10)

    def clickbid2(self):
        el = self.browser.find_by_xpath('//*[@id="market"]/section/div/div[1]/div[4]/div/div/div[1]/footer/ul/li[3]/a')[0]
        if el.text =='2':
            el.click()
    def clickbid1(self):
        el = self.browser.find_by_xpath('//*[@id="market"]/section/div/div[1]/div[4]/div/div/div[1]/footer/ul/li[2]/a')[0]
        if el.text =='1':
            el.click()
    def clickask2(self):
        el = self.browser.find_by_xpath('//*[@id="market"]/section/div/div[1]/div[4]/div/div/div[2]/footer/ul/li[3]/a')[0]
        if el.text =='2':
            el.click()
    def clickask1(self):
        el = self.browser.find_by_xpath('//*[@id="market"]/section/div/div[1]/div[4]/div/div/div[2]/footer/ul/li[2]/a')[0]
        if el.text =='1':
            el.click()
            
    def getOrderBook(self,  market ='xrp', basecurr = 'inr'):
        """

        """
        askarray = np.zeros((20,2))
        bidarray = np.zeros((20,2))
        self.browser.reload()
        
        try:
        
            time.sleep(5)
            self.browser.execute_script('scroll(250, 0)')
            if self.mktbtc:
                self.browser.find_by_xpath('//*[@id="market"]/section/div/div[2]/div[1]/div/div/div[1]/div/ul/li[2]/a').click()
                marketclick = dict(omg=self.browser.find_by_xpath('//*[@id="market"]/section/div/div[2]/div[1]/div/div/div[2]/table/tbody/tr[3]').click,\
                        xrp=self.browser.find_by_xpath('//*[@id="market"]/section/div/div[2]/div[1]/div/div/div[2]/table/tbody/tr[5]').click,\
                        eth=self.browser.find_by_xpath('//*[@id="market"]/section/div/div[2]/div[1]/div/div/div[2]/table/tbody/tr[1]').click,\
                        ltc=self.browser.find_by_xpath('//*[@id="market"]/section/div/div[2]/div[1]/div/div/div[2]/table/tbody/tr[2]').click,\
                        qtum=self.browser.find_by_xpath('//*[@id="market"]/section/div/div[2]/div[1]/div/div/div[2]/table/tbody/tr[4]').click,\
                 )
                marketclick[market]()
            else: #inr market
                # self.browser.find_by_xpath('//*[@id="market"]/section/div/div[1]/div[1]/div/div[1]/div/ul/li[1]').click()

                marketclick = dict(omg=self.browser.find_by_xpath('//*[@id="market"]/section/div/div[2]/div[1]/div/div/div[2]/table/tbody/tr[4]').click,\
                        btc=self.browser.find_by_xpath('//*[@id="market"]/section/div/div[2]/div[1]/div/div/div[2]/table/tbody/tr[1]').click,\
                        xrp=self.browser.find_by_xpath('//*[@id="market"]/section/div/div[2]/div[1]/div/div/div[2]/table/tbody/tr[6]').click,\
                        eth=self.browser.find_by_xpath('//*[@id="market"]/section/div/div[2]/div[1]/div/div/div[2]/table/tbody/tr[2]').click,\
                        ltc=self.browser.find_by_xpath('//*[@id="market"]/section/div/div[2]/div[1]/div/div/div[2]/table/tbody/tr[3]').click,\
                        qtum=self.browser.find_by_xpath('//*[@id="market"]/section/div/div[2]/div[1]/div/div/div[2]/table/tbody/tr[5]').click,\
                        bch=self.browser.find_by_xpath('//*[@id="market"]/section/div/div[2]/div[1]/div/div/div[2]/table/tbody/tr[7]').click)
                marketclick[market]()
            time.sleep(5)
            page = self.browser.html
        except Exception, e:
            eprint("Order book failed for %s with %e"%(market, e))

        try:    

            countcorr = 0
            self.clickask1()
            self.clickbid1()
            for row in range(1,21):

                xpthbidsum  ='//*[@id="market"]/section/div/div[1]/div[4]/div/div/div[1]/table/tbody/tr[%i]/td[3]/text()'%(row+countcorr)
                xpthbidrate  ='//*[@id="market"]/section/div/div[1]/div[4]/div/div/div[1]/table/tbody/tr[%i]/td[4]/text()'%(row+countcorr)
                xpthaskvol = '//*[@id="market"]/section/div/div[1]/div[4]/div/div/div[2]/table/tbody/tr[%i]/td[2]/text()'%(row+countcorr)
                xpthaskrate = '//*[@id="market"]/section/div/div[1]/div[4]/div/div/div[2]/table/tbody/tr[%i]/td[1]/text()'%(row+countcorr)
                etree = html.fromstring(self.browser.html)
                bid_vol = pfloat(etree.xpath(xpthbidsum)[0])
                bid_rate = pfloat(etree.xpath(xpthbidrate)[0])
                ask_vol = pfloat(etree.xpath(xpthaskvol)[0])
                ask_rate = pfloat(etree.xpath(xpthaskrate)[0])
                if row == 10:

                    self.clickask2()
                    self.clickbid2()
                    countcorr = -10


                askarray[row-1, 1] = ask_vol
                askarray[row-1, 0] = ask_rate
                bidarray[row-1, 1] = bid_vol
                bidarray[row-1, 0] = bid_rate


        except Exception, e:
            eprint("Error occured in get order book %s - %s"%(market,e))
        return {\
            'asks' : askarray,\
            'bids' : bidarray
               }
