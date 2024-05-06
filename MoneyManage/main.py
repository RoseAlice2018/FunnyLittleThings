import tkinter as tk
import sqlite3
import yaml

# 读取配置
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

target_money = config['TARGET_MONEY']

# 创建主窗口
root = tk.Tk()

# 设置窗口标题
root.title("收入管理")

# 设置窗口大小
root.geometry("1200x800")

# 目标金额
target_money_label = tk.Label(root, text="FuckYouMoney: ")
target_money_label.grid(row=0, column=0)

target_money_val = tk.Label(root, text=f"{target_money}")
target_money_val.grid(row=0, column=1)

# 余额宝等货币基金，国债逆回购 低风险收入
# cash or cash equivalents
cash_label = tk.Label(root, text="现金或现金等价物: ")
cash_label.grid(row=1, column=0)

cash_val   = tk.Label(root, text="10")
cash_val.grid(row=1, column=1)


# 股票
# Stock
stock_label = tk.Label(root, text="股票")
stock_label.grid(row=2, column=0)

stock_val = tk.Label(root, text="10")
stock_val.grid(row=2, column=1)

# 期货
future_label = tk.Label(root, text="期货")
future_label.grid(row=3, column=0)

future_val = tk.Label(root, text="10")
future_val.grid(row=3, column=1)

# 加密货币
btc_label = tk.Label(root, text="加密货币")
btc_label.grid(row=4, column=0)

btc_val = tk.Label(row=4, text="10")
btc_val.grid(row=4, column=1)

# 执行
root.mainloop()