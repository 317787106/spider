#encoding:utf-8
import os

from utils import insertTxtFile
if __name__ == "__main__":
#     for rt, dirs, files in os.walk("/home/Classify_ImportantFile"):
#         for f in files:
#             if os.path.splitext(f)[1] == ".txt":
#                 content_path = rt+"/"+f
#                 url = os.path.splitext(f)[0]
#                 index = rt.rfind("/")
#                 classify = rt[index+1:]
#                 
#                 insertTxtFile(url,classify,content_path)
                
    for rt, dirs, files in os.walk("/home/AllText/"):
        for f in files:
            if os.path.splitext(f)[1] == ".txt":
                content_path = rt+"/"+f
                url = os.path.splitext(f)[0]

                classify = ''
                
                insertTxtFile(url,classify,content_path)
                