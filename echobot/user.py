import pymysql

def connect2db():
    db = pymysql.connect(host="127.0.0.1", user="root", password="", db="linebot", port=3306,use_unicode=True, charset="utf8")
    cur = db.cursor()
    cur.execute('SET NAMES utf8;')
    cur.execute('SET CHARACTER SET utf8;')
    cur.execute('SET character_set_connection=utf8;')
    return cur , db

def userexist(userID):
    cur , db = connect2db()
    sql_search = "SELECT * FROM `echobot_user` WHERE `userID` =%r"%str(userID)
    exist = False
    try:
        cur.execute(sql_search)  # 执行sql语句
        results = cur.fetchall()  # 获取查询的所有记录

        if (results!=()):  #判斷是否存在
           exist = True

    except pymysql.OperationalError as e:
        if e.errno == 2006:
            cur = connect2db()
            cur.execute(sql_search)  # 执行sql语句
            results = cur.fetchall()  # 获取查询的所有记录

            if (results != ()):  # 判斷是否存在
                exist = True

    finally:
        db.close()
        return exist

def useradd(exist , userID , TimeStamp):

    if(exist==False):
        cur , db = connect2db()
        sql_add = "INSERT INTO `echobot_user` (`userID`, `TimeStamp`) VALUES (%r, %r);"%(str(userID),str(TimeStamp))
        try:
            cur.execute(sql_add)
            # 提交
            db.commit()
        except pymysql.OperationalError as e:
            if e.errno == 2006:
                cur, db = connect2db()
                cur.execute(sql_add)
                # 提交
                db.commit()

        finally:
            db.close()
