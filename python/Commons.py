#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    功    能:
        包含交易通用方法
    修改信息:
        2019/6/17 10:15 d00357487 Created
    版权信息:
        华为技术有限公司，版权所有(C) 2019-2020
"""
import csv
import time,datetime
import json
import os, sys
import logging
import pandas as pd

from gateAPI import GateIO


class TradingFunctions:


    def __init__(self, Currency, Cycle, Ma, HedgeFunds, GainRate):

        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.StreamHandler(sys.stdout))
        self.logger.addHandler(logging.FileHandler(filename='log.log', encoding='utf-8'))
        ## 填写 apiKey APISECRET
        apiKey = '02542CE3-4E60-4BDE-B5E2-1962112A14AE'
        secretKey = '96472f3bf7d53a26286cb0410a0adabed57bd133d407d5116251a9d309a0ad64'

        ## Provide constants
        API_QUERY_URL = 'data.gateio.co'
        API_TRADE_URL = 'api.gateio.co'

        ## Create a gate class instance
        self.gate_query = GateIO(API_QUERY_URL, apiKey, secretKey)
        self.gate_trade = GateIO(API_TRADE_URL, apiKey, secretKey)

        self.balances = json.loads(self.gate_trade.balances())
        self.__UsdtNumber = self.balances['available']['USDT']
        self.__EosNumber = self.balances['available']['EOS']

        self.logger.info("初始资金，EOS:{0}, USDT:{1}".format(self.__EosNumber, self.__UsdtNumber))

        # # 测试数据
        # self.__UsdtNumber = 3500
        # self.__EosNumber = 0

        ## 交易基础数据
        self.MaFilePath = r"Ma_Value.csv"  # k线以及ma值存放数据表格
        self.BusinessFilePath = r"Business.csv"  # 交易数据表格
        self.Currency = Currency  # 交易对
        self.Cycle = Cycle  # K线周期
        self.Ma = Ma  # 移动均值
        self.GainRate = GainRate # 止盈点
        if float(HedgeFunds) > float(self.__UsdtNumber) or float(HedgeFunds) <= 1:
            raise Exception("invalid hedge funds，insufficient usdt or too small hedge funds.")
        else:
            self.HedgeFunds = float(HedgeFunds) # 对冲USDT数量

    def Write_json(self, file, json):
        # 写入本地json文件
        with open(file, 'a+') as d_log:
            d_log.write(json + "\r\n")
    
    def Write_info_log(self,log):
        # 写入log.log
        with open('log.log', 'a+') as d_log:
            d_log.write(log + "\r\n")
    
    def Time_stamp(self, timeNum):
        """
        时间戳转换为可读时间
        Args:
            timeNum, 时间戳

        Returns:
            本地可读时间

        Changes:
            2019/6/17 10:15 d00357487 Created
        """
        timeStamp = float(timeNum / 1000)
        timeArray = time.localtime(timeStamp)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return otherStyleTime

    def get_gateio_tradding_pairs(self):
        # Trading Pairs, test api is working
        self.logger.info(self.gate_query.pairs())

    def get_gateio_kdata(self):
        """
        根据统计周期取得 k 线数据，

        Args:
            currency, 等于self.Currency
            group_sec, 等于self.Cycle
            range_hour，默认是从当前时间往前推Ma*2天时间 等于24*Ma*2
            start_time，(预留) 数据为当前时间到start_time的小时差数加上24*Ma*2
            end_time，(预留)小于或者等于现在时间

        Returns:
            生成一个csv文件

        Changes:
            2019/6/17 10:15 d00357487 Created

    """
        currency = str(self.Currency)
        group_sec = str(self.Cycle)
        range_hour = str(int(self.Ma) * 24 * 2)
        res = self.gate_query.candleStick2(currency=currency,
                                                      group_sec=group_sec,
                                                      range_hour=range_hour)
        # self.Write_json("{0}_{1}_{2}.json".format(currency, group_sec, range_hour), res["data"])
        return res["data"]

    def write_kdata_into_csv(self, kdatas):

        # kdatas = self.get_gateio_kdata()

        # # 测试数据
        # with open("{0}_{1}_{2}.json".format(self.Currency, self.Cycle, str(int(self.Ma) * 24 * 2)), 'r') as load_f:
        #     kdatas = json.load(load_f)

        headers = ['timestamp', 'date',  'volume', 'close',  'high', 'low',  'open']
        rows = []
        for kd in kdatas:
            local_time = self.Time_stamp(float(kd[0]))
            rows.append([str(kd[0]), local_time, kd[1], kd[2], kd[3], kd[4], kd[5]])

        with open(self.MaFilePath, 'w', newline='')as f:
            f_csv = csv.writer(f)
            f_csv.writerow(headers)
            f_csv.writerows(rows)

    def caculate_ma(self):
        # 导入数据
        stock_data = pd.read_csv(self.MaFilePath, parse_dates=True, index_col=0)

        # 数据按照时间倒序
        stock_data.sort_values(by="date", axis=0, ascending=False, inplace=True, kind='quicksort', na_position='last')

        #  计算简单算术移动平均线MA - 注意：stock_data['close']为股票每天的收盘价
        stock_data['Ma5'] = stock_data['close'].rolling(window=5).mean().shift(-4)

        # 保存到表格
        stock_data.to_csv(self.MaFilePath, index=True)

    def buy_point(self):
        #      读取最新ma-value.csv,判断买点规则，返回true or false

        self.write_kdata_into_csv(self.get_gateio_kdata())
        self.caculate_ma()
        stock_data = pd.read_csv(self.MaFilePath, parse_dates=True, index_col=0)
        first_line = stock_data.to_dict('record')[0]

        if float(first_line['low']) >= float(first_line['Ma5']):
            self.logger.info("当前最新买点k线及ma值：")
            self.logger.info(first_line)
            return True
        self.logger.info("当前非买点最新k线及ma值：")
        self.logger.info(first_line)
        return False

    def buy(self):
        # 获得当前深度最大的买单价
        self.buy_price = self.get_depth_buy_price()
        self.buy_eos_amount = float(self.HedgeFunds / self.buy_price)
        self.buy_cost = self.buy_eos_amount * 0.002 * self.buy_price
        before_eos = self.__EosNumber
        before_usdt = self.__UsdtNumber

        # buy_res = self.gate_trade.buy(self.Currency, eos_price, eos_amount)

        self.__EosNumber =float(before_eos) + float(self.buy_eos_amount) - float(self.buy_cost)
        self.__UsdtNumber = float(before_usdt) - float(self.HedgeFunds)
        date_stampe = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

        # headers = ['date', 'business', 'before_eos',  'before_usdt', 'buy_eos_amount',
        #            'buy_price',  'cost',  'after_eos',  'after_usdt']
        row = [date_stampe,
               'Buy',
               before_eos,
               before_usdt,
               self.buy_eos_amount,
               self.buy_price,
               self.buy_cost,
               self.__EosNumber,
               self.__UsdtNumber]
        self.logger.info(row)
        with open(self.BusinessFilePath, 'a+', newline='')as f:
            f_csv = csv.writer(f)
            # f_csv.writerow(headers)
            f_csv.writerow(row)

        # return buy_res['orderNumber']
        return "buy_orderNumber"

    def sell_point(self):
        current_price = self.gate_query.ticker(self.Currency)['last']
        date_stampe = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        self.logger.info(date_stampe+" 当前最新价格："+current_price)

        if self.judge_gain(current_price):
            date_stampe = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            self.logger.info(date_stampe+" 当前达到止盈点3%："+current_price)
            return current_price

        stock_data = pd.read_csv(self.MaFilePath, parse_dates=True, index_col=0)
        first_line = stock_data.to_dict('record')[0]
        if float(first_line['low']) < float(first_line['Ma5']) or float(first_line['high']) > float(
                first_line['Ma5']) * 1.15:
            self.logger.info("当前卖点k线及ma值：")
            self.logger.info(first_line)
            return "ma_sell"
        self.logger.info("当前非卖点最新k线及ma值：")
        self.logger.info(first_line)
        return "unok"

    def sell_ma_price(self):
        # 获得当前深度最大的卖单价
        self.sell_price = self.get_depth_sell_price()
        self.sell_eos_amount = float(self.HedgeFunds / self.sell_price)
        self.sell_cost = self.HedgeFunds * 0.002
        before_eos = self.__EosNumbe
        before_usdt = self.__UsdtNumber

        # sell_res = self.gate_trade.sell(self.Currency, eos_price, eos_amount)

        self.__EosNumber = before_eos - self.sell_eos_amount
        self.__UsdtNumber = before_usdt + self.HedgeFunds - self.sell_cost
        date_stampe = time.strftime('%Y-%m-%d %H%:%M', time.localtime(time.time()))

        # headers = ['date',  'business',  'before_eos', 'before_usdt', 'sell_eos_amount',
        #            'sell_price',  'cost', 'after_eos', 'after_usdt']
        row = [date_stampe,
               'M_Sell',
               before_eos,
               before_usdt,
               self.sell_eos_amount,
               self.sell_price,
               self.sell_cost,
               self.__EosNumber,
               self.__UsdtNumber]
        self.logger.info(row)
        with open(self.BusinessFilePath, 'a+', newline='')as f:
            f_csv = csv.writer(f)
            # f_csv.writerow(headers)
            f_csv.writerow(row)
            f.close()

        # return sell_res['orderNumber']
        return "sell_orderNumber"

    def sell_current_price(self, current_price):
        self.sell_price = current_price * 0.998
        self.sell_eos_amount = float(self.HedgeFunds / self.sell_price)
        self.sell_cost = self.HedgeFunds * 0.002
        before_eos = self.__EosNumbe
        before_usdt = self.__UsdtNumber

        # sell_res = self.gate_trade.sell(self.Currency, eos_price, eos_amount)

        self.__EosNumber = before_eos - self.sell_eos_amount
        self.__UsdtNumber = before_usdt + self.HedgeFunds - self.sell_cost
        date_stampe = time.strftime('%Y-%m-%d %H%:%M', time.localtime(time.time()))

        # headers = ['date', 'business', 'before_eos', 'before_usdt', 'sell_eos_amount',
        #            'sell_price', 'cost', 'after_eos', 'after_usdt']
        row = [date_stampe,
               'C_Sell',
               before_eos,
               before_usdt,
               self.sell_eos_amount,
               self.sell_price,
               self.sell_cost,
               self.__EosNumber,
               self.__UsdtNumber]
        self.logger.info(row)
        with open(self.BusinessFilePath, 'a+', newline='')as f:
            f_csv = csv.writer(f)
            # f_csv.writerow(headers)
            f_csv.writerow(row)
            f.close()

        # return sell_res['orderNumber']
        return "sell_orderNumber"

    def get_order_status(self, orderNumber):
        # return self.gate_trade.getOrder(orderNumber, self.Currency)['order']['status']
        return "closed"

    def get_depth_sell_price(self):
        sell_depth_data = self.gate_query.orderBook('eos_usdt')['asks']
        stock_data = pd.DataFrame(sell_depth_data, columns=['price', 'amount'])
        stock_data.sort_values(by="amount", axis=0, ascending=False, inplace=True, kind='quicksort', na_position='last')
        sell_price = stock_data.to_dict('record')[0]['price']
        return float(sell_price)

    def get_depth_buy_price(self):
        buy_depth_data = self.gate_query.orderBook('eos_usdt')['bids']
        stock_data = pd.DataFrame(buy_depth_data, columns=['price', 'amount'])
        stock_data.sort_values(by="amount", axis=0, ascending=False, inplace=True, kind='quicksort', na_position='last')
        buy_price = stock_data.to_dict('record')[0]['price']
        return float(buy_price)

    def cal_gain(self):
        all_cost = float(self.buy_cost) * float(self.buy_price) + float(self.sell_cost)
        all_gain = float(self.buy_eos_amount - self.sell_eos_amount) * float(self.sell_price)
        return all_gain - all_cost

    def judge_gain(self, current_price):
        all_cost = float(self.buy_cost) * float(self.buy_price) + self.HedgeFunds*0.002
        tmp_sell_eos_amount = float(float(self.HedgeFunds) / float(current_price))
        all_gain = float(float(self.buy_eos_amount) - tmp_sell_eos_amount) * float(current_price)
        gain_cal = float((float(current_price) - float(self.buy_price)) / float(self.buy_price))
        if all_cost < all_gain and  gain_cal > float(self.GainRate):
            self.logger.info("当前的赢利点："+str(gain_cal))
            return True
        self.logger.info("当前的赢利点只有：" + str(gain_cal)+ "，不交易。")
        return False
