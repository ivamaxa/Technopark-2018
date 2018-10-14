# -*- encoding: utf-8 -*-
#hash_log-хэш логов, ключи hash_log- урлы, сортируем их
import re
from datetime import datetime
import collections


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
    url=collections.Counter()
    time=collections.Counter()
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
                if line_res==ignore_urls: 
                    continue
                else:
                    line_res=line_res

            if ignore_files:
                if re.search(r'(https?\:\/\/\S+(\.\w+)$)', line_res):
                    continue    
                else:
                    line_res=line_res
            
            if request_type:
                line_res=line_res if re_type==reuest_type else ''
            
            if start_at or stop_at:
                data_re=datetime.strptime(re_date, '%d/%b/%Y %H:%M:%S')

                if start_at:  
                    data1=datetime.strptime(start_at, '%d/%b/%Y %H:%M:%S')
                    if data_re>=data1:
                        line_res=line_res
                if stop_at:
                    data1=datetime.strptime(stop_at, '%d/%b/%Y %H:%M:%S')
                    if data_re<=data1:
                        line_res=line_res
            if line_res:
                url[line_res]+=1
                time[line_res]+=int(response_time)
    
    
    if slow_queries:
        for i in range(5):       
            max_time=time.most_common(5) 
            result.append(max_time[i][1]//url[(max_time[i][0])])
            result.sort(reverse=True)
    else:
        for i in range(5):
            result.append(url.most_common(5)[i][1]) 
 
    return(result)
