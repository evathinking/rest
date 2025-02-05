#!/usr/bin/eos
# -*- coding: utf-8 -*-

'''
Provide the GateIO class to abstract web interaction
'''

from pub.HttpUtil import httpGet, httpPost, httpGet2


class GateIO:
    def __init__(self, url, apiKey, secretKey):
        self.__url = url
        self.__apiKey = apiKey
        self.__secretKey = secretKey

    ## General methods that query the exchange

    # 所有交易对
    def pairs(self):
        URL = "/api2/1/pairs"
        params = ''
        return httpGet(self.__url, URL, params)

    # 市场订单参数
    def marketinfo(self,coin_pair="eos_usdt"):
        URL = "/api2/1/marketinfo"
        params = ''
        response = httpGet(self.__url, URL, params)
        if coin_pair is not None:
            for pair in response['pairs']:
                for k,v in pair.items():
                    if k == coin_pair.lower():
                        return v
        else:
            return response

    # 交易市场详细行情
    def marketlist(self, coin_pair="eos_usdt"):
        URL = "/api2/1/marketlist"
        params = ''
        response = httpGet(self.__url, URL, params)
        if coin_pair is not None:
            for coin in response['data']:
                if coin['pair'] == coin_pair.lower():
                    return coin
        else:
            return response

    def orderBooks_c2c(self):
        URL = "/api2/1/orderBooks_c2c"
        params = ''
        response = httpGet(self.__url, URL, params)
        return response['usdt_cny']

    # 所有交易
    def tickers(self, coin_pair="eos_usdt"):
        URL = "/api2/1/tickers"
        params = ''
        response=httpGet(self.__url, URL, params)
        if coin_pair is not None:
            return response[coin_pair]
        else:
            return response
    # 所有交易对市场深度
    def orderBooks(self):
        URL = "/api2/1/orderBooks"
        param = ''
        return httpGet(self.__url, URL, param)

    # 单项交易行情
    def ticker(self, param):
        URL = "/api2/1/ticker"
        return httpGet(self.__url, URL, param)

    # 单项交易对市场深度
    def orderBook(self, param):
        URL = "/api2/1/orderBook"
        return httpGet(self.__url, URL, param)

    # 历史成交记录
    def tradeHistory(self, param):
        URL = "/api2/1/tradeHistory"
        return httpGet(self.__url, URL, param)

    ## Methods that make use of the users keys

    # 获取帐号资金余额
    def balances(self):
        URL = "/api2/1/private/balances"
        param = {}
        return httpPost(self.__url, URL, param, self.__apiKey, self.__secretKey)

    # 获取充值地址
    def depositAddres(self, param):
        URL = "/api2/1/private/depositAddress"
        params = {'currency': param}
        return httpPost(self.__url, URL, params, self.__apiKey, self.__secretKey)

    # 获取充值提现历史
    def depositsWithdrawals(self, start, end):
        URL = "/api2/1/private/depositsWithdrawals"
        params = {'start': start, 'end': end}
        return httpPost(self.__url, URL, params, self.__apiKey, self.__secretKey)

    # 买入
    def buy(self, currencyPair, rate, amount):
        URL = "/api2/1/private/buy"
        params = {'currencyPair': currencyPair, 'rate': rate, 'amount': amount}
        return httpPost(self.__url, URL, params, self.__apiKey, self.__secretKey)

    # 卖出
    def sell(self, currencyPair, rate, amount):
        URL = "/api2/1/private/sell"
        params = {'currencyPair': currencyPair, 'rate': rate, 'amount': amount}
        return httpPost(self.__url, URL, params, self.__apiKey, self.__secretKey)

    # 取消订单
    def cancelOrder(self, orderNumber, currencyPair):
        URL = "/api2/1/private/cancelOrder"
        params = {'orderNumber': orderNumber, 'currencyPair': currencyPair}
        return httpPost(self.__url, URL, params, self.__apiKey, self.__secretKey)

    # 取消所有订单
    def cancelAllOrders(self, type, currencyPair):
        URL = "/api2/1/private/cancelAllOrders"
        params = {'type': type, 'currencyPair': currencyPair}
        return httpPost(self.__url, URL, params, self.__apiKey, self.__secretKey)

    # 获取下单状态
    def getOrder(self, orderNumber, currencyPair):
        URL = "/api2/1/private/getOrder"
        params = {'orderNumber': orderNumber, 'currencyPair': currencyPair}
        return httpPost(self.__url, URL, params, self.__apiKey, self.__secretKey)

    # 获取我的当前挂单列表
    def openOrders(self):
        URL = "/api2/1/private/openOrders"
        params = {}
        return httpPost(self.__url, URL, params, self.__apiKey, self.__secretKey)

    # 获取我的24小时内成交记录
    def mytradeHistory(self, currencyPair, orderNumber):
        URL = "/api2/1/private/tradeHistory"
        params = {'currencyPair': currencyPair, 'orderNumber': orderNumber}
        return httpPost(self.__url, URL, params, self.__apiKey, self.__secretKey)

    # 提现
    def withdraw(self, currency, amount, address):
        URL = "/api2/1/private/withdraw"
        params = {'currency': currency, 'amount': amount, 'address': address}
        return httpPost(self.__url, URL, params, self.__apiKey, self.__secretKey)

    # K线数据
    def candleStick2(self, currency, group_sec, range_hour):
        URL = "/api2/1/candlestick2/{0}?group_sec={1}&range_hour={2}".format(currency,str(group_sec),str(range_hour))
        return httpGet2(self.__url, URL)

    # def orderBook(self, currency):
    #     URL = "/api2/1/orderBooks/{0}".format(currency)
    #     params = ""
    #     return httpGet(self.__url, URL, params)