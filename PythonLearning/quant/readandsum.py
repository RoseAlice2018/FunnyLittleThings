# 回测流程
# 1. 读取OHLC数据
# 2. 对OHLC进行指标运算
# 3. 策略根据指标向量进行买卖
# 4. 发给模拟的“交易所”进行交易
# 5. 最后统计结果


# 交易所类（ExchangeAPI）：负责维护账户的资金和仓位，以及进行模拟的买卖；
# 策略类 （Strategy）：负责根据市场信息生成指标，根据指标决定买卖；
# 回测类框架 （Backtest）: 包含一个策略类和一个交易所类，负责迭代的


def assert_msg(condition, msg):
    if not condition:
        raise Exception(msg)
    

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
    

                            
        