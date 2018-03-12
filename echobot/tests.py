# from linebot import LineBotApi
# from linebot.models import *
#
# line_bot_api = LineBotApi('3Hn3QKR+1nWt/DzpON4N+wGUXv/ne3/fR0zXTZmN4Zm60p3Eh1VGImUXRir6w41LQW01fU/r59PKSKsKFhZ+Nlo8CyHn+v/vhdcyngnh595kfBmgmjw3IIOfCJE5gjRU614lMKTfq4VfuGAHZc0UIAdB04t89/1O/w1cDnyilFU=')
#
#
# line_bot_api.push_message('U453eacd40482c951f5b40b2b2b60b5ca', ImageSendMessage(original_content_url = 'https://i.imgur.com/8vgC03Q.jpg', preview_image_url = 'https://i.imgur.com/8vgC03Q.jpg'))
#
# #
#
# import pymysql
#
# db = pymysql.connect(host="127.0.0.1", user="root", password="", db="linebot", port=3306)
# cur = db.cursor()
#
# userID = 555555
# TimeStamp = 674645
#
# sql_add = "INSERT INTO `user` (`userID`, `TimeStamp`) VALUES (%r, %r);"%(str(userID),str(TimeStamp))
#
# cur.execute(sql_add)
#
# db.commit()