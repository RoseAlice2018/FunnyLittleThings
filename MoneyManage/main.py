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

cash_val   = tk.Label(root, text="")
cash_val.grid(row=1, column=1)

# 股票
# 期货
# 加密货币


# 执行
root.mainloop()