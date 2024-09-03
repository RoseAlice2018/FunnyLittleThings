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
