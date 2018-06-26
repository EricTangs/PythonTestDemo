import urllib
from urllib import request, parse
import re
import threadpool
import queue
from threading import Thread
import threading
import time


def get_tieba_listnumber(name):
    try:
        url = "http://tieba.baidu.com/f?"
        head = {
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"}
        word = {"kw": name}
        word = parse.urlencode(word)
        url = url + word
        requests = request.Request(url=url, headers=head)
        requests.add_header("Connection", "keep-alive")
        respose = request.urlopen(requests)
        data = respose.read().decode('utf-8')
        restr_card = "<span class=\"card_menNum\">([\s\S]*?)</span>"
        regex = re.compile(restr_card, re.IGNORECASE)
        mylist_card = regex.findall(data)
        card_num = mylist_card[0].replace(",", "")
        restr_talk = "<span class=\"card_infoNum\">([\s\S]*?)</span>"
        regex_talk = re.compile(restr_talk, re.IGNORECASE)
        mylist_talk = regex_talk.findall(data)
        talk_num = mylist_talk[0].replace(",", "")
        return card_num, talk_num
    except:
        print("解析异常")


def get_tieba_list(name):
    try:
        number_tuples = get_tieba_listnumber(name)
        word = {"kw": name}
        name_decode = parse.urlencode(word)
        talk_num = eval(number_tuples[1])
        tieba_list = []
        if talk_num % 50 == 0:
            for i in range(talk_num // 50):
                tieba_list.append("http://tieba.baidu.com/f?" + name_decode + "&ie=utf-8&pn=" + str(i * 50))
        else:
            for i in range(talk_num // 50 + 1):
                tieba_list.append("http://tieba.baidu.com/f?" + name_decode + "&ie=utf-8&pn=" + str(i * 50))
        return tieba_list
    except:
        print("解析错误")


def get_url_list_from_page(url=""):
    """
    获得当前页面的主贴页面
    :param url:当前页的url
    :return:所有子主贴
    """
    try:
        head = {
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"}
        requests = request.Request(url=url, headers=head)
        requests.add_header("Connection", "keep-alive")
        respose = request.urlopen(requests)
        data = respose.read().decode('utf-8')
        restr_card = "<div id=\"pagelet_frs-list/pagelet/thread_list\">([\s\S]*?)<div class=\"thread_list_bottom clearfix\">"
        regex = re.compile(restr_card, re.IGNORECASE)
        mylist_card = regex.findall(data)  # 抓取整个表格
        url_list = []  # 子贴的url列表
        restr_single = "href=\"/p/(\d+)\""
        regex = re.compile(restr_single, re.IGNORECASE)
        data = mylist_card[0]
        mylist = regex.findall(data)  # 抓取单个链接
        for i in mylist:
            url_list.append("http://tieba.baidu.com/p/" + i)
        return url_list
    except:
        print("解析异常")


def get_totalpage_detail_list(url):
    """
    获取该讨论的每一页的链接
    :param url: 该页面的首页地址
    :return:该讨论的所有页的链接
    """
    try:
        head = {
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"}
        requests = request.Request(url=url, headers=head)
        requests.add_header("Connection", "keep-alive")
        respose = request.urlopen(requests)
        data = respose.read().decode('utf-8')
        restr = "<span class=\"red\">(\d+)</span>"
        regex = re.compile(restr, re.IGNORECASE)
        totalpage = eval(regex.findall(data)[0])
        mylist = []
        print(totalpage)
        for i in range(0, totalpage + 1):
            mylist.append(url + "?pn=" + str(i))
        return mylist
    except:
        print("解析异常")


def all_talk_word_singlepage(url):
    try:
        head = {
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"}
        requests = request.Request(url=url, headers=head)
        requests.add_header("Connection", "keep-alive")
        respose = request.urlopen(requests)
        data = respose.read().decode('utf-8')
        all_word = ""
        all_word = all_word + get_post_word(data)
        return all_word
    except:
        print("解析错误")


def get_main_word(data):
    """
    获取主话题
    :param data:
    :return:
    """
    restr = "<h1 class=\"core_title_txt  \" title=\"([\s\S]*?)"
    regex = re.compile(restr, re.IGNORECASE)
    mylist = regex.findall(data)
    dr = re.compile(r'<[^>]+>', re.IGNORECASE)
    str = " "
    for i in mylist:
        str = str + dr.sub('', i)
    return str


def get_post_word(data):
    """
    获取主对话
    :param data:网页数据
    :return: 当前数据所有对话的字符串
    """
    try:
        restr = "class=\"d_post_content j_d_post_content  clearfix\">([\s\S]*?)</div>"
        regex = re.compile(restr, re.IGNORECASE)
        mylist = regex.findall(data)
        dr = re.compile(r'<[^>]+>', re.IGNORECASE)
        str = " "
        for i in mylist:
            str = str + dr.sub('', i)
        print(str)
        return str
    except:
        print("解析异常")


def get_reply_word(data):
    """
    返回当前回话数据的字符串
    :param data: 网页数据
    :return: 当前数据所有回话的字符串
    """
    try:
        restr = "class=\"lzl_content_main\">([\s\S]*?)</span>"
        regex = re.compile(restr, re.IGNORECASE)
        mylist = regex.findall(data)
        dr = re.compile(r'<[^>]+>', re.IGNORECASE)
        str = " "
        for i in mylist:
            str = " " + str + dr.sub('', i)
        return str
    except:
        print("解析异常")


def get_all_talk_word(name, path):
    try:
        mylist = get_tieba_list(name)
        try:
            for i in mylist:
                list = get_url_list_from_page(i)
                try:
                    for a in list:
                        mylist1 = get_totalpage_detail_list(a)
                        try:
                            for j in mylist1:
                                all_word = " " + all_talk_word_singlepage(j)
                                save_file(all_word, path)
                        except:
                            pass
                except:
                    pass
        except:
            pass
    except:
        print("发生错误")


'''
                    try:
                requests = threadpool.makeRequests(threadpool_getword, mylist)
                [pool.putRequest(req) for req in requests]
            except:
                print("发生错误")
            '''


def save_file(str, path):
    try:
        savefile = open(path, "a", encoding='utf-8')
        savefile.write(str)
    except:
        print("保存出错")


def threadpool_getword(i):
    list = get_url_list_from_page(i)
    try:
        for a in list:
            mylist1 = get_totalpage_detail_list(a)
            try:
                all_word = " " + all_talk_word_singlepage(j)
                for j in mylist1:
                    time.sleep(.1)
                    thread_lock.acquire()
                    word_queue.put(all_word)
                    thread_lock.release()
            except:
                pass
    except:
        pass


def save_text_thread():
    '''
    保存文本线程
    :return:
    '''
    while True:
        time.sleep(.1)
        if thread_lock.acquire():
            if (word_queue.empty()):
                print("wordqueue is null")
                thread_lock.release()
            else:
                word = word_queue.get()
                save_file(word, path)


path = "湖南科技学院.txt"  # 存储路径
word_queue = queue.Queue()  # 对话队列
thread_lock = threading.Lock()  # 线程锁
pool = threadpool.ThreadPool(10)  # 线程池
if __name__ == '__main__':
    # threading._start_new_thread(save_text_thread, ())
    get_all_talk_word("湖南科技学院", path)
