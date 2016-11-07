#encoding:utf-8

'''
爬虫任务调度系统：读取数据库配置，执行任务调度
'''

from utils import queryTask,writeJobidByTaskid
from datetime import datetime
import urllib
import urllib2
import simplejson

def writeLog(logstr):
    print datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" - " + logstr

def getStartTime():
    now = datetime.now()
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute
    weekday = now.weekday() #周一为0
    
    return (minute,hour,day,month,weekday)

def isAvailableTime(crontab_time_str,current_time):
    
    items = crontab_time_str.strip().split()
    if len(items)!=5 or items[0]=="*" or items[1]=="*":
        writeLog("wrong crontab format: "+crontab_time_str)
        return False
    
    try:
        int(items[1])
        int(items[0])
    except:
        writeLog("column minute,hour must be type int: "+crontab_time_str)
        return False
    
    #周检验
    if items[4] != "*" and int(items[4]) != current_time[4]:
        return False
    
    #月份检验
    if items[3] != "*" and int(items[3]) != current_time[3]:
        return False
    
    #日检验
    if items[2] != "*" and int(items[2]) != current_time[2]:
        return False
    
    #小时检验
    if int(items[1]) != current_time[1]:
        #print "hour"
        return False
    
    #分检验
    if int(items[0]) != current_time[0]:
        #print "minute"
        return False
    
    return True

def schedule_task(spidername,urlids):
    '''进行任务调度
    '''
    post_data = {'project':'articles',
                 'spider':spidername,
                 'urlids':urlids}
    post_data_urlencode = urllib.urlencode(post_data)
    
    requrl = "http://localhost:7002/schedule.json"
    req = urllib2.Request(url = requrl,data = post_data_urlencode)
    
    res_data = urllib2.urlopen(req)
    json_data = res_data.read()
    print json_data
    data = simplejson.loads(json_data)
    
    status = data['status'] if "status" in data else None
    jobid = data['jobid'] if "jobid" in data else None
    
    return (status,jobid)
    
def schedule():
    '''任务调度系统入口
    '''
    current_time = getStartTime()
    
    #查询任务
    tasks = queryTask()
    
    for task in tasks:
        task_id = task[0]
        crontab_time_str = task[1]
        spidername = task[2]
        urlids = task[3]
        
        if isAvailableTime(crontab_time_str,current_time) == False:
            #writeLog("not available time for taskid:"+str(task_id))
            continue
        
        (status,jobid) = schedule_task(spidername,urlids)
        
        if status == "ok":
            writeLog("schedule "+str(task_id)+" succeed! taskid is "+jobid)
            
            #回写jobid
            writeJobidByTaskid(task_id,jobid)
        else:
            writeLog("schedule "+str(task_id)+" falied!")
    
    
if __name__ == "__main__":
    schedule()