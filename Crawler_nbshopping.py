import datetime
import sys
import time
import requests
import urllib3
import pymysql
import re
import echobot.user as user
from bs4 import BeautifulSoup
from linebot import LineBotApi
from linebot.models import *

urllib3.disable_warnings()
rs = requests.session()

def over18(board):
    res = rs.get('https://www.ptt.cc/bbs/{}/index.html'.format(board), verify=False) #verify為是否需SSL認證
    # 先檢查網址是否包含'over18'字串 ,如有則為18禁網站
    if 'over18' in res.url:
        print("18禁網頁")
        load = {
            'from': '/bbs/{}/index.html'.format(board),
            'yes': 'yes'
        }
        res = rs.post('https://www.ptt.cc/ask/over18', verify=False, data=load)
    return BeautifulSoup(res.text, 'html.parser')

def get_page_number(content):
    start_index = content.find('index')
    end_index = content.find('.html')
    page_number = content[start_index + 5: end_index]
    # 加一後才是最新頁數
    return int(page_number) + 1

def craw_page(res, Keywords):
    soup_ = BeautifulSoup(res.text, 'html.parser')
    article_seq = []
    for r_ent in soup_.find_all(class_="r-ent"):
        try:
            # 先得到每篇文章的篇url
            link = r_ent.find('a')['href']
            if link:
                # 確定得到url再去抓 標題
                title = r_ent.find(class_="title").text.strip()
                url = 'https://www.ptt.cc' + link

                if (Keywords in title)&(title.find('公告')==-1):
                    article_seq.append({'title': title,'url': url,})
        except Exception as e:
            pass
    return article_seq

def is_goods_exist(goodsID):
    cur, db = user.connect2db()
    sql_search = "SELECT * FROM `echobot_goods` WHERE `goodsID` =%r" % str(goodsID)
    goods_exist = False

    try:
        cur.execute(sql_search)  # 执行sql语句
        results = cur.fetchall()  # 获取查询的所有记录
        if (results != ()):  # 判斷是否存在
            goods_exist = True

    except pymysql.OperationalError as e:
        if e.errno == 2006:
            cur, db = user.connect2db()
            cur.execute(sql_search)  # 执行sql语句
            results = cur.fetchall()  # 获取查询的所有记录

            if (results != ()):  # 判斷是否存在
                goods_exist = True

    finally:
        db.close()
        return goods_exist

def goods_save_and_return_price(goodsID , article):
    rs = requests.session()
    res = rs.get(article['url'], verify=False)
    # 如網頁忙線中,則休息1秒後再連接
    if res.status_code != 200:
        time.sleep(1)
        res = rs.get(article['url'], verify=False)

    text = BeautifulSoup(res.text, 'html.parser')

    #先存商品基本資料
    content = text.find(id='main-content')
    # 過濾推文、其他資訊
    filtered = [v for v in content.stripped_strings if v[0] not in [u'※', u'◆'] and v[:2] not in [u'--']]
    content = ' '.join(filtered)
    content = re.sub(r'(\s)+', '', content)
    # print(content)

    try:
        #抓標題
        start = content.index('標題')
        end = content.index('時間')
        title = content[start+2:end]

        #抓價格
        start = content.index('價格')
        price = content[start+3:start+10]
        price = price.replace(',','')
        price=re.findall("\d+", price)

        if (price!=[]):
            price = int(price[0])
        else:price = 0

        #TimeStamp
        timestamp = goodsID.split('.')[1]
        # print(timestamp)

    except ValueError :
        title = article['title']
        price = 0
        timestamp = goodsID.split('.')[1]

    cur, db = user.connect2db()
    sql_add = "INSERT INTO `echobot_goods` (`id`, `goodsID`, `title`, `price`, `webLink` ,  `timestamp`) VALUES " \
              "(NULL, %r, %r, %r, %r ,%r);" % (str(goodsID), str(title), int(price), str(article['url']) ,str(timestamp))
    try:
        cur.execute(sql_add)
        # 提交
        db.commit()
    except pymysql.OperationalError as e:
        if e.errno == 2006:
            cur, db = user.connect2db()
            cur.execute(sql_add)
            # 提交
            db.commit()
    finally:
        db.close()

    #存圖片連結
    pic_url_list = []
    text = BeautifulSoup(res.text, 'html.parser')
    #找尋所有圖片連結
    for img in text.find_all("a", rel='nofollow'):
        img_url = img['href']
        if 'imgur' in img_url:
            img_url = img_url.split(':')
            img_url = 'https:'+img_url[1]
            pic_url_list.append(img_url)
    # print(pic_url_list)
    if (len(pic_url_list)!=0):
        cur, db = user.connect2db()
        for i in range(0,len(pic_url_list)):
            sql_add = "INSERT INTO `echobot_image` (`id`, `goodsID`, `imageLink`) VALUES " \
                  "(NULL, %r, %r);" % (str(goodsID), str(pic_url_list[i]))
            cur.execute(sql_add)
            db.commit()
        db.close()
    return price

def goods_notify(goodsID , article , sellprice):
    cur, db = user.connect2db()
    sql_search = "SELECT * FROM `echobot_goods_condition`"
    cur.execute(sql_search)  # 执行sql语句
    results = cur.fetchall()

    for row in results:
        goodstitle = row[1]
        price = row[2]

        if (re.search(goodstitle, article['title'], re.IGNORECASE)):
            while(price!=0):
                if((int(price)>=int(sellprice))):
                    line_bot_api = LineBotApi('3Hn3QKR+1nWt/DzpON4N+wGUXv/ne3/fR0zXTZmN4Zm60p3Eh1VGImUXRir6w41LQW01fU/r59PKSKsKFhZ+Nlo8CyHn+v/vhdcyngnh595kfBmgmjw3IIOfCJE5gjRU614lMKTfq4VfuGAHZc0UIAdB04t89/1O/w1cDnyilFU=')
                    line_bot_api.push_message('U453eacd40482c951f5b40b2b2b60b5ca', TextSendMessage(text=article['title']+" "+str(sellprice)+"元"))
                    line_bot_api.push_message('U453eacd40482c951f5b40b2b2b60b5ca', TextSendMessage(text=article['url']))
                    sql_search = "SELECT * FROM `echobot_image` WHERE `goodsID` = %r" % str(goodsID)
                    cur.execute(sql_search)  # 执行sql语句
                    picresults = cur.fetchall()
                    for pic in picresults:
                        piclink = pic[2]
                        if piclink.endswith('jpg'):
                            line_bot_api.push_message('U453eacd40482c951f5b40b2b2b60b5ca', ImageSendMessage(original_content_url = piclink, preview_image_url = piclink))
                        else:
                            line_bot_api.push_message('U453eacd40482c951f5b40b2b2b60b5ca', TextSendMessage(text=piclink))
                break

def analysis(article):
    article = article
    url = article['url']
    goodsID = url.split('/')[5].split('.html')[0]
    goods_exist = is_goods_exist(goodsID)
    if(goods_exist == False):
        sellprice = goods_save_and_return_price(goodsID,article)
        goods_notify(goodsID,article,sellprice)

def main():
    #  [版名] [爬蟲起始的頁面] [爬幾頁] [推文多少以上]
    board, start_page, page_term, Keywords = 'nb-shopping', -1, 2, '賣'
    start_time = time.time() #記錄開始TimeStamp

    if start_page == 0:
        print("請輸入有效數字")
        sys.exit()
    else:
        # 檢查看板是否為18禁,有些看板為18禁,回傳看板第一頁html
        soup = over18(board)
        all_page_url = soup.select('.btn.wide')[1]['href']
        start_page = get_page_number(all_page_url)

    # 如為 -1 ,則從最新的一頁開始
    index_list = []
    article_list = []

    for page in range(start_page, start_page - page_term, -1):
        page_url = 'https://www.ptt.cc/bbs/{}/index{}.html'.format(board, page)
        index_list.append(page_url)

    while index_list:
        index = index_list.pop(0)
        res = rs.get(index, verify=False)
        # 如網頁忙線中,則先將網頁加入 index_list 並休息1秒後再連接
        if (res.status_code != 200):
            index_list.append(index)
            time.sleep(1)
        else:
            article_list += craw_page(res, Keywords)
        time.sleep(0.05)

    # print(article_list)
    # 進入每篇文章分析內容
    while article_list:
        article = article_list.pop(0)
        res = rs.get(article['url'], verify=False)
        # 如網頁忙線中,則先將網頁加入 index_list 並休息1秒後再連接
        if res.status_code != 200:
            article_list.append(article)
            time.sleep(1)
        else:
            analysis(article)

if __name__ == '__main__':
    main()




