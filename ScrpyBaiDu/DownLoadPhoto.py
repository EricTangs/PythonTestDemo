import requests
from bs4 import BeautifulSoup
path="E:\Art\Leader\\"
url="http://www.ngchina.com.cn/animals/"
html=requests.get(url).text
soup=BeautifulSoup(html,'lxml')
print(soup)
img_url=soup.find_all('ul',{"class":"img_list"})
print(len(img_url))

for ul in img_url:
    imgs=ul.find_all('img')
    for img in imgs:
        url=img['src']
        r=requests.get(url,stream=True)
        image_name=url.split('/')[-1]
        with open(path+image_name,'wb') as f:
            for chunk in r.iter_content(chunk_size=128):
                f.write(chunk)
        print('Saved %s'%image_name)