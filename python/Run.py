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

    __buy_flag = False
    __sell_flag = False
    __gain_flag = False
    __during = 10
    __cycle = 900
    __ma = 5
    __currency = "eos_usdt"
    __hedge_funds = 100
    __gain_rate = 0.03

    tc = TradingFunctions(Currency=__currency,
                          Cycle=__cycle,
                          Ma=__ma,
                          HedgeFunds=__hedge_funds,
                          GainRate=__gain_rate)
    for i in range(0, 100):
        while __buy_flag is False:
            buy = tc.buy_point()
            if buy:
                order_num = tc.buy()
                while tc.get_order_status(order_num) != "closed":
                    time.sleep(120)
                __buy_flag = True
                __sell_flag = False
                break
            else:
                time.sleep(__during)
                continue
        while __buy_flag is True and __sell_flag is False:
            sell = tc.sell_point()
            if sell == "ma_sell":
                order_num = tc.sell_ma_price()
                while tc.get_order_status(order_num) != "closed":
                    time.sleep(120)
                __buy_flag = False
                __sell_flag = True
                break
            elif sell == "unok":
                time.sleep(__during)
                continue
            else:
                order_num = tc.sell_current_price(sell)
                while tc.get_order_status(order_num) != "closed":
                    time.sleep(120)
                __buy_flag = False
                __sell_flag = True
                break

