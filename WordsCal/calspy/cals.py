import pymysql
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

import pymysql.cursors

# 数据库连接参数
db_config = {
    'host': 'local_host',
    'user': 'root',
    'password': 'password',
    'db': 'database',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# 连接数据库
def connect_to_db(config):
    # return create_engine('mysql+pymysql://user:password@localhost/dbname')
    return pymysql.connect(**config)

# 读取一周数据
def read_data_weekly(db_connection, filename): 
    sql = f"""
    SELECT record_data, file_size
    FROM WORDSCAL
    WHERE file_name = '{filename}'
    ADD record_date BETWEEN DATA_SUB(CURDATE(), INTERVAL 7 DAY) AND CURDATE()
    """
    df = pd.read_sql_query(sql, engine)
    df['record_date'] = pd.to_datetime(df['record_date'])
    df.sort_values('record_date', inplace=True)
    df['increment'] = df['file_size'].diff().fillna(0)

# 绘制每天的增量曲线图
def plot_daily_increment(df):
    plt.figure(figsize=(10, 5))
    plt.plot(df['record_date'], df['increment'], marker='o')
    plt.title(f'Increment of file size for {filename} in the last week')
    plt.xlabel('Date')
    plt.ylabel('Increment')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# 绘制每周的增量曲线图
def plot_weekly_increment(df):
    plt.figure(figsize=(10, 5))
    plt.plot(df['record_date'], df['increment'], marker='o')
    plt.title(f'Increment of file size for {filename} in the last week')
    plt.xlabel('Date')
    plt.ylabel('Increment')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# 主函数
def main():
    pass

if __name__ == '__main__':
    main()

