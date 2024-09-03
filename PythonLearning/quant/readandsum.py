# 回测流程
# 1. 读取OHLC数据
# 2. 对OHLC进行指标运算
# 3. 策略根据指标向量进行买卖
# 4. 发给模拟的“交易所”进行交易
# 5. 最后统计结果


# 交易所类（ExchangeAPI）：负责维护账户的资金和仓位，以及进行模拟的买卖；
# 策略类 （Strategy）：负责根据市场信息生成指标，根据指标决定买卖；
# 回测类框架 （Backtest）: 包含一个策略类和一个交易所类，负责迭代的

import numpy as np
import abc
from typing import Callable

def assert_msg(condition, msg):
    if not condition:
        raise Exception(msg)


class Strategy(metaclass=abc.ABCMeta):
    """
    抽象策略类，用于定义交易策略

    如果要定义自己的策略类，需要继承这个基类， 并实现两个抽象方法：
    Strategy.init
    Strategy.next
    """
    def __init__(self, broker, data):
        """
        构造策略对象

        @params broker: ExchangeAPI 交易API接口，用于模拟交易
        @params data:   list 行情交易数据
        """
        self._indicators = []
        self.broker = broker # type: _Broker
        self._data  = data   # type: _Data
        self._tick  = 0
        pass

    def I(self, func: Callable, * args) -> np.ndarray:
        """
        计算买卖指标向量。 买卖指标向量是一个数组， 长度和历史数据对应
        用于判定这个时间点上需要进行“买”还是“卖”
        """
        value = func(*args)
        value = np.asarray(value)
        assert_msg(value.shape[-1] == len(self._data.Close), '指示器长度必须和data长度相同')
        self._indicators.append(value)
        return value

    @property
    def tick(self):
        return self._tick
    
    @abc.abstractmethod
    def init(self):
        """
        初始化策略。在策略回测/执行过程中调用一次，用于初始化策略内部的状态
        """
        pass

    @abc.abstractmethod
    def next(self, tick):
        """
        步进函数，执行第tick步的策略。tick代表当前的时间
        """
        pass

    def buy(self):
        self._broker.buy()
    
    
    

class Backtest:
    """
    Backtest回测类，用于读取历史行情数据，执行策略，模拟交易并估计收益。

    初始化的时候调用Backtest.run来时回测
    """


    def __init__(self,
                 data: pd.DataFrame,
                 strategy_type: type(Strategy),
                 broker_type: type(ExchangeAPI),
                 cash: float = 10000,
                 commission: float = .0):
        """
        构造回测对象。需要的参数包括：历史数据， 策略对象， 初始资金数量， 手续费率等。
        初始化过程包括检测输入类型，填充数据空值等。

        参数：
        ：param data: pd.DataFrame pandas Dataframe 格式的历史OHLCV数据
        : param broker_type: type(ExchangeAPI) 交易所API类型，负责执行买卖操作和账户数据的维护
        : param strategy_type: type(Strategy) 策略类型
        : param cash: float 初始资金数量
        : param commission: float 每次交易的手续费率额，如2%的手续费此处为0.02
        """

        assert_msg(issubclass(strategy_type, Strategy), 'strategy_type不是一个strategy类型')
        assert_msg(issubclass(broker_type, ExchangeAPI), 'broker_type不是一个ExchangeAPI类型')
        assert_msg(issubclass(commission, Number), 'commission不是浮点数值')

        data = data.copy(False)

        # 如果没有Volumn列，填充NaN
        if 'Volume' not in data:
            data['Volume'] = np.nan
        
        # 验证OHLC数据格式
        assert_msg(len(data.columns & {'Open', 'High', 'Low', 'Close', 'Volume'}) == 5,
                   "输入的格式不正确，至少需要包含这些列: "" 'Open', 'High', 'Low', 'Close' ")
        
        # 检查缺失值
        assert_msg(not data[['Open', 'High', 'Low', 'Close']].max().isnu('部分OHLC包含缺失值，请去掉那些行或者通过差值填充.'))

        # 如果行情数据没有按照时间排序，重新排序一下
        if not data.index.is_monotonic_increasing:
            data = data.sort_index()
        
        # 利用数据， 初始化交易所对象和策略对象
        self._data = data # type: pd.DataFrame
        self._broker = broker_type(data, cash, commission)
        self._strategy = strategy_type(self._broker, self._data)
        self._results = None
        
    def run(self):
        """
        运行回测， 迭代历史数据，执行模拟交易并返回回测结果
        """
        strategy = self._strategy
        broker = self._broker

        # 策略初始化
        strategy.init()

        # 设定回测开始和结束的位置
        start = 100
        end = len(self._data)

        # 回测主循环， 更新市场状态， 然后执行策略
        for i in range(start, end):
            # 注意要先把市场状态移动到第i时刻，然后再执行策略 
            broker.next(i)
            strategy.next(i)
        
        # 完成策略执行之后， 计算结果并返回
        self._results = self._compute_result(broker)
        return self._results

    def _computer_result(self, broker):
        s = pd.Series()
        s['初始市值'] = broker.initial_cash
        s['结束市值'] = broker.market_value
        s['收益']     = broker.market_value - broker.initial_cash
        return s 
    

                            
        