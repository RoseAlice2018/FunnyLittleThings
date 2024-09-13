import json
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import mysql.connector

# 打开JSON文件
def readconfig():
    with open('./config/config.json', 'r') as file:
        data = json.load(file)
        return data

# 连接数据库
def connect_to_db():
    data = readconfig()
    conn = mysql.connector.connect(
        host="localhost",
        user=data['database']['user'],
        password=data['database']['password'],
        database=data['database']['dbname']
    )
    return conn

# 读取一周的数据
def read_data_weekly(filename):
    conn = connect_to_db()
    cursor = conn.cursor()
    sql = f"""
    SELECT record_data, file_size
    FROM WORDSCAL
    WHERE file_name = '{filename}'
    AND record_date BETWEEN DATA_SUB(CURDATE(), INTERVAL 7 DAY) AND CURDATE()
    """
    cursor.excute(sql)
    results = cursor.fetchall()
    record_data = [item[0] for item in results]
    file_sizes = [item[1] for item in results]

    plt.figure()
    plt.plot(record_data, file_sizes, marker='o')  # 'o' 是点标记

    # 设置图表标题和坐标轴标签
    plt.title('File Size Trend')
    plt.xlabel('Record Data')
    plt.ylabel('File Size')

    # 显示网格
    plt.grid(True)

    # 显示图例
    plt.legend(['File Size'])

    # 显示图表
    plt.show()    

# 主函数
def main():
    read_data_weekly('./READEME.md ')
    pass

if __name__ == '__main__':
    main()

