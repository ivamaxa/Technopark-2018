# -*- encoding: utf-8 -*-
#hash_log-хэш логов, ключи hash_log- урлы, сортируем их
import re
from datetime import datetime
from collections import Counter


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
    result=[]
    mas_time=[]
    
    f=open('log.log')
    for line in f:
        
        pars_str=re.search(r'\[(\S+\s+\S+)\]\s+\"(\S+)\s+https?(\:\/\/[\w\.]+\.[a-z\.]+[\/\w\.]*\-*\w+\=*\-*\.*\w+\.*\w*\.*)*[\?\S+]*\s+\S+\s+(\S+)\s+(\S+)', line) 
        if pars_str:
            re_date=pars_str.group(1).rstrip()
            re_type=pars_str.group(2).rstrip()
            line_url=pars_str.group(3).rstrip()
            response_time=pars_str.group(5).rstrip()
            re_code=pars_str.group(4).rstrip()

            line_res=line_url
            #if ignore_www or ignore_urls or ignore_files:
            if ignore_www:
                line_res=line_res.replace("www.", "") if re.search(r'\:\/\/www', line_url) else line_res
            if ignore_urls:
                line_res='' if line_res==ignore_urls else line_res
            if ignore_files:
                line_res='' if re.search(r'([^\s]+(?=\.(jpg|gif|png|js))\.\2)', line_res) else line_res
            
            if request_type:
                line_res=line_res if re_type==reuest_type else ''
            
            if start_at or stop_at:
                data_re=datetime.strptime(re_date, '%d/%b/%Y %H:%M:%S')
                pattern=start_at if start_at else stop_at 
                data1=datetime.strptime(pattern, '%d/%b/%Y %H:%M:%S')
                if start_at:    
                    if data_re>=data1:
                        line_res=line_res
                if stop_at:
                    if data_re<=data1:
                        line_res=line_res
            if line_res:
                mas_time.append(int(response_time))
                mas.append(line_res)
    dict_url=Counter(mas)
    max_el=[]
    max_i=[]
    max_url=[]
    if slow_queries:
        for h in range(5):
            time=0
            max_el=max(mas_time)
            max_i=mas_time.index(max_el)
            max_url=mas[max_i]

            for i in range(len(mas)):
                if max_url==mas[i]:
                    time+=mas_time[i]
            result.append(time//dict_url[max_url])
            result.sort(reverse=True)

            mas_time.pop(max_i)        
    else:
        for i in sorted(dict_url, key=dict_url.get, reverse=True):
            if len(result)<5:
                result.append(dict_url[i])
 
    return(result)
