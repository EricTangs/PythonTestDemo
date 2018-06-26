import re
import json
from bs4 import BeautifulSoup
from urllib import request, parse

if __name__ == '__main__':
    ip = 'http://www.iqiyi.com/v_19rrb2yq04.html?fc=8b62d5327a54411b#vfrm=19-9-0-1'
    get_url = 'http://www.sfsft.com/index.php?url=%s' % ip

    get_movie_url = 'http://www.sfsft.com/api.php'

    head = {
        'User-Agent':'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19',
        'Referer':'http://www.sfsft.com/index.php?url=%s' % ip
    }

    get_url_req = request.Request(url = get_url, headers = head)
    get_url_response = request.urlopen(get_url_req)

    get_url_html = get_url_response.read().decode('utf-8')
    print("html:")
    print(get_url_html)
    bf = BeautifulSoup(get_url_html, 'lxml')
    print(bf.body.script.next_sibling.string)
    a = str(bf.find_all('script'))
    print(">>>a:")
    print(a)
    pattern = re.compile("url : '(.+)',", re.IGNORECASE)
    print(pattern)
    url = pattern.findall(a)[0]

    get_movie_data = {
        'up':'0',
        'url':'%s' % url,
    }
    get_movie_req = request.Request(url = get_movie_url, headers = head)
    get_movie_data = parse.urlencode(get_movie_data).encode('utf-8')
    get_movie_response = request.urlopen(get_movie_req, get_movie_data)
    get_movie_html = get_movie_response.read().decode('utf-8')
    print(get_movie_data['url'])