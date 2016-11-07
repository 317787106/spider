#encoding:utf-8

from __future__ import division

import xlwt

def getData():
    
    city2diff2count = dict()
    city2total = dict()
    city2distinct_orders = dict()
    city2percent = dict()
    
    cityids = [1,2,3,4,15,16,17,18,19,37,38,40,41,42,46,50,51,52,53,54,55,60,61,62,63,65,67,97,112,129,146,167,236,265,266,267,322,333,339,365,1315]
    
    for city in cityids:
        city2diff2count[city] = {10:0,
                                9:0,
                                8:0,
                                7:0,
                                6:0,
                                5:0,
                                4:0,
                                3:0,
                                2:0,
                                
                                -2:0,
                                -3:0,
                                -4:0,
                                -5:0,
                                -6:0,
                                -7:0,
                                -8:0,
                                -9:0,
                                -10:0
                                 }
    
        city2total[city] = 0
        city2distinct_orders[city] = set()
        
    with open("sample/test.txt") as f:
        for line in f:
            items = line.strip().split()
            city = int(items[0])
            diff = int((int(items[7]) - int(items[6]))/1000)
            
            if diff>=2:
                diff = min([diff,10]) 
                for delta in range(2,diff+1):
                    city2diff2count[city][delta] += 1
                    
            if diff<=-2 :
                diff = max(diff,-10)
                for delta in range(diff,-2+1):
                    city2diff2count[city][delta] += 1
                
            city2total[city] += 1
            city2distinct_orders[city].add("\t".join(items[1:5]))
            
    with open("sample/city_percent.txt") as f:
        for line in f:
            items = line.strip().split()
            cityid = int(items[0])
            percent = float(items[1])
            
            city2percent[cityid] = percent
            
    output = []
    out = ["城市id","全国"]
    for cityid in cityids:
        out.append(cityid)
    output.append(out)
    
    out = ["样本数",sum(city2total.values())]
    for cityid in cityids:
        out.append(city2total[cityid])
    output.append(out)
    
    out = ["不重复样本数",]
    total = 0
    for cityid in cityids:
        total += len(city2distinct_orders[cityid])
    out.append(total)
    for cityid in cityids:
        out.append(len(city2distinct_orders[cityid]))
    output.append(out)
    
    out = ["该城市订单占全国市内订单百分比",]
    total = 0.0
    for cityid in cityids:
        total += city2percent[cityid]*100
    out.append(total)
    for cityid in cityids:
        out.append(city2percent[cityid]*100)
    output.append(out)
        
    for km in [10,9,8,7,6,5,4,3,2,-2,-3,-4,-5,-6,-7,-8,-9,-10]:
        if km > 0:
            out = [">=%skm" % km,]
        else:
            out = ["<=%skm" % km,]
            
        #先写总体数据，横着写
        weights = 0.0
        for city in cityids:
            weights += city2diff2count[city][km] * city2percent[city]
        weights = "%.1f" % weights
        out.append(weights)
        
        #再写分城市数据
        for city in cityids:
            out.append(city2diff2count[city][km])
        
        output.append(out)
    
    return output

def getSampleData():
    
    city2diff2count = dict()
    city2ABdiff2count = dict()
    city2total = dict()
    city2distinct_orders = dict()
    city2percent = dict()
    
    cityidset = set()
    with open("sample/test_sample.txt") as f:
        for line in f:
            items = line.strip().split()
            cityid = int(items[1])
            cityidset.add(cityid)
            
    cityids = list(cityidset)
    
    for city in cityidset:
        city2diff2count[city] = {10:0,
                                9:0,
                                8:0,
                                7:0,
                                6:0,
                                5:0,
                                4:0,
                                3:0,
                                2:0,
                                
                                -2:0,
                                -3:0,
                                -4:0,
                                -5:0,
                                -6:0,
                                -7:0,
                                -8:0,
                                -9:0,
                                -10:0
                                 }
        
        city2ABdiff2count[city] = {10:0,
                                9:0,
                                8:0,
                                7:0,
                                6:0,
                                5:0,
                                4:0,
                                3:0,
                                2:0,
                                
                                -2:0,
                                -3:0,
                                -4:0,
                                -5:0,
                                -6:0,
                                -7:0,
                                -8:0,
                                -9:0,
                                -10:0
                                 }
    
        city2total[city] = 0
        city2distinct_orders[city] = set()
        
    total = 0
    with open("sample/test_sample.txt") as f:
        for line in f:
            items = line.strip().split()
            city = int(items[1])
            diff = int((int(items[8]) - int(items[7]))/1000)
            
            if diff>=2:
                diff = min([diff,10]) 
                for delta in range(2,diff+1):
                    city2diff2count[city][delta] += 1
                    
            if diff<=-2 :
                diff = max(diff,-10)
                for delta in range(diff,-2+1):
                    city2diff2count[city][delta] += 1
                
            ABdiff = int((int(items[8]) - int(items[6]))/1000)
            
            if ABdiff>=2:
                ABdiff = min([ABdiff,10]) 
                for delta in range(2,ABdiff+1):
                    city2ABdiff2count[city][delta] += 1
                    
            if ABdiff<=-2 :
                ABdiff = max(ABdiff,-10)
                for delta in range(ABdiff,-2+1):
                    city2ABdiff2count[city][delta] += 1
                
            city2total[city] += 1
            city2distinct_orders[city].add("\t".join(items[2:6]))
            
            total += 1
            
    for city in cityids:
        city2percent[city] = city2total[city]*100/total
            
    output = []
    out = ["城市id","全国"]
    for cityid in cityids:
        out.append(cityid)
    output.append(out)
    
    out = ["样本数",sum(city2total.values())]
    for cityid in cityids:
        out.append(city2total[cityid])
    output.append(out)
    
    out = ["不重复样本数",]
    total = 0
    for cityid in cityids:
        total += len(city2distinct_orders[cityid])
    out.append(total)
    for cityid in cityids:
        out.append(len(city2distinct_orders[cityid]))
    output.append(out)
    
    out = ["该城市订单占全国市内订单百分比",]
    total = 0.0
    for cityid in cityids:
        total += city2percent[cityid]
    out.append(total)
    for cityid in cityids:
        out.append("%.2f" % city2percent[cityid])
    output.append(out)
        
    for km in [10,9,8,7,6,5,4,3,2,-2,-3,-4,-5,-6,-7,-8,-9,-10]:
        if km > 0:
            out = [">=%skm" % km,]
        else:
            out = ["<=%skm" % km,]
            
        #先写总体数据，横着写
        weights = 0
        for city in cityids:
            weights += city2diff2count[city][km]
        out.append(weights)
        
        #再写分城市数据
        for city in cityids:
            out.append(city2diff2count[city][km])
        
        output.append(out)
    
    output.append([])
    
    #计算距离与目前距离的差距
    for km in [10,9,8,7,6,5,4,3,2,-2,-3,-4,-5,-6,-7,-8,-9,-10]:
        if km > 0:
            out = [">=%skm" % km,]
        else:
            out = ["<=%skm" % km,]
            
        #再写分城市数据
        for city in cityids:
            out.append(city2ABdiff2count[city][km])
        
        output.append(out)
    
    return output

