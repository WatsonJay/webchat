# -*- coding: utf-8 -*-
import re
import os
import time
import itchat
from itchat.content import TEXT, PICTURE, FRIENDS, CARD, MAP, SHARING, RECORDING, ATTACHMENT, VIDEO, NOTE

MSGINFO = {}
FACEPACKAGE = None

class WechatGoBack():
    def __init__(self, **kwargs):
        self.info = 'antiWithdrawal'
        self.options = kwargs
    #用于调用的函数
    def run(self):
        try:
            itchat.auto_login(hotReload=True)
        except:
            itchat.auto_login(hotReload=True, enableCmdQR=True)
        itchat.run()
    #处理接受到的消息
    @itchat.msg_register([TEXT, PICTURE, FRIENDS, CARD, MAP, SHARING, RECORDING, ATTACHMENT, VIDEO, NOTE], isFriendChat=True, isGroupChat=True, isMpChat=True)
    def saveReceiveMsg(msg):
        msg_receive_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if 'ActualNickName' in msg :
            msg_from_nickname = msg['ActualNickName']
            msg_from = msg_from_nickname
            msg_from_username = msg['ActualUserName']
            friends = itchat.get_friends(update=True)
            for friend in friends:
                if msg_from_nickname == friend['UserName']:
                    if friend['RemarkName']:
                        msg_from = friend['RemarkName']
                    else:
                        msg_from = friend['NickName']
            groups = itchat.get_chatrooms(update=True)
            for group in groups:
                if msg['FromUserName'] == group['UserName']:
                    p=1
if __name__ == '__main__':
    test = WechatGoBack()
    test.run()