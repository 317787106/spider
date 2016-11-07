# encoding: utf-8
from scrapy import Item,Field

class ArticleItem(Item):
    #分类
    classify = Field()
    #来源、发布者
    source = Field()
    #作者
    author = Field()
    #标题
    title = Field()
    #内容类型：1：文本类型，2：htm文件，3：pdf，0：其他
    content_type = Field()
    #内容保存路径
    content_path = Field()
    #内容
    content = Field()
    #发布时间
    publish_time = Field()
    #摘要
    abstract = Field()
    #关键词
    keywords = Field()
    #网址
    url = Field()
    #附件名列表
    attachments = Field()
    
    #定义需要下载的文件url，然后调用FilesPipeline
    file_urls = Field()
    files = Field()
    data_dir = Field()
    
class MaterialItem(Item):
    
    url = Field()
    
    title = Field()
    
    classify = Field()
    
    content_path = Field()
    