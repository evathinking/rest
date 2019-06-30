#!/usr/bin/eos
# -*- coding:utf-8 -*-
"""
    功    能:
        自动交易系统
    修改信息:
        2019/6/17 11:46 d00357487 Created
    版权信息:
        华为技术有限公司，版权所有(C) 2019-2020
"""
import time
import sys

sys.path.append('..')
from pub.Commons import TradingFunctions

if __name__ == '__main__':

    __during = 10
    __cycle = 900
    __ma = 5
    __currency = "btc_usdt"
    __hedge_funds = 4500
    __gain_rate = 0.05
    __low_income = 35
    __usdt_income = 7.07

    tc = TradingFunctions(Currency=__currency,
                          Cycle=__cycle,
                          Ma=__ma,
                          HedgeFunds=__hedge_funds,
                          GainRate=__gain_rate,
                          LowIncome=__low_income)

    while True:
        buy = tc.buy_point()
        if buy and tc.get_buy_flag() is False:
            tc.send_msg(buy)
            tc.send_msg(buy)
            tc.send_msg(buy)
            # tc.buy()
            tc.set_buy_flag("True")
            tc.set_sell_flag("False")
        sell = tc.sell_point()
        if sell and tc.get_sell_flag() is False:
            tc.send_msg(sell)
            tc.send_msg(sell)
            tc.send_msg(sell)
            # tc.sell()
            tc.set_sell_flag("True")
            tc.set_buy_flag("False")
        usdt_price = tc.get_usdt_min_price()
        if float(usdt_price) <= __usdt_income and tc.get_usdt_flag() is False:
            tc.send_msg("USDT:" + str(usdt_price))
            tc.send_msg("USDT:" + str(usdt_price))
            tc.set_usdt_flag("True")
        time.sleep(__during)
        continue
