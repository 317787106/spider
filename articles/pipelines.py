# encoding: utf-8

from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem

import shutil
from settings import FILES_STORE

from utils import ensureConnection

spidernames = ["chira","clssn","cssn","drcnet","exuezhe","labournet","mohrss","cnss","chinajob"]

class MyFilesPipeline(FilesPipeline):
    
    def item_completed(self, results, item, info):
        
        if info.spider.name not in spidernames:
            return item
        
        attachments = []
        
        #重定义文件保存路径        
        for ok, x in results:
            
            if ok:
                
                filename = x['url'].split('/')[-1]
                
                old_path = FILES_STORE + x['path']
                
                shutil.copyfile(old_path, item['data_dir']+ filename)
                
                #写入附件名
                #if x['url'].endswith("pdf") or x['url'].endswith("xls"):
                attachments.append(item['data_dir']+ filename)
        
        item['attachments'] = attachments    
            
        return item
    
class StorePipeline():
    
    def __init__(self):
        pass
        
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls()
        
    def open_spider(self, spider):
        pass
        
    def process_item(self, item, spider):
        
        if spider.name in spidernames:
            sql = "insert into articles(url,classify,source,author,title,content_type,content_path,content,publish_time,abstract,keywords,attachments,create_time) \
            values(%(url)s,%(classify)s,%(source)s,%(author)s,%(title)s,%(content_type)s,%(content_path)s,%(content)s, \
            %(publish_time)s,%(abstract)s,%(keywords)s,%(attachments)s,now());"
            
            data = {"url":item["url"],
                    "classify":item["classify"],
                    "source":item.get("source",None),
                    "author":item.get("author",None),
                    "title":item["title"],
                    "content_type":item.get("content_type",0),
                    "content_path":item.get("content_path",None),
                    "content":item.get("content",None),
                    "publish_time":item.get("publish_time",None),
                    "abstract":item.get("abstract",None),
                    "keywords":item.get("keywords",None),
                    "attachments":','.join(item.get("attachments",[])),
                    }
        else:
            sql = "insert into material(url,classify,title,content_path) values(%(url)s,%(classify)s,%(title)s,%(content_path)s)"
            data = {"url":item["url"],
                    "classify":item["classify"],
                    "title":item["title"],
                    "content_path":item["content_path"],
                    }
            
        #db_cursor = self.db_spider.cursor()
        db_cursor = ensureConnection()
        db_cursor.execute(sql,data)
        db_cursor.close()
        
        #把文件内容写入数据库
        if spider.name in spidernames and item.get("content_type",0) == 2:
            content = open(item.get("content")).read()
             
            sql2 = "update articles set content=%(content)s where url=%(url)s;"
            
            data2 = {"url":item["url"],
                "content":content
                }
            
            db_cursor2 = ensureConnection()
            db_cursor2.execute(sql2,data2)
            db_cursor2.close()
        
        return item
        
    def close_spider(self, spider):
        pass