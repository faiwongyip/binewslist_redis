# -*- coding: utf-8 -*-

import pymssql
import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.conf import settings
import re


class ProxyMiddleware(object):
    def __init__(self):
        self.conn=pymssql.connect(
            host=settings['MSSQL_HOST'],
            database=settings['MSSQL_DB_DOWN_DEV'],
            user=settings['MSSQL_USER'],
            password=settings['MSSQL_PWD'],
            charset="UTF-8")
        self.cur = self.conn.cursor()
        self.proxy = self._get_ip()
        
    def process_request(self, request, spider):
        request.meta['proxy'] = "https://%s" % self.proxy
        
    def process_response(self, request, response, spider):  
        if response.status // 100 not in [4,5]:
            return self._retry(request) or response
        return response
        
    def process_exception(self, request, exception, spider):
        return self._retry(request)
        
    def _get_ip(self):
        sql = """
            select ip + ':' + convert(varchar,port) 
            from ahbbs_ipproxy
        """
        self.cur.execute(sql)
        ip_port_list = self.cur.fetchall()
        ip_port = random.choice(ip_port_list)[0]
        return ip_port
        
    def _retry(self, request):
        retries = request.meta.get('retry_times', 0) + 1
        if retries <= 20:
            self.proxy = self._get_ip()
            new_request = request.copy()
            new_request.meta['retry_times'] = retries
            new_request.dont_filter = True
            new_request.meta['proxy'] = "https://%s" % self.proxy
            return new_request
        
class RandomUserAgent(UserAgentMiddleware):
    def __init__(self, user_agent=''):
        self.user_agent = settings['UA_LIST']
        
    def process_request(self, request, spider):
        ua = random.choice(self.user_agent)
        request.headers.setdefault('User-Agent', ua)
        
    

                
                
                
                
                
                
                
                
                
                
                
                