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
        self.info = 'WechatGoBack'
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
                if msg_from_username == friend['UserName']:
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
               print('[TEXT/FRIENDS]:%s' % msg_content)
        elif msg['Type'] == 'ATTACHMENT' or msg['Type'] == 'VIDEO' or msg['Type'] == 'RECORDING' or msg['Type'] == 'PICTURE':
                msg_content = msg['FileName']
                msg['Text'](str(msg_content))
                print('[Attachment/Video/Picture/Recording]: %s' % msg_content)
        # 位置信息
        elif msg['Type'] == 'Map':
            x, y, location = re.search("<location x=\"(.*?)\" y=\"(.*?)\".*label=\"(.*?)\".*", msg['OriContent']).group(1,2,3)
            if location is None:
                msg_content = r"纬度:" + x.__str__() + ", 经度:" + y.__str__()
            else:
                msg_content = r"" + location
            print('[Map]: %s' % msg_content)
        # 分享的音乐/文章
        elif msg['Type'] == 'Sharing':
            msg_content = msg['Text']
            msg_link = msg['Url']
            print('[Sharing]: %s' % msg_content)
        FACEPACKAGE = msg_content
        MSGINFO.update(
            {
                msg_id:{
                    "msg_from":msg_from,
                    "msg_send_time":msg_send_time,
                    "msg_receive_time":msg_receive_time,
                    "msg_type":msg['Type'],
                    "msg_content":msg_content,
                    "msg_link": msg_link
                }
            }
        )
        WechatGoBack.checkMsgInfo()

    #监听是否有消息撤回
    @itchat.msg_register(NOTE, isFriendChat=True, isGroupChat=True, isMpChat=True)
    def monitorMsg(msg):
        if u'撤回了一条消息' in msg['Content']:
            callBack_msg_id = re.search("\<msgid\>(.*?)\<\/msgid\>",msg['Content']).group(1)
            callBack_msg = MSGINFO.get(callBack_msg_id)
            if len(callBack_msg_id) < 11:
                itchat.send_file(FACEPACKAGE, toUserName='filehelper')
            else:
                prompt = u'+++' + callBack_msg.get('msg_from') + u'撤回了一条消息+++\n' \
                                u'--消息类型：' + callBack_msg.get('msg_type') + '\n' \
                                u'--接收时间：' + callBack_msg.get('msg_receive_time') + '\n' \
                                u'--消息内容：' + callBack_msg.get('msg_content')
                if callBack_msg['msg_type'] == 'Sharing':
                    prompt += u'\n链接：' + callBack_msg.get('msg_link')
                itchat.send_msg(prompt, toUserName='filehelper')
                if callBack_msg['msg_type'] == 'Attachment' or callBack_msg['msg_type'] == "Video" or callBack_msg['msg_type'] == 'Picture' or callBack_msg['msg_type'] == 'Recording':
                    file = '@fil@%s' % (callBack_msg['msg_content'])
                    itchat.send(msg=file, toUserName='filehelper')
                    os.remove(callBack_msg['msg_content'])
                MSGINFO.pop(callBack_msg)

    @staticmethod
    def checkMsgInfo():
        need_del_msgs = []
        for msg in MSGINFO:
            msg_time_stay = int(time.time()) - MSGINFO[msg]['msg_send_time']
            if msg_time_stay > 180:
                need_del_msgs.append(msg)
        if need_del_msgs:
            for msg in need_del_msgs:
                MSGINFO.pop(msg)
if __name__ == '__main__':
    test = WechatGoBack()
    test.run()