import json
import os.path
import threading
import requests
from bs4 import BeautifulSoup

## step1: 伪造登录获取cookie
## step2: 带着cookie访问遍历id的html
## 这里因为网页设计分为两步 第一步先获取到dplayer对应的url
## 然后拼接成下一个获取对应的m3u8地址
headers = {
    'Accept' : '',
    'Host': '',
    'Origin': 'http://.com',
    'Accept-Encoding': '',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Proxy-Connection': 'keep-alive',
    'Referer': '',
    'User-Agent': '',
    'Cookie' : ''
}

base_url = ''
player_url = ''

### 循环获取页面

begin_val = 53000
end_val   = 54000

def get_js_var(html, var_name):
    soup = BeautifulSoup(html, 'html.parser')
    script_tags = soup.find_all('script')

    for script_tag in script_tags:
        script_content = script_tag.string
        if script_content == None :
            continue
        if len(script_content) > 1000 :
            continue
        if len(script_content) <= 300 :
            continue
        print(script_content)
        return script_content
        # pattern = r'var {}="(.*?)"'.format(var_name)
        # match = re.search(pattern, script_content)
        # if match and match.group(1):
        #     print(match.group(1))
    return None

def parse_js_var(var_string):
    if var_string == None:
        return None
    json_start = var_string.find('{')
    json_end   = var_string.rfind('}')
    json_string = var_string[json_start : json_end + 1]
    try:
        json_data = json.loads(json_string)
        print(json_data)
        return json_data
    except json.JSONDecodeError:
        return None

def extract_url_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    #查找所有的<script>标签
    script_tags = soup.find_all('script')

    for script_tag in script_tags:
        #获取script标签文本内容
        script_content = script_tag.string

        if script_content:
            #检查是否包含 var url
            if 'var urls' in script_content:
                start_index = script_content.index('var urls') + len('var urls') + 1
                end_index   = script_content.index(';', start_index)
                url = script_content[start_index + 3: end_index - 1]
                return url
    return None


def write_to_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)

def core(begin_val, end_val):
    for index in range(begin_val, end_val):
        url = base_url.format(index)
        ## 发第一个请求
        response_first = requests.get(url, headers=headers)

        ## 查找具有特定id和class的div元素
        html_first = response_first.text
        player = get_js_var(html_first, '')
        json_data = parse_js_var(player)
        if json_data == None:
            continue
        vod_data = json_data['vod_data']
        vod_name = vod_data['vod_name']
        vod_actor = vod_data['vod_actor']
        vod_class = vod_data['vod_class']
        new_url = player_url.format(json_data['url'])
        ## 发第二个请求
        response_second = requests.get(new_url, headers=headers)
        m3u8 = extract_url_from_html(response_second.text)
        if m3u8 == None:
            continue
        ## 写入到文件中
        subfolder = ''
        vod_sum = vod_actor + ' ' + vod_class + ' ' + vod_name
        filename = os.path.join(subfolder, vod_sum)
        write_to_file(filename, m3u8)
        # time.sleep(1)


threads = []
begin_index = 1
for i in range(40):
    t = threading.Thread(target=core, args=(begin_index , begin_index + 250))
    print(begin_index)
    begin_index += 250
    threads.append(t)
    t.start()

for t in threads:
    t.join()