def getCountryData():
    diff2total = {10:0,
                9:0,
                8:0,
                7:0,
                6:0,
                5:0,
                4:0,
                3:0,
                2:0,
                1:0,
                
                -1:0,
                -2:0,
                -3:0,
                -4:0,
                -5:0,
                -6:0,
                -7:0,
                -8:0,
                -9:0,
                -10:0
                  }
    total = 0
    
    with open("sample/test_country.txt") as f:
        for line in f:
            items = line.strip().split()
            diff = int((int(items[6]) - int(items[5]))/10000)
            
            if diff>=1:
                diff = min([diff,10])
                for delta in range(1,diff+1):
                    diff2total[delta] += 1
            
            if diff <=-1:
                diff = max([diff,-10])
                for delta in range(diff,-1+1):
                    diff2total[delta] += 1
            
            total += 1
    
    output = []
    output.append(["样本数",total])
    
    for km in [10,9,8,7,6,5,4,3,2,1,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10]:
        if km > 0:
            out = [">=%s0km" % km,diff2total[km]]
        else:
            out = ["<=%s0km" % km,diff2total[km]]
        output.append(out)    
        
    return output
            
def writeSampleError():
    
    fp = open("sample/sample_error.txt","w")
    
    with open("sample/test_sample.txt") as f:
        for line in f:
            items = line.strip().split()
            calc_distance = int(items[8])
            baidu_distance = int(items[7])
            
            if calc_distance-baidu_distance > 4000:
                fp.write(line.strip()+"\n")
    
    fp.close()

def writeExcel():
    workbook = xlwt.Workbook(encoding='utf-8')
    
    data = getSampleData()
    booksheet = workbook.add_sheet('城市整体距离误差评估', cell_overwrite_ok=True)

    for i, row in enumerate(data):
        for j, col in enumerate(row):
            booksheet.write(i, j, col)
    
    data = getData()
    booksheet = workbook.add_sheet('单城市距离误差评估', cell_overwrite_ok=True)

    for i, row in enumerate(data):
        for j, col in enumerate(row):
            booksheet.write(i, j, col)
    
    data = getCountryData()
    booksheet = workbook.add_sheet('城际距离误差评估', cell_overwrite_ok=True)

    for i, row in enumerate(data):
        for j, col in enumerate(row):
            booksheet.write(i, j, col)
    
    workbook.save('sample/距离误差评估.xls')
    
    writeSampleError()

def send_report_mail(to_list,sub,content,attachment=None):
    import smtplib  
    from email.mime.text import MIMEText
    from email.MIMEMultipart import MIMEMultipart
    
    mail_host="211.151.134.214"  #设置服务器
    mail_port = 25
    mail_user="info"  #用户名
    mail_pass="info2ofni"   #口令 
    mail_postfix="mx.didapinche.com"  #发件箱的后缀
    
    me=mail_user+"@"+mail_postfix
    msg=MIMEMultipart() 
    msg['Subject'] = sub
    msg['From'] = me  
    msg['To'] = ";".join(to_list)  
    
    body=MIMEText(content,'plain', 'utf-8')
    msg.attach(body)
    
    #发送多个附件
    for filename in attachment:
        att = MIMEText(open(filename,'rb').read(),'base64','utf-8')
        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = 'attachment;filename="%s"' % (filename.split('/')[-1],)
        msg.attach(att)
    
    server = smtplib.SMTP()  
    server.connect(mail_host,mail_port)  
    server.login(mail_user,mail_pass)  
    server.sendmail(me, to_list, msg.as_string())  
    server.close()  

def sendMail():
    from datetime import datetime
    mailto_list=['jiangyuanshu@didapinche.com']
    #mailto_list=['jiangyuanshu@didapinche.com','duanjianbo@didapinche.com','yangyongxin@didapinche.com','sunbowen@didapinche.com'] 
    send_report_mail(mailto_list,"距离误差评估报告-"+datetime.now().strftime("%Y-%m-%d"),"",['sample/距离误差评估.xls',"sample/sample_error.txt"])
    
if __name__ == "__main__":
    writeExcel()
    sendMail()
    