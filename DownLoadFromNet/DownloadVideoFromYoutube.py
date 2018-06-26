import requests
respose=requests.get("http://maoyan.com/board/4?")
print(respose.text)