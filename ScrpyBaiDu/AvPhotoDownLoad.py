import requests
from bs4 import BeautifulSoup
#proxies={"https":"https://104.17.81.25:443"}

web_url='https://www.gavbus.com/'
path='E:\Art\AV\\'

#获取URL想要的url
def get_allurl(url,tag,list):
    html=requests.get(url).text
    soup = BeautifulSoup(html,'lxml')
    #url 列表
    return soup.find_all(tag,list)

def get_allurl_bytag(soup,tag):
    return soup.find_all(tag)

#下载资源
def download_source(path,url):
    image_name = url.split('/')[-1]
    print(image_name)
    print(url)
    r=requests.get(url,stream=True)
    with open(path + image_name, 'wb') as f:
        for chunk in r.iter_content(chunk_size=128):
            f.write(chunk)
    print('Saved %s'% image_name +' Success!')

#获得url_soup
url_soup=get_allurl(web_url,'div',{"class":"photo-frame"})
for ul in url_soup:
    #print(ul)
    img_soup = get_allurl_bytag(ul,'img')
    #print(img_soup)
    for img_url in img_soup:
        print(img_url['src'])
        print('\n')

        download_source(path,'https:'+img_url['src'])
