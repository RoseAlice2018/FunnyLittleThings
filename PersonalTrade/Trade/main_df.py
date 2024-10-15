# coding=utf-8
from __future__ import print_function, absolute_import
from gm.api import *
import os
import time

annual_return_rate = 0.28

def init(context):
    # 每天14:50 定时执行algo任务,
    # algo执行定时任务函数，只能传context参数
    # date_rule执行频率，目前暂时支持1d、1w、1m，其中1w、1m仅用于回测，实时模式1d以上的频率，需要在algo判断日期
    # time_rule执行时间， 注意多个定时任务设置同一个时间点，前面的定时任务会被后面的覆盖
    schedule(schedule_func=algo, date_rule='1d', time_rule='07:50:00')

class IDGenerator:
    def __init__(self):
        self.id_counter = 0

    def get_next_id(self):
        self.id_counter += 1
        return self.id_counter 

id_gen = IDGenerator()

class stock_trade:
    def __init__(self, stock_id, buy_price, quantity, buy_time, sell_price, sell_quantity, sell_timestamp):
        self.transaction_id = id_gen.get_next_id()
        self.stock_id = stock_id
        self.buy_price = buy_price
        self.quantity = quantity
        self.buy_time = buy_time
        self.sell_price = sell_price
        self.sell_quantity = sell_quantity
        self.sell_timestamp = sell_timestamp
        self.annual_return_rate = annual_return_rate

    def buy(self, buy_price, quantity):
        self.buy_price = buy_price
        self.quantity = quantity
        self.buy_time = (int)time.time()
    
    def sell(self, sell_price, quantity):
        self.sell_price = sell_price
        self.sell_quantity = quantity
        self.sell_timestamp = (int)time.time()

def read_stock_pool(filename):
    stock_ids[]
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            stock_id = line.strip()
            if stock_id is not None:
                stock_ids.append(stock_id)
    return stock_ids

def read_history_trade(filename):
    data = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            # 每项之间由空格分隔
            parts = line.strip().split()
            if len(parts) != 9:
                print(f"错误，行'{line}'格式不正确")
                continue 
            # 提取信息并尝试转换为适当的数据类型
            try:
                transaction_id, stock_id, buy_price, quantity, but_time, sell_price, sell_quantity, sell_timestamp, annual_return_rate = parts

                # 将字符串转为数值类型
                buy_price = float(buy_price)
                quantity  = float(quantity)
                sell_price = float(sell_price)
                sell_quantity = float(sell_quantity)
                annual_return_rate = float(annual_return_rate) 

                


def algo(context):
    # 读取备选股票
    stocks_pool = read_stock_pool('./stock_pool.txt')
    # 读取历史交易记录


    # 读取价格
    # 读取Data中买卖记录
    # 计算市盈率
    # 以市价购买200股浦发银行股票， price为保护限价
    order_volume(symbol='SHSE.600000', volume=200, side=OrderSide_Buy,
                 order_type=OrderType_Market, position_effect=PositionEffect_Open, price=0)


# 查看最终的回测结果
def on_backtest_finished(context, indicator):
    print(indicator)


if __name__ == '__main__':
    '''
        strategy_id策略ID, 由系统生成
        filename文件名, 请与本文件名保持一致
        mode运行模式, 实时模式:MODE_LIVE回测模式:MODE_BACKTEST
        token绑定计算机的ID, 可在系统设置-密钥管理中生成
        backtest_start_time回测开始时间
        backtest_end_time回测结束时间
        backtest_adjust股票复权方式, 不复权:ADJUST_NONE前复权:ADJUST_PREV后复权:ADJUST_POST
        backtest_initial_cash回测初始资金
        backtest_commission_ratio回测佣金比例
        backtest_slippage_ratio回测滑点比例
        backtest_match_mode市价撮合模式，以下一tick/bar开盘价撮合:0，以当前tick/bar收盘价撮合：1
    '''
    run(strategy_id='205c6ddb-8b11-11ef-851a-00ff976e2e31',
        filename='main.py',
        mode=MODE_BACKTEST,
        token='19122ae5bc27fc5b10968e1008bd15a0536cdd89',
        backtest_start_time='2020-11-01 08:00:00',
        backtest_end_time='2020-11-10 16:00:00',
        backtest_adjust=ADJUST_PREV,
        backtest_initial_cash=10000,
        backtest_commission_ratio=0.0001,
        backtest_slippage_ratio=0.0001,
        backtest_match_mode=1)

