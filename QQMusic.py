# -*- coding: utf-8 -*-
import requests
import urllib

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'
}

def music(title):
    text=urllib.quote(title)
    url='https://api.bzqll.com/music/tencent/search?key=579621905&s='+text+'&limit=1&offset=0&type=song'
    data = requests.get(url,headers=headers)
    request = eval(data.text)
    try:
        data = request['data'][0]
        reurl = data['url']
        retitle = data['name']
        pic = data['pic']
        returnData = [retitle,reurl,pic]
        return returnData
    except Exception :
        return 'error'
if __name__ == '__main__':
    music('爱你没差')