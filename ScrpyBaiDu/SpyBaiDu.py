from bs4 import BeautifulSoup
from  urllib.request import urlopen
import urllib
import urllib.parse
import re #正则表达式
import random\

#获取url编码
def get_url(url_str):
    return urllib.parse.quote(url_str)

url="https://baike.baidu.com/item/%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB/5162711?fr=aladdin"
print(get_url(url))

base_url="https://baike.baidu.com/"
data=urllib.parse.quote("网络爬虫")
url_str="item/"+data+"/5162711?fr=aladdin"
his=[url_str]
url=base_url+his[-1]
html=urlopen(url).read().decode('utf-8')
soup=BeautifulSoup(html,features='lxml')
sub_urls=soup.find_all("a",{"target":"_blank","href":re.compile("/item/(%.{2})+$")})
if len(sub_urls)!=0:
    his.append(random.sample(sub_urls,1)[0]['href'])
else:
    his.pop()
print(his)
