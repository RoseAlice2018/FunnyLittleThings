## 爬取xxx网站的文章并分类保存

### How to Use
```commandline
base_url = 'https:///{}.html'
next_base_url = 'https:///news/{}_{}.html'
```
- 填写baseUrl和 next_base_url 

```python
def core
```
- 核心函数，按begin to end 通过线程池并行执行文章内容下载

```python
single_paper 
--->
get_text
---> 如果有下一页
get_next_text
```

- 逻辑如上，获取单页内容，如果有下一页依次获取下一页内容