import json
import sys
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from consts import ExcuteArg
import mysql.connector

# 打开JSON文件
def readconfig():
    with open('./config/config.json', 'r') as file:
        data = json.load(file)
        return data

localsavepath = readconfig()['savepath']['defaultpath']

# 连接数据库 
def connect_to_db():
    data = readconfig()
    conn = mysql.connector.connect(
        # host="localhost",
        user=data['database']['user'],
        password=data['database']['password'],
        database=data['database']['dbname'],
        unix_socket='/var/run/mysqld/mysqld.sock'
    )
    return conn

# plot 绘制
def plot(results, filename):
    record_data = [item[0] for item in results]
    file_sizes = [item[1] for item in results]

    print('record_data:%s', record_data)
    print('file_size:%s', file_sizes)
    plt.figure()
    plt.plot(record_data, file_sizes, marker='o') # 'o'是点标记

    # 设置图表标题和坐标轴标签
    plt.title('File Size Trend')
    plt.xlabel('Record Data')
    plt.ylabel('File Size')

    # 显示网格
    plt.grid(True)

    # 显示图例
    plt.legend(['File Size'])

    # save图表
    plt.savefig('{}/{}.png'.format(localsavepath, filename))

# 读取一周的数据
def read_data_weekly(filename):
    conn = connect_to_db()
    cursor = conn.cursor()
    sql = f"""
    SELECT record_date, file_size
    FROM WORDSCAL
    WHERE file_name = '{filename}'
    AND record_date BETWEEN DATE_SUB(CURDATE(), INTERVAL 7 DAY) AND CURDATE()
    """
    cursor.execute(sql)
    results = cursor.fetchall()
    plot(results, filename)

# 读取一个月的数据
def read_data_monthly(filename):
    conn = connect_to_db()
    cursor = conn.cursor()
    sql = f"""
    SELECT record_date, file_size
    FROM WORDSCAL
    WHERE file_name = '{filename}'
    AND record_date BETWEEN DATE_SUB(CURDATE(), INTERVAL 30 DAY) AND CURDATE()
    """
    cursor.execute(sql)
    results = cursor.fetchall()
    plot(results, filename)

# 读取三个月的数据
def read_data_quarterly(filename):
    conn = connect_to_db()
    cursor = conn.cursor()
    sql = f"""
    SELECT record_date, file_size
    FROM WORDSCAL
    WHERE file_name = '{filename}'
    AND record_date BETWEEN DATE_SUB(CURDATE(), INTERVAL 90 DAY) AND CURDATE()
    """
    cursor.execute(sql)
    results = cursor.fetchall()
    plot(results, filename)

# 读取十二个月的数据
def read_data_yearly(filename):
    conn = connect_to_db()
    cursor = conn.cursor()
    sql = f"""
    SELECT record_date, file_size
    FROM WORDSCAL
    WHERE file_name = '{filename}'
    AND record_date BETWEEN DATE_SUB(CURDATE(), INTERVAL 365 DAY) AND CURDATE()
    """
    cursor.execute(sql)
    results = cursor.fetchall()
    plot(results, filename)


# 主函数
def main():
    if len(sys.argv) < 3:
        print("Usage: python3 cals.py <arg1:Type> <arg2:FileName>")
        sys.exit(1)
    
    arg1 = int(sys.argv[1])
    arg2 = sys.argv[2]
    if arg1 == ExcuteArg.WEEKLY:
        read_data_weekly(arg2)
    elif arg1 == ExcuteArg.MONTHLY:
        read_data_monthly(arg2)
    elif arg1 == ExcuteArg.QUARTERLY:
        read_data_quarterly(arg2)
    elif arg1 == ExcuteArg.YEARLY:
        read_data_yearly(arg2)

if __name__ == '__main__':
    main()

