# step1 访问网站获取response
# step2 获取html内文件内容 Page数 标题 tag等
# step3 获取txt内容并存储
import concurrent.futures
import os.path
import threading

import requests
from bs4 import BeautifulSoup
import gzip
from io import BytesIO
import  re

base_url = 'https:///{}.html'
next_base_url = 'https:///news/{}_{}.html'

begin = 0
end = 1

def del_text_blank_line(text):
    text = "\n".join([line for line in text.split("\n") if line.strip()])

    lines = text.split("\n")
    text = "\n".join(lines[:-4])
    return text


def get_next_text_content(html, idx, filepath):
    soup = BeautifulSoup(html, "html.parser")
    # get text
    div_element = soup.find('div', class_='wodetupian a{} suit'.format(idx))

    if div_element:
        div_content = div_element.text
        div_content = del_text_blank_line(div_content)
    else:
        print("{} text not found".format(idx))

    with open(filepath, 'a') as file:
        file.write(div_content)



def get_next_text(idx, num, filepath):
    print(idx, num, filepath)
    print("hi i am here\n")
    for index in range(2, num):
        target_url = next_base_url.format(idx, index)
        print(target_url + "Hi i am here\n")
        try:
            response = requests.get(target_url,  verify=False)
        except requests.exceptions.RequestException as e:
            print("An error occurred while makeing the request:{e}")
            continue
        if response.status_code != 200:
            print(target_url + "failed\n")
            continue
        response.encoding = 'utf-8'
        decode_data = response.content.decode('utf-8')
        get_next_text_content(decode_data, idx, filepath)




def get_text(html, idx):
    soup = BeautifulSoup(html, "html.parser")


    # get title
    title_element = soup.find('title')
    if title_element:
        title_text = title_element.text
    else:
        print("{}not found".format(idx))

    # get text
    div_element = soup.find('div', class_='wodetupian a{} suit'.format(idx))

    if div_element:
        div_content = div_element.text
        div_content = del_text_blank_line(div_content)
    else:
        print("{} text not found".format(idx))

    # 获取后续的page
    page_element = soup.find('div', class_="hy-page clearfix")

    if page_element:
        page_content = page_element.text
    else:
        print("{} page text not found".format(idx))

    match = re.search(r'共(\d+)页', page_content)

    if match:
        num = int(match.group(1))
        print(num)
    else:
        print(" {} not found page num".format(idx))
        return None

    directory = "Paper"
    if not os.path.exists(directory):
        os.mkdir(directory)

    filename = title_text + ".txt"

    file_path = os.path.join(directory, filename)
    with open(file_path, 'w') as file:
        file.write(div_content)

    # 获取后续的内容 并输入到同一个txt中
    get_next_text(idx, num, file_path)

def decode_html(response):
    if response.headers.get("Content-Encoding") == "gzip":
        compress_data = BytesIO(response.content)
        decompress_data = gzip.GzipFile(fileobj=compress_data).read()
        decode_data = decompress_data.decode("utf-8")
        print(decode_data)
    else:
        print("failed")


def single_paper(idx):
    target_url = base_url.format(idx)
    print(target_url)
    try:
        response = requests.get(target_url)
    except requests.exceptions.RequestException as e:
        print("An error occurred {e}")
    response.encoding = 'utf-8'
    decode_data = response.content.decode('utf-8')
    get_text(decode_data, idx)

def core(begin, end):
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        for idx in range(begin, end):
            executor.submit(single_paper, idx);


core(begin, end)