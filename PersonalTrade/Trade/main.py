

class InvestmentStrategy:
    def __init__(self, annual_return_rate=0.28, buy_threshold=-0.075, max_holdings=20):
        self.annual_return_rate = annual_return_rate
        self.buy_threshold = buy_threshold
        self.max_holdings = max_holdings
        self.portfolio = defaultdict(list)  # 存储投资组合
    
def calculate_sell_price(self, purchase_price, holding_period_days):
        # 计算卖出价格
        holding_period_years = holding_period_days / 365.0
        sell_price = purchase_price * math.pow((1 + self.annual_return_rate), holding_period_years)
        return sell_price

    def check_and_trade(self, symbol):
        stock = get_stock_info(symbol)
        today = datetime.date.today()

        # 检查是否需要买入
        if stock.current_price < stock.estimated_value * (1 + self.buy_threshold):
            if len(self.portfolio[symbol]) < self.max_holdings:
                logging.info(f"Bought at {stock.current_price} on {today}.")
                self.portfolio[symbol].append((stock.current_price, today))

        # 检查是否需要卖出
        for purchase_price, purchase_date in self.portfolio[symbol]:
            holding_period_days = (today - purchase_date).days
            sell_price = self.calculate_sell_price(purchase_price, holding_period_days)
            if stock.current_price >= sell_price:
                logging.info(f"Selling at {stock.current_price} on {today}.")
                self.portfolio[symbol].remove((purchase_price, purchase_date))   


if __name__ == "__main__":
    