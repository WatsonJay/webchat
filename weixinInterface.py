# -*- coding: utf-8 -*-
import hashlib
import web
from lxml import etree
import time
import os
from imgRe import imgRe
from webchat import talk

class WeixinInterface:

    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        try:
            # 获取输入参数
            data = web.input()
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            # 自己的token
            token = "Jaywatson1994"  # 这里改写你在微信公众平台里输入的token
            # 字典序排序
            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            # sha1加密算法

            # 如果是来自微信的请求，则回复echostr
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception as Argument:
            return Argument

    def POST(self):
        try:
            str_xml = web.data()  # 获得post来的数据
            xml = etree.fromstring(str_xml)  # 进行XML解析
            msgType = xml.find("MsgType").text
            fromUser = xml.find("FromUserName").text
            toUser = xml.find("ToUserName").text
            userid = fromUser[0:15]
            if msgType == 'image':
                try:
                    picurl = xml.find('PicUrl').text
                    picResult = imgRe(picurl)
                    return self.render.reply_text(fromUser, toUser, int(time.time()),
                                                  '图中人物性别为' + picResult[0] + '\n' + '年龄为' + picResult[
                                                      1] + '岁\n' + '颜值为' + picResult[2] + '分')
                except:
                    return self.render.reply_text(fromUser, toUser, int(time.time()),'识别失败，换张图片试试吧')
            elif msgType == 'text':
                content = xml.find("Content").text  # 获得用户所输入的内容
                if content[0:4] == u"自我介绍":
                    return self.render.reply_text(fromUser, toUser, int(time.time()), '我叫小小肥仔，我被我的主人扔在这里，我会陪你聊天，还会看图认脸看地图等等，把我抱走吧，对了，我家在www.nothingistrue.top哦')
                else :
                    try:
                        msg = talk(content, userid)
                        return self.render.reply_text(fromUser,toUser,int(time.time()), msg)
                    except:
                        return self.render.reply_text(fromUser,toUser,int(time.time()), content + '这货还不够聪明，换句话聊天吧')
            elif msgType == 'voice':
                content = xml.find("Recognition").text  # 获得用户语音的内容
                try:
                    msg = talk(content, userid)
                    return self.render.reply_text(fromUser, toUser, int(time.time()), msg)
                except:
                    return self.render.reply_text(fromUser, toUser, int(time.time()), content + '这货还不够聪明，换句话聊天吧')
            else:
                return self.render.reply_text(fromUser, toUser, int(time.time()), '我还没学会看懂这个东西')
        except Exception as Argument:
            return Argument