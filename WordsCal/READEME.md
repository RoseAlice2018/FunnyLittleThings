## 需求
1. 每日新增字节数
    1.1 文件已经存在，计算差值即可 （Today- Yesterday）
    1.2 文件新建， 昨日值计为0 
    1.3 每日新增字节数记入数据库中
2. 每周新增字节数
    1.1 以自然周为计算标准 如8.19-8.25为一周
    1.2 计算一周新增字节数（对比Weekyly的差值）
    1.3 每周新增字节数记入数据库中
3. 每月新增字节数
    基本同上
4. 删除文件不记录为负数 只计算新增字节数
5. 暂不支持移动文件（二期需求）

## 功能
1. 实现每日，每周，每月的开发和文档增量数据统计
2. 一个合理和美观的展现方式
3. 可以配置指定的文件夹和分文件夹展示
4. 支持功能插件
## 表格设计
1. WordsCal Table
```
CREATE TABLE WORDSCAL(
    file_id INT AUTO_INCREMENT PRIMARY KEY,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(1024),
    record_date DATE NOT NULL,
    file_size BIGINT UNSIGNED NOT NULL,
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP 
)ENGINE=InnoDB;
```
## 目录结构
1. calspy
- 展现数据的python文件
2. config
- 配置目录
3. 主目录
- main.py

## 自动化执行
```
crontab -e
在末尾追加
0 8 * * * /path/to/your/main_program  // 每天早上八点执行main
systemctl restart cron // 重启服务
```

## Update记录
```
9.11
- 完成makefile编译

9.12 
- main文件跑通流程 完成对文件的遍历和插入mysql数据库
- 实现文件path的配置
9.13
- 读取数据库实现每周曲线绘制
9.18
- 测试整个流程
- 实现filename自动读取生成
- 实现filename指定生成path
9.19
- main文件遍历时提供跳过指定文件夹和文件功能(下个版本优化)
- python遍历展示图片提供指令操纵(下个版本优化)
- 优化Readme 
- 优化配置文件
- 自动化全流程
9.20
- main文件遍历提供跳过指定文件和文件夹功能
- python读取配置实现指令操控
- 自动化流程
9.23
- 拆分图片展示，展示为全部文件，同时下面区分每个文件的增量
- main程序自动化执行
10.08
- 修复跳过config指定文件夹失败的问题
- 清除一些cals.py的错误，优化图表结构。

10.09
- 

```

