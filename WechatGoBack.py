# -*- coding: utf-8 -*-
import re
import os
import time
import itchat
from itchat.content import TEXT, FRIENDS, ATTACHMENT, VIDEO, RECORDING, PICTURE, CARD, MAP, SHARING, NOTE

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
                    group_name = group['NickName']
                    group_member = group['MemberCount']
                    break
            if not group_name:
                group_name = u'未命名群聊'
            group_name = group_name + u'(%s)人' % str(group_member)
            msg_from = group_name + '-->' + msg_from
        else:
            try:
                msg_from = itchat.search_friends(userName=msg['FromUserName'])['RemarkName']
                if not msg_from:
                    msg_from = itchat.search_friends(userName=msg['FromUserName'])['NickName']
            except:
                msg_from = u'微信官方消息'
        msg_send_time = msg['CreateTime']
        msg_id = msg['MsgId']
        msg_content = None
        msg_link = None
        if msg['Type'] == 'Text' or msg['Type'] == 'Friends':
               msg_content = msg['Text']
               print('[TEXT/FRIENDS]:%S' % msg_content)
        elif msg['Type'] == 'ATTACHMENT' or msg['Type'] == 'VIDEO' or msg['Type'] == 'RECORDING' or msg['Type'] == 'PICTURE':
                msg_content = msg['FileName']
                msg['Text'](str(msg_content))
                print('[Attachment/Video/Picture/Recording]: %s' % msg_content)
                p=1

if __name__ == '__main__':
    test = WechatGoBack()
    test.run()