# -*- encoding: utf-8 -*-
#hash_log-хэш логов, ключи hash_log- урлы, сортируем их
import re
from datetime import datetime



def parse(
    ignore_files=False,
    ignore_urls=[],
    start_at=None,
    stop_at=None,
    request_type=None,
    ignore_www=False,
    slow_queries=False
):
    mas=[]
    url={}
    slow_url={} #cловарь урлов с медленными запросами(для сравнения)
    url_sum_time={} #словарь урлов с суммарным временем
    url2={} #доп словарь урлов ? 
    k=0
    f=open('log.log')
    for line in f:
        line_res='' #url строка прошедшая через модификаторы 
        result=re.search(r'\[(\S+\s+\S+)\]\s+\"(\S+)\s+https?(\:\/\/[\w\.]+\.[a-z\.]+[\/\w\.]*\-*\w+\=*\-*\.*\w+\.*\w*\.*)*', line) 
        result1=re.search(r'\s+(\S+)\/\S+\"\s+(\S+)\s+(\S+)', line)
        if result:
            re_date=result.group(1).rstrip()
            re_type=result.group(2).rstrip()
            line_url=result.group(3).rstrip()
            if result1:
                response_time=result1.group(3).rstrip()
                protocol=result1.group(1).rstrip()
                re_code=result1.group(2).rstrip()

            if ignore_www:
                line_res=line_res+line_url.replace("www.", "")
            elif slow_queries:
                if len(slow_url)<5:
                    slow_url[line_url]=int(response_time)
                    url_sum_time[line_url]=[int(response_time),1]
                else:
                    mas_key=sorted(slow_url, key=slow_url.get)
                    for i in mas_key:
                        if int(response_time)>int(slow_url[i]) and line_url !=i:
                            url2[i]=slow_url[i]
                            del slow_url[i]
                            slow_url[line_url]=int(response_time)
                            del url_sum_time[i]
                            url_sum_time[line_url]=[int(response_time), 1]
                            break
                        elif line_url==i:
                            url_sum_time[line_url][0]+=int(response_time)
                            url_sum_time[line_url][1]+=1

            elif request_type:
                if re_type==request_type:
                    line_res=line_res+line_url
                else:
                    line_res=''

            elif ignore_urls:
                if line_url==ignore_urls:
                    line_res=''
                else:
                    line_res=line_res+line_url
            elif ignore_files:
                if re.search(r'([^\s]+(?=\.(jpg|gif|png|js))\.\2)', line_url):
                    line_res=''
                else:
                    line_res=line_res+line_url
            elif start_at or stop_at:
                data_re=datetime.strptime(re_date, '%d/%b/%Y %H:%M:%S')
                pattern=start_at if start_at else stop_at 
                data1=datetime.strptime(pattern, '%d/%b/%Y %H:%M:%S')
                if start_at:    
                    if data_re>=data1:
                        line_res=line_res+line_url
                if stop_at:
                    if data_re<=data1:
                        line_res=line_res+line_url
            
            else:   
                line_res=line_res+line_url
            
            if line_res:
                if line_res in url:
                    url[line_res]=url[line_res]+1
                else:
                    url[line_res]=1
            
    if line_res:
        for i in sorted(url, key=url.get, reverse=True):
            if len(mas)<5:
                mas.append(url[i])
    elif url_sum_time:
        for i in url_sum_time:
            for j in url2:
                if i==j:
                    url_sum_time[i][0]+=url2[j]
                    url_sum_time[i][1]+=1
            mas.append(url_sum_time[i][0]//url_sum_time[i][1])
        mas=sorted(mas, reverse=True)        
    
    return(mas)

