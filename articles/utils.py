#encoding:utf-8

from connections import spider_connection

db_spider = spider_connection()

def ensureConnection():
    #确保数据库连接
    
    global db_spider
    if db_spider.is_connected() == False:
        db_spider.reconnect()
    return db_spider.cursor()

#判定该文章是否已抓取过
def isArticleExist(url):
    db_cursor = ensureConnection()
    
    sql1 = "select count(*) from articles where url='%s';" % url

    db_cursor.execute(sql1)
    
    for row in db_cursor.fetchall():
        count = int(row[0])
        if count >= 1:
            #return False
            return True
        else:
            return False
        
def isMaterialExist(url):
    db_cursor = ensureConnection()
    
    sql1 = "select count(*) from material where url='%s';" % url

    db_cursor.execute(sql1)
    
    for row in db_cursor.fetchall():
        count = int(row[0])
        if count >= 1:
            #return False
            return True
        else:
            return False
        
def insertTxtFile(url,classify,content_path):
    db_cursor = ensureConnection()
    
    if isMaterialExist(url) == True:
        return
    else:
        sql = "insert into material(url,classify,content_path) values(\"%s\",\"%s\",\"%s\")" % (url,classify,content_path)
        db_cursor.execute(sql)
        
def getSiteEntryUrl(site,urlids=None):
    db_cursor = ensureConnection()
    
    classify2url = dict()
     
    sql = "select concat_ws('-',site_chinese,category_1,category_2,category_3,category_4),url from articles_entry where site='%s'" % site
    
    if urlids is not None:
        sql += " and id in(%s);" % (urlids,)
    
    db_cursor.execute(sql)
    
    for row in db_cursor.fetchall():
        classify = str(row[0]).replace(" ","").strip("-")
        classify2url[classify] = str(row[1])
    
    return classify2url

def getSiteXpath(site):
    db_cursor = ensureConnection()
    
    property2xpath = dict()
    
    sql = "select property,xpath from articles_xpath where site='%s';" % site
    db_cursor.execute(sql)
    
    for row in db_cursor.fetchall():
        property2xpath[str(row[0])] = row[1].decode("utf-8")
        
    return property2xpath

def queryTask():
    db_cursor = ensureConnection()
    
    tasks = []
    
    sql = "select id,frequency,site,url_ids from articles_task where isvalid='Y';"
    db_cursor.execute(sql)
    
    for row in db_cursor.fetchall():
        task = [int(row[0]),row[1],row[2],row[3]]
        tasks.append(task)
        
    return tasks

def writeJobidByTaskid(taskid,jobid):
    db_cursor = ensureConnection()
    
    sql = "update articles_task set jobid='%s',update_time=now() where id=%s" % (jobid,taskid)
    
    db_cursor.execute(sql)
    