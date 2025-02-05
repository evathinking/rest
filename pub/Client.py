#!/usr/bin/eos
# -*- coding: utf-8 -*-
# encoding: utf-8

'''
Provide user specific data and interact with gate.io
'''
from pub.gateAPI import GateIO
from pub.Commons import TradingFunctions

__during = 10
__cycle = 300
__ma = 5
__currency = "eos_usdt"
__hedge_funds = 500
__gain_rate = 0.03
__low_income = 35
apiKey = '02542CE3-4E60-4BDE-B5E2-1962112A14AE'
secretKey = '96472f3bf7d53a26286cb0410a0adabed57bd133d407d5116251a9d309a0ad64'

## Provide constants
API_QUERY_URL = 'data.gateio.co'
API_TRADE_URL = 'api.gateio.co'

## Create a gate class instance
gate_query = GateIO(API_QUERY_URL, apiKey, secretKey)
gate_trade = GateIO(API_TRADE_URL, apiKey, secretKey)

tc = TradingFunctions(Currency=__currency,
                      Cycle=__cycle,
                      Ma=__ma,
                      HedgeFunds=__hedge_funds,
                      GainRate=__gain_rate,
                      LowIncome=__low_income)




#
# def calc_angle(x_point_s, y_point_s, x_point_e, y_point_e):
#     angle = 0
#     y_se = y_point_e - y_point_s;
#     x_se = x_point_e - x_point_s;
#     if y_se == 0:
#         angle = 0
#     elif y_se > 0:
#         angle = math.atan(y_se / x_se) * 180 / math.pi
#     else:
#         angle = -((math.atan(y_se / x_se) * 180 / math.pi)+90)
#     return angle
#
# print(calc_angle(x_point_s=0,y_point_s=6.83908,x_point_e=1,y_point_e=6.8499))
# Trading Pairs
# 返回所有系统支持的交易对
#     eth_btc: 以太币对比特币交易
#     etc_btc: 以太经典对比特币
#     etc_eth: 以太经典对以太币
#     xrp_btc: 瑞波币对比特币
#     zec_btc: ZCash对比特币
#     ……
# print(gate_query.pairs())


## Below, use general methods that query the exchange

#  Market Info
# 默认查询pair为eos_usdt
# 返回所有系统支持的交易市场的参数信息，包括交易费，最小下单量，价格精度等。
#     decimal_places: 价格精度
#     min_amount : 最小下单量
#     min_amount_a : 币种a [CURR_A]的最小下单量
#     min_amount_b : 币种b [CURR_B]的最小下单量
#     fee : 交易费
#     trade_disabled : 0表示未暂停交易，1表示已经暂停交易
# print(gate_query.marketinfo())

# Market Details
# 默认查询pair为eos_usdt
# 返回所有系统支持的交易市场的详细行情和币种信息，包括币种名，市值，供应量，最新价格，涨跌趋势，价格曲线等。
#     symbol : 币种标识
#     name: 币种名称
#     name_en: 英文名称
#     name_cn: 中文名称
#     pair: 交易对
#     rate: 当前价格
#     vol_a: 被兑换货币交易量
#     vol_b: 兑换货币交易量
#     curr_a: 被兑换货币
#     curr_b: 兑换货币
#     curr_suffix: 货币类型后缀
#     rate_percent: 涨跌百分百
#     trend: 24小时趋势 up涨 down跌
#     supply: 币种供应量
#     marketcap: 总市值
#     plot: 趋势数据
# print(gate_query.marketlist())

# Tickers
# 默认查询pair为eos_usdt
# 返回系统支持的所有交易对的 最新，最高，最低 交易行情和交易量，每10秒钟更新:
#     baseVolume: 交易量
#     high24hr: 24
#     小时最高价
#     highestBid: 买方最高价
#     last: 最新成交价
#     low24hr: 24
#     小时最低价
#     lowestAsk: 卖方最低价
#     percentChange: 涨跌百分比
#     quoteVolume: 兑换货币交易量
# print(gate_query.tickers())

# Depth
# print(gate_query.orderBook('eos_usdt'))

# orders
# print(gate_query.openOrders())


## Below, use methods that make use of the users keys



# Ticker
# '''
# 返回系统支持的所有交易对的 最新，最高，最低 交易行情和交易量，每10秒钟更新:
# baseVolume: 交易量
# high24hr: 24
# 小时最高价
# highestBid: 买方最高价
# last: 最新成交价
# low24hr: 24
# 小时最低价
# lowestAsk: 卖方最低价
# percentChange: 涨跌百分比
# quoteVolume: 兑换货币交易量
# '''
# print(gate_query.ticker('eos_usdt'))

# Market depth of pair
# print(gate_query.orderBook('btc_usdt'))

# Trade History
# print(gate_query.tradeHistory('btc_usdt'))
# import json
# data =gate_query.candleStick2(currency='eos_usdt', group_sec=900, range_hour=240)
# print (data)
# print(len(data['data']))

# Get account fund balances
# print(gate_trade.balances())

# get new address
# print(gate_trade.depositAddres('btc'))

# get deposit withdrawal history
# print(gate_trade.depositsWithdrawals('1469092370', '1569092370'))

# Place order sell
# print(gate_trade.buy('etc_btc', '0.001', '123'))

# Place order sell
# print(gate_trade.sell('etc_btc', '0.001', '123'))

# Cancel order
# print(gate_trade.cancelOrder('267040896', 'etc_btc'))

# Cancel all orders
# print(gate_trade.cancelAllOrders('0', 'etc_btc'))

# Get order status
# print(gate_trade.getOrder('267040896', 'eth_btc'))

# Get my last 24h trades
# print(gate_trade.mytradeHistory('etc_btc', '267040896'))

# withdraw
# print(gate_trade.withdraw('btc', '88', btcAddress))
