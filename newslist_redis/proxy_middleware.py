# -*- coding: utf-8 -*-


import random
# import base64
# from scrapy.conf import settings


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        # proxy = random.choice(settings['PROXIES'])
        proxy = random.choice(list(open('E:/mywork_yhh/binewslist_redis/newslist_redis/ip_list.txt'))).strip()
        print('----------' + proxy + '----------')
            
        request.meta['proxy'] = "http://%s" % proxy
        
        # request.meta['proxy'] = "http://183.95.80.102:8080" 