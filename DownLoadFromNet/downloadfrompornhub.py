import requests
from fake_useragent import UserAgent
headers = {"User-Agent": UserAgent().chrome}
respose = requests.get(url='https://services.pornhub.com/chronopop/131887851/105',headers=headers)
with open("F:\\vpornhub.mp4",'wb') as f:
    f.write(respose.content)
    f.close()
    print('finished')
