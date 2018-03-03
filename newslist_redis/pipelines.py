# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.conf import settings
from scrapy import log
import pymssql
# import pyodbc
from operator import itemgetter, attrgetter 
from .match_tool.deal_sale_files import match_from_cont
 
class MongoDBPipeline(object):
 
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]
    def process_item(self, item, spider):
        #print(item)
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))
            log.msg("Question added to MongoDB database!",
                    level=log.DEBUG, spider=spider)
        return item
        
class SqlserverPipeline(object):

    def __init__(self):
        self.conn=pymssql.connect(
            host=settings['MSSQL_HOST'],
            user=settings['MSSQL_USER'],
            password=settings['MSSQL_PWD'],
            charset="UTF-8")
        self.cur=self.conn.cursor()
        
    def process_item(self, item, spider):
        if item['salesinfotype']=='车友活动':
            dataHd = [
                item['city'],item['agencyid'],
                item['agencyname'],item['carsseriesid'],
                item['carsseries_en'],
                item['carsseriesname'],item['salesinfoid'],
                item['salesinfotype'],item['title'],
                item['postdate'],item['salesinfotype2'],
                item['keyword'],item['shijian'],
                item['changneiwai'],item['content'],
                item['address'],item['tel'],item['srcsys'],
                item['url'],item['updatetime'],
                item['manufacture'][:12],item['brandname']
            ]
            self.insert_data('ccp_xz_newslist_hd',dataHd)
            
        match_flag_list = [x for x in ['团购','车展'] if x in item['title']]
        dataNl1 = [
            item['city'],item['agencyid'],
            item['agencyname'],item['carsseriesid'],
            item['carsseries_en'],item['carsseriesname'],
            item['salesinfoid'],item['salesinfotype'],
            item['title'],item['postdate'],item['libao'],
            item['yhtj_qt'],item['yhtj_dp'],item['yhtj_bz'],
            item['by_zbzq'],item['by_jlfy'],item['by_jyfy'],
            item['bx_gs'],item['bx_fy'],item['dk_jrgs'],
            item['dk_dkfs'],item['address'],item['tel'],
            item['srcsys'],item['url'],item['updatetime'],
            item['salesinfotype1'],item['manufacture'][:12],
            item['brandname'],''.join(match_flag_list)
        ]
        isInsert = self.insert_data('ccp_xz_newslist_1',dataNl1)
        if isInsert: 
        # if 0: 
            matchRes = match_from_cont(item['content'])
            for mr in matchRes:
                mr.insert(0,item['salesinfoid'])
                if not mr[-1]:
                    # 提及车为空时，新闻的车型填充
                    mr[-1] = item['carsseriesname']
                mr.append(item['srcsys'])
                self.insert_data('saleInfoContent',mr)
            
        self.conn.commit()
        # return item
        
    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()        
        
    def insert_data(self,table, data):
        ccp_xz_newslist_hd_sql = """
            insert into ccpspider.dbo.ccp_xz_newslist_hd(
                city,agencyid,agencyname,carsseriesid,
                carsseries_en,carsseriesname,salesinfoid,
                salesinfotype,title,postdate,salesinfotype1,
                keyword,shijian,changneiwai,content,
                address,tel,srcsys,url,updatetime,
                manufacture,brandname) 
            values('%s','%s','%s','%s','%s','%s','%s',
                '%s','%s','%s','%s','%s','%s','%s','%s',
                '%s','%s','%s','%s','%s','%s','%s')
        """
        ccp_xz_newslist_1_sql = """
            insert into ccpspider.dbo.ccp_xz_newslist_1(
                city,agencyid,agencyname,
                carsseriesid,carsseries_en,carsseriesname,
                salesinfoid,salesinfotype,title,postdate,
                libao,yhtj_qt,yhtj_dp,yhtj_bz,by_zbzq,
                by_jlfy,by_jyfy,bx_gs,bx_fy,dk_jrgs,
                dk_dkfs,address,tel,srcsys,url,updatetime,
                salesinfotype1,manufacture,brandname,
                match_flag) 
            values('%s','%s','%s','%s','%s','%s','%s',
                '%s','%s','%s','%s','%s','%s','%s','%s',
                '%s','%s','%s','%s','%s','%s','%s','%s',
                '%s','%s','%s','%s','%s','%s','%s')
        """
        saleInfoContent_sql = '''
            insert into ccpspider.dbo.saleInfoContent
                (salesinfoid,oneclassify,twoclassify
                    ,content,note,mentioncar,srcsys)
            values ('%s','%s','%s','%s','%s','%s','%s')
        '''
        sqlDt = {
            'ccp_xz_newslist_hd': ccp_xz_newslist_hd_sql,
            'ccp_xz_newslist_1': ccp_xz_newslist_1_sql,
            'saleInfoContent': saleInfoContent_sql,
        }
        sql = sqlDt[table] % tuple(data)
        try:
            self.cur.execute(sql)
        # except pyodbc.OperationalError as e:
        except pymssql.OperationalError as e:
            print('报错！！！','\n',sql)
        # except pyodbc.IntegrityError as e:
        except pymssql.IntegrityError as e:
            print('%s发现重复值报错！！！' % table)
            return False
        return True
        
