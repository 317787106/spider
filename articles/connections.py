#encoding:utf-8

from mysql import connector
# from urls import dev_config,production_config

# import socket,fcntl,struct

#开发环境数据库配置
dev_config = {
"HOST" : "192.168.1.234",
"DATABASE" : "didapinche",
"USERNAME" : "jiangyuanshu",
"PASSWORD" : "jiangyuanshu",
"PORT" : 3308
}

#产品环境数据库配置
production_config = {
"HOST" : "123.57.164.181",
"DATABASE" : "didapinche",
"USERNAME" : "root",
"PASSWORD" : "12345678",
"PORT" : 3306
}

# def getip(ethname='em1'): 
#     s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
#     try:
#         return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0X8915, struct.pack('256s', ethname[:15]))[20:24]) 
#     except:
#         return None

'''
建立mysql数据库连接
'''
def mysql_connection(mysql_host, mysql_user, mysql_passwd, mysql_db, mysql_port=3306, mysql_charset='utf8', mysql_connect_timeout=5000):
    return connector.Connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_passwd,
        database=mysql_db,
        port = mysql_port,
        charset=mysql_charset,
        connect_timeout=mysql_connect_timeout,
        autocommit=True,
        use_unicode=False
    )

def spider_connection():
#     if getip() is not None and getip().startswith('192.168.'): 
#         HOST = dev_config["HOST"]
#         USERNAME = dev_config["USERNAME"]
#         PASSWORD = dev_config["PASSWORD"]
#         DATABASE = dev_config["DATABASE"]
#         PORT = dev_config["PORT"]
#     else:
#         HOST = production_config["HOST"]
#         USERNAME = production_config["USERNAME"]
#         PASSWORD = production_config["PASSWORD"]
#         DATABASE = production_config["DATABASE"]
#         PORT = production_config["PORT"]
        
    HOST = production_config["HOST"]
    USERNAME = production_config["USERNAME"]
    PASSWORD = production_config["PASSWORD"]
    DATABASE = production_config["DATABASE"]
    PORT = production_config["PORT"]
            
    return mysql_connection(HOST, USERNAME, PASSWORD, DATABASE,PORT)