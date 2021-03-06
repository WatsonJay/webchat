# -*- coding: utf-8 -*-
import sys

import itchat
import jieba
from itchat.content import TEXT, FRIENDS, ATTACHMENT, VIDEO, RECORDING, PICTURE, CARD, MAP, SHARING, NOTE

reload(sys)
sys.setdefaultencoding( "utf-8" )

WARNING_KEYWORDS = [
    u"钢铁侠",
    u"铁人",
    u"铁罐",
    u"iron",
    u"man",
    u"小蜘蛛",
    u"绿巨人",
    u"鹰眼",
    u"美队",
    u"tony",
    u"stack",
    u"复联",
    u"复仇者",
    u"妇联",
    u"黑寡妇",
    u"灭霸",
    u"奇异博士",
]

WARNING_REPLY = u"""觉得有关复联4，我就无聊的清个屏!!
\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n
"""

def check_msg(msg):
    keyword_list = jieba.cut(msg)
    for word in keyword_list:
        if word in WARNING_KEYWORDS:
            return True
    return False

@itchat.msg_register([TEXT, PICTURE, FRIENDS, CARD, MAP, SHARING, RECORDING, ATTACHMENT, VIDEO, NOTE], isFriendChat=True, isGroupChat=True, isMpChat=True)
def text_replay(msg):
    if 'ActualNickName' in msg:
        msg_from_nickname = msg['ActualNickName']
        groups = itchat.get_chatrooms(update=True)
        for group in groups:
            if msg['FromUserName'] == group['UserName'] and group['NickName'] == '谁是谁的谁':
                if check_msg(msg.text):
                    print(u"WARNING! 这条消息涉嫌剧透,现已自动屏蔽 FROM：{}".format(group['NickName']+'的'+msg_from_nickname))
                    # return WARNING_REPLY

if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    itchat.run()