import requests
import re
import json
import urllib.parse
import shutil

url="https://www.youtube.com/watch?v=b57XVkLADaM"
res =requests.get("https://www.youtube.com/watch?v=iW2yUrXXRTI")
m=re.search('"args":({.*?}),',res.text)
print(m.group(1))
json_default=m.group(1).replace("\\","")
print("------------------------")
print(json_default)
print(type(json_default))
print("------------------------")
json_data=json.loads(json_default)
print(json_data)
a=urllib.parse(json_data["url_encoded_fmt_stream_map"])

print(json_data["url_encoded_fmt_stream_map"])
res2=requests.get(a['url'][0],stream=True)
f=open('a.mp4','wb')
shutil.copyfileobj(res.raw,f)
f.close()

