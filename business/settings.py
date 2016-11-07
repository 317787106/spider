# encoding: utf-8

# Scrapy settings for cmt project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#


BOT_NAME = 'business'

SPIDER_MODULES = ['business.spiders']
NEWSPIDER_MODULE = 'business.spiders'

LOG_LEVEL = 'INFO'

DOWNLOADER_DEBUG = False

MEMUSAGE_REPORT = True
MEMDEBUG_ENABLED = True

ITEM_PIPELINES = {
                  }

CONCURRENT_REQUESTS = 3
CONCURRENT_REQUESTS_PER_DOMAIN = 3
CONCURRENT_ITEMS = 10

DOWNLOAD_TIMEOUT = 200

#DOWNLOAD_DELAY = 0.0

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip,deflate',
}

DNSCACHE_ENABLED = True
