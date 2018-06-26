from urllib import request,parse
get_movie_data = {
        "authcookie":"",
        "antiCsrf":"37a6259cc0c1dae299a7866489dff0bd",
        "agenttype":"1",
        "fields":"qiyi_tennis_vip,r,userinfo,qiyi_vip,pps,accounts,tokens,v,insecure_account,ablogin",
    }

if __name__=='__main__':
    get_movie_response = request.urlopen("https://passport.iqiyi.com/apis/user/info/queryWithVerify.action", get_movie_data)
    get_movie_html = get_movie_response.read().decode('utf-8')
    print(get_movie_data['url'])