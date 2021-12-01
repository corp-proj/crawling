import os
import json
import datetime

def execute():
    os.system("scrapy crawl cr -o b.json")

def read():
    with open('a.json',encoding='utf-8') as json_file:
        data = json.load(json_file)

    now_time = datetime.datetime.now()
    year = str(now_time.year)
    month = str(now_time.month)
    day = str(now_time.day)
    hour = str(now_time.hour)
    new = year + '-' + month + '-' + day + '-' + hour
    
    new_data = {'id' : new, 'type' : 'hour', 'content' : data}
    return new_data

execute()



