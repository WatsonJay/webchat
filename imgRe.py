# -*- coding: utf-8 -*-
import requests
global s
s = requests.session()


def imgRe(photo_url):
    url = "https://api-cn.faceplusplus.com/facepp/v3/detect"
    data= {"api_key":"1GCVYIgh3BF0MGSG6aXuCAKmJKpW9Q7t",
          "api_secret":"aBs1Il2WSG9Dg8xPlwkf-latRVGC0fsM" ,
          "image_url": photo_url,
          "return_attributes":"gender,age,beauty"}
    r = s.post(url, data=data)
    j = eval(r.text)
    result = j['faces'][0]['attributes']
    if result['gender']['value'] == 'Male':
        sex='男性'
        beauty=result['beauty']['male_score']
    if result['gender']['value'] == 'Female':
        sex='女性'
        beauty = result['beauty']['female_score']
    datas = [sex, str(result['age']['value']),str(beauty)]
    return datas
