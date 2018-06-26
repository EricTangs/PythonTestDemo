from bs4 import BeautifulSoup
from urllib.request import  urlopen
html=urlopen("https://wannianrili.51240.com/").read().decode('utf-8')
soup=BeautifulSoup(html,features='lxml')
main_title=soup.head.find('div', {"id":"main_title"})
ahref=main_title.find_all('a')
print(ahref)
