from urllib.parse import urlencode
from requests.exceptions import RequestException
from json.decoder import JSONDecodeError
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from hashlib import md5
import os, sys
from config import *
import pymongo
import requests
import json
import re

'''
client = pymongo.MongoClient(MONGO_URL)
# 数据库要用[]号
db = client[MONGO_DB]
'''

'''
def save_to_mongo(result):
    print("Save Result:", result)
    if db[MONGO_TABLE].insert(result):
        print("存储到MongoDB成功", result)
        return True
    return False
'''


def download_image(url, key_word):
    print('正在下载', url)
    try:
        respose = requests.get(url, stream=True)
        if respose.status_code == 200:
            # return respose.text
            save_image(respose.content, key_word)
        return None
    except RequestException:
        print("请求图片出错", url)
        return None


def save_image(content, key_word):
    print(md5(content).hexdigest())
    md5_value = md5(content).hexdigest()
    if md5_value:
        file_path = 'F:\\TouTiao\%s\%s.%s' % (key_word, md5_value, 'jpg')
        file_doc = 'F:\\TouTiao\%s' % (key_word)
        if not os.path.exists(file_doc):
            os.makedirs(file_doc)
        print(file_path)
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()
            print('saved%s.%s', md5_value, 'jpg')


def get_one_index(offset, keyword):
    '''
    获取搜索页面
    :param offset: 偏移
    :param keyword: 关键词
    :return: html
    '''
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': '1'
    }
    # urlenncode将字典转成URL形式
    url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
    try:
        respose = requests.get(url)
        # 注意判断,状态为200时为成功
        if respose.status_code == 200:
            return respose.text
        return None
    except RequestException:
        print('请求索引页出错!')
        return None


def parse_one_page(text):
    '''
    解析网页获取地址
    :param text:json数据
    :return:详情页地址
    '''
    try:
        data = json.loads(text)
        if data and 'data' in data.keys():
            for item in data.get('data'):
                yield item.get('url')
    except JSONDecodeError:
        pass


def get_page_detail(url, header):
    '''
    获取详情页
    :param url: 地址
    :return: 内容
    '''
    try:
        respose = requests.get(url=url, headers=header)
        if respose.status_code == 200:
            return respose.text
        return None
    except RequestException:
        print('请求详情页出错!')
        return None


def parse_page_detail(html, request_url, key_word):
    soup = BeautifulSoup(html, 'lxml')
    if soup.head.title:
        title = soup.head.title.string
    else:
        title = '获取失败!'
    print("Title:", title)
    article_info_parttern = re.compile('articleInfo: \{(.*?)}', re.S)
    url_parttern = re.compile('&quot;http(.*?)&', re.S)
    result = re.search(article_info_parttern, html)
    if not result:
        return None
    url_list = []
    for url in re.findall(url_parttern, result.group(1)):
        url_list.append('http' + url)
    if url_list:
        for image in url_list: download_image(image, key_word)
        return {
            'title': title,
            'url': request_url,
            'images_url': url_list
        }


def get_image(page, key_word):
    main_html = get_one_index(page * 20, key_word)
    headers = {"User-Agent": UserAgent().chrome}
    print("HEADER:", headers)
    for url in parse_one_page(main_html):
        print("单的页面:", url)
        html_info = get_page_detail(url, headers)
        if html_info:
            result = parse_page_detail(html_info, url, key_word)
            print("Result:", result)
            # save_to_mongo(result)


if __name__ == '__main__':
    request_image_list = ['校花','波多野结衣','AV女星','街拍', '美女', '模特', '车模']
    for key_word in request_image_list:
        i = 0
        while i < 5:
            get_image(i, key_word)
            i += 1
