#!/usr/bin/python
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

from Commons import TradingFunctions

if __name__ == '__main__':

    __during = 10
    __cycle = 300
    __ma = 5
    __currency = "eos_usdt"
    __hedge_funds = 500
    __gain_rate = 0.03

    tc = TradingFunctions(Currency=__currency,
                          Cycle=__cycle,
                          Ma=__ma,
                          HedgeFunds=__hedge_funds,
                          GainRate=__gain_rate)
    __buy_flag = tc.get_buy_flag()
    __sell_flag = tc.get_sell_flag()

    for i in range(0, 100):
        while __buy_flag is False:
            buy = tc.buy_point()
            if buy:
                tc.buy()
                tc.set_buy_flag("True")
                tc.set_sell_flag("False")
                __buy_flag = True
                __sell_flag = False
                break
            else:
                time.sleep(__during)
                continue
        while __buy_flag is True and __sell_flag is False:
            sell = tc.sell_point()
            if sell:
                tc.sell()
                tc.set_buy_flag("False")
                tc.set_sell_flag("True")
                __buy_flag = False
                __sell_flag = True
                break
            else:
                time.sleep(__during)
                continue