class DealCsName(object):

    def __init__(self):
        self.conn=pymssql.connect(host=settings['MSSQL_HOST'],database=settings['MSSQL_DB_DOWN'],user=settings['MSSQL_USER'],password=settings['MSSQL_PWD'],charset="UTF-8")
        self.cur=self.conn.cursor()
        sql="select srcsys,manufactureid,manufacture,carsseriesid,carsseriesname,sortid,keyword,impflag,brandname from keyword_carsseries"
        self.cur.execute(sql)
        self.rows=self.cur.fetchall()
        
    def process_item(self, item, spider):
        if item['carsseriesname']=='':
            k=[l for l in self.rows if l[0]==item['srcsys'] and l[2].replace('汽车','') in item['manufacture'].replace('汽车','')]
            k=sorted(k, key=itemgetter(5),reverse=True)  
            # print(k) 
            #第一遍遍历，优先处理进口，按关键词长度从上往下查找
            for tmp_k in k:
                if tmp_k[7]=='1':
                    if '进口' in item['title'] and tmp_k[6].lower() in item['title'].lower():
                        item['carsseriesid']=tmp_k[3]
                        item['carsseriesname']=tmp_k[4]
                        item['brandname']=tmp_k[8]
                        item['manufacture']=tmp_k[2]
                        break
                else:        
                    if tmp_k[6].lower() in item['title'].lower():
                        item['carsseriesid']=tmp_k[3]
                        item['carsseriesname']=tmp_k[4]
                        item['brandname']=tmp_k[8]
                        item['manufacture']=tmp_k[2]
                        break
            
            #第二遍遍历，直接根据关键词查找，主要处理进口车型，但是标题中不含进口
            if item['carsseriesname']=='':
                    for tmp_k in k:        
                        if tmp_k[6].lower() in item['title'].lower():
                            item['carsseriesid']=tmp_k[3]
                            item['carsseriesname']=tmp_k[4]
                            item['brandname']=tmp_k[8]
                            item['manufacture']=tmp_k[2]
                            break
            
            #第三遍遍历，如果匹配不到车型则按品牌去匹配厂商
            if item['carsseriesname']=='':
                #全系处理
                for tmp_k in k:
                    if tmp_k[7]=='1':
                        if '进口' in item['title'] and tmp_k[8].lower() in item['title'].lower(): #根据品牌+进口去匹配
                            item['carsseriesid']=''
                            item['carsseriesname']='全系'
                            item['brandname']=tmp_k[8]
                            item['manufacture']=tmp_k[2]
                            break
                    else:        #非进口部分
                        if tmp_k[8].lower() in item['title'].lower():
                            item['carsseriesid']=''
                            item['carsseriesname']='全系'
                            item['brandname']=tmp_k[8]
                            item['manufacture']=tmp_k[2]
                            break
            
            #最终如果还是为空，则分配一个国产厂商
            if item['carsseriesname']=='':
                try:
                    tmp_k=k[-1]
                    item['carsseriesid']=''
                    item['carsseriesname']='全系'
                    item['brandname']=tmp_k[8]
                    item['manufacture']=tmp_k[2]
                except Exception as e:
                    # print(e)
                    pass
        return item
        
    def close_spider(self, spider):
        self.conn.commit()
        self.cur.close()
        self.conn.close()           