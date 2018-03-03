# -*- coding: utf-8 -*-
from twisted.internet import task
from scrapy import signals
from scrapy.conf import settings
import pymssql


class StatsCollection(object):
    def __init__(self, stats):
        self.stats = stats
        self.stats_keys = [
            'downloader/request_bytes', 
            'downloader/request_count', 
            'downloader/request_method_count/GET', 
            'downloader/response_bytes', 
            'downloader/response_count', 
            'downloader/response_status_count/200', 
            'finish_reason', 'finish_time', 
            'item_scraped_count', 'log_count/DEBUG',
            'log_count/ERROR', 'log_count/INFO', 
            'log_count/WARNING', 'request_depth_max', 
            'response_received_count', 
            'scheduler/dequeued/redis', 
            'scheduler/enqueued/redis', 'start_time']
        self.conn = pymssql.connect(
            host=settings['MSSQL_HOST'],
            database=settings['MSSQL_DB'],
            user=settings['MSSQL_USER'],
            password=settings['MSSQL_PWD'],
            charset="UTF-8")
        self.cur = self.conn.cursor()
        
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        instance = cls(crawler.stats)
        
        # 注册spider关闭信号函数
        crawler.signals.connect(
            instance.spider_closed, 
            signal=signals.spider_closed)
        return instance
        
    def spider_closed(self, spider):
        dict_stats = self.stats.get_stats()
        
        # 获取stats字典的值，返回列表
        values_list = []
        for key in self.stats_keys:
            value = dict_stats.get(key, '')
            values_list.append(value)
            
        # 把爬虫的名字加进去
        values_list.insert(0, spider.name)
        
        sql = """
            insert into stats_list(
                spider_name, downloader_request_bytes, downloader_request_count, 
                downloader_request_method_count_GET, 
                downloader_response_bytes, 
                downloader_response_count, 
                downloader_response_status_count_200, 
                finish_reason, finish_time, 
                item_scraped_count, log_count_DEBUG, 
                log_count_ERROR, log_count_INFO, 
                log_count_WARNING, request_depth_max, 
                response_received_count, 
                scheduler_dequeued_redis, 
                scheduler_enqueued_redis, start_time) 
            values('%s','%s','%s','%s','%s','%s','%s',
                '%s','%s','%s','%s','%s','%s','%s',
                '%s','%s','%s','%s','%s')
        """ % tuple(values_list)
        
        self.cur.execute(sql)
        self.conn.commit()
        self.cur.close()
        self.conn.close() 

