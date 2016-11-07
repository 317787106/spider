#encoding:utf-8

import os
from pipelines import spidernames
from utils import ensureConnection

def writeContent():
    
    sql = "select id,content_path from articles where content_type=2 and id>=247243;"
    db_cursor = ensureConnection()
    db_cursor.execute(sql)
    
    count = 0
    for row in db_cursor.fetchall():
        
        count += 1
        if count % 1000 ==0:
            print count
        row_id = int(row[0])
        content_path = str(row[1])
        
        if not os.path.exists(content_path):
            continue
        
        content = open(content_path).read()
        
        sql = "update articles set content=%(content)s where id=%(row_id)s;"
         
        data = {"row_id":row_id,
                "content":content
                }
        
        db_cursor2 = ensureConnection()
        db_cursor2.execute(sql,data)
        db_cursor2.close()
        
    db_cursor.close()
    
if __name__ == "__main__":
    writeContent()