# -*- coding: utf-8 -*-
import datetime
import re
import os
import redis
import xlrd
import scrapy
from scrapy.conf import settings
from scrapy_redis.spiders import RedisCrawlSpider

class BinewslistSpider(RedisCrawlSpider):

    name = "binewslist"
    redis_key ='binewslistScanpage:start_urls' #从redis读取经销商的入口链接
    
    def __init__(self,lastdate=None, *args, **kwargs):
        self.batchno=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        super(BinewslistSpider, self).__init__(*args, **kwargs)
        if lastdate:#获取参数
            self.lastdate=lastdate    
        else:
            self.lastdate=(datetime.datetime.now() + datetime.timedelta(days = -2)).strftime('%Y%m%d')#默认前推两天
            
        #读取相应关键词
        self.keyword_hd=[]
        self.keyword_cx=[]
        self.keyword_sj=[]
        self.keyword_cncw=[]
        wb = xlrd.open_workbook('keyword.xls') 
        sh = wb.sheets()[0]
        nRows=sh.nrows
        for iRow in range(1,nRows):
            if sh.cell(iRow,0).value != None and str(sh.cell(iRow,0).value).strip() !='':
                self.keyword_hd.append([sh.cell(iRow,0).value,sh.cell(iRow,1).value])
            else:
                break
        
        for iRow in range(1,nRows):
            if sh.cell(iRow,3).value != None and str(sh.cell(iRow,3).value).strip() !='':
                self.keyword_cncw.append([sh.cell(iRow,3).value,sh.cell(iRow,4).value])
            else:
                break
                
        for iRow in range(1,nRows):
            if sh.cell(iRow,6).value != None and str(sh.cell(iRow,6).value).strip() !='':
                self.keyword_sj.append([sh.cell(iRow,6).value])
            else:
                break
                
        for iRow in range(1,nRows):
            if sh.cell(iRow,8).value != None and str(sh.cell(iRow,8).value).strip() !='':
                self.keyword_cx.append([sh.cell(iRow,8).value,sh.cell(iRow,9).value])
            else:
                break
    
    def parse(self,response):
        try:
            firstpostdate = response.xpath("//div[@class='mov_news']/ul/li[1]/div/p[2]/span/text()").extract()[0].replace('-','')
        except:
            firstpostdate = False
        if int(firstpostdate) >= int(self.lastdate):
            print("parse:",response.url)
            for dl in response.xpath("//dl[contains(dt/text(),'分类')]/dd//a[not(contains(text(),'全部分类'))]"):
                yield scrapy.http.Request(url=response.urljoin(dl.xpath("@href").extract()[0]),callback=self.parse_list1, dont_filter=True)
            
    def parse_list1(self,response):
        try:
            firstpostdate = response.xpath("//div[@class='mov_news']/ul/li[1]/div/p[2]/span/text()").extract()[0].replace('-','')
        except:
            firstpostdate = False
        if int(firstpostdate) >= int(self.lastdate):
            print("parse_list1:",response.url)
            salesinfotype = response.xpath("//dl[contains(dt/text(),'分类')]/dd//a[@class='current']/text()").extract()[0].strip()
            
            for tr in response.xpath("//div[@class='mov_news']/ul/li"):
                if int(tr.xpath("div/p[2]/span/text()").extract()[0].replace("-",""))>=int(self.lastdate):
                    yield scrapy.http.Request(
                        url=response.urljoin(tr.xpath("h3/a/@href").extract()[0]),
                        callback=self.parse_content,
                        meta={'salesinfotype':salesinfotype}, dont_filter=True)
                        
            if int(response.xpath("//div[@class='mov_news']/ul/li[last()]/div/p[2]/span/text()").extract()[0].replace("-",""))>=int(self.lastdate) and response.xpath("//a[contains(text(), '下一页')]"):
                yield scrapy.http.Request(
                    url=response.urljoin(response.xpath("//a[contains(text(), '下一页')]/@href").extract()[0]),
                    callback=self.parse_list1, 
                    dont_filter=True)

    def parse_content(self,response):
        salesinfoid=response.url.split("/")[-1].split(".")[0]
        print("parse_content:",response.url)
        libao=""    #礼包
        yhtj_qt=""  #优惠条件-前提条件
        yhtj_dp=""
        yhtj_bz=""
        by_zbzq=""
        by_jlfy=""
        by_jyfy=""
        bx_gs=""
        bx_fy=""
        dk_jrgs=""
        dk_dkfs=""
        
        title = response.xpath("//h1[@class='ad']/text()").extract()[0].strip().replace('\'', ' ')
        postdate = re.sub('年|月|日', '', re.findall(r'<i>|</i>.*?发布时间：(.*?)</span>', response.text, re.S)[0].strip())
        
        if settings['HASHTML']==True:
            contentxpath="//div[@class='lfcont visible']"
        else:
            contentxpath="//div[@class='lfcont visible']//*[not(@type='text/javascript')]/text()"
        zhengwen = re.sub('\\xa0|\\xae|\\u2022','',''.join(response.xpath(contentxpath).extract()))
        
        if response.xpath("//dt[contains(text(),'优惠前提条件')]"):
            yhtj_qt=';'.join(re.findall('>([\S]*?)</em',re.findall("<dt[\s\S]*?>[\s\S]*?优惠前提条件[\s\S]*?<dd[\s\S]*?>([\s\S]*?)</dd>",response.xpath("/html").extract()[0])[0])).replace("'","").replace("(","").replace(")","")
        if response.xpath("//dt[contains(text(),'搭配消费项')]"):
            yhtj_dp=';'.join(re.findall('>([\S]*?)</em',re.findall("<dt[\s\S]*?>[\s\S]*?搭配消费项[\s\S]*?<dd[\s\S]*?>([\s\S]*?)</dd>",response.xpath("/html").extract()[0])[0])).replace("'","").replace("(","").replace(")","")
        if response.xpath("//p[text()='优惠备注']"):
            yhtj_bz=';'.join(re.findall('>([\S]*?)<',re.findall("优惠备注</p>([\s\S]*?)</div>",response.xpath("/html").extract()[0])[0])).replace("'","").replace("(","").replace(")","")
        if response.xpath("//p[text()='赠送礼包']"):
            libao=''.join(re.findall("赠送礼包[\s\S]*?<br>([\s\S]*?)</p>",response.xpath("/html").extract()[0])).replace('\n', '').replace("'","").replace(" ","")
        if response.xpath("//span[starts-with(text(),'质保周期')]"):
            by_zbzq=''.join(response.xpath("//p[starts-with(span/text(),'质保周期')]/text()").extract()).strip().replace("'","").replace("(","").replace(")","")
        if response.xpath("//span[starts-with(text(),'更换机油机滤费用')]"):
            by_jlfy=''.join(response.xpath("//p[starts-with(span/text(),'更换机油机滤费用')]/text()").extract()).strip().replace("'","").replace("(","").replace(")","")
        if response.xpath("//span[starts-with(text(),'更换机油三滤费用')]"):
            by_jyfy=''.join(response.xpath("//p[starts-with(span/text(),'更换机油三滤费用')]/text()").extract()).strip().replace("'","").replace("(","").replace(")","")
        if response.xpath("//span[starts-with(text(),'保险公司')]"):
            bx_gs=''.join(response.xpath("//p[starts-with(span/text(),'保险公司')]/text()").extract()).strip().replace("'","").replace("(","").replace(")","")
        if response.xpath("//span[starts-with(text(),'保险费用')]"):
            bx_fy=''.join(response.xpath("//p[starts-with(span/text(),'保险费用')]/text()").extract()).strip().replace("'","").replace("(","").replace(")","")
        if response.xpath("//span[starts-with(text(),'金融公司')]"):
            dk_jrgs=''.join(response.xpath("//p[starts-with(span/text(),'金融公司')]/text()").extract()).strip().replace("'","").replace("(","").replace(")","")
        if response.xpath("//span[starts-with(text(),'贷款方式')]"):
            dk_dkfs=''.join(response.xpath("//p[starts-with(span/text(),'贷款方式')]/text()").extract()).strip().replace("'","").replace("(","").replace(")","")

        cont=zhengwen
        #活动分类
        hdfl=[]#活动分类
        hdgjc=[]#活动关键词
        hdsj=''
        cncw=[]
        salesinfotype2=''
        salesinfotype1='其它'
        for key in self.keyword_cx:
                if str(key[0]) in title:
                    salesinfotype1=str(key[1])
                    break
        #活动处理
        if '活动' in response.meta["salesinfotype"]:
            cont=''.join(response.xpath("//div[@class='lfcont visible']//text()").extract()).strip().replace('\'', ' ')
            for key in self.keyword_hd:
                if str(key[0]) in title+cont:
                    if not str(key[0]) in hdgjc:
                        hdgjc.append(str(key[0]))
                    if not str(key[1]) in hdfl:
                        hdfl.append(str(key[1]))
                     
            #活动时间
            for key in self.keyword_sj:
                rtn=re.search(key[0],title+cont)
                if rtn:
                    if len(rtn.group())>len(hdsj):
                        hdsj=rtn.group()
                    #break
            #场内场外
            
            for key in self.keyword_cncw:
                if str(key[0]) in title+cont:
                    if not str(key[1]) in cncw:
                        cncw.append(str(key[1]))
            salesinfotype2='/'.join(hdfl)
        
        
        agencyid = response.url.split("/")[3]
        try:
            agencyname = response.xpath("//div[@class='jxs_info']/h2/strong/text()").extract()[0].strip()
        except:
            agencyname = response.xpath("//div[@class='brand']/a[1]/text()").extract()[0].strip()
        try:
            tel = response.xpath("//p[contains(text(),'电话')]/span/text()").extract()[0].replace('-','').strip()
        except:
            tel = ''
            
        try:
            address = response.xpath("//div[@class='jxs_info']/ul/li/div[@class='ads']/@title").extract()[0].strip()   
        except:
            address = ''
        try:
            manufacture = response.xpath("//div[@class='jxs_info']/ul/li/div/div[@class='carmore']/text()").extract()[0].strip()
        except:
            manufacture = ''
        
        data = {
            "city":'',
            "agencyid":agencyid,
            "agencyname": agencyname,
            "carsseriesid":'',
            "carsseries_en":'',
            "carsseriesname":'',
            "brandname":'',
            "manufacture":manufacture,
            "salesinfoid":salesinfoid,
            "salesinfotype":response.meta["salesinfotype"],
            "title":title,
            "postdate":postdate,
            "libao":libao,
            "yhtj_qt":yhtj_qt,
            "yhtj_dp":yhtj_dp,
            "yhtj_bz":yhtj_bz,
            "by_zbzq":by_zbzq,
            "by_jlfy":by_jlfy,
            "by_jyfy":by_jyfy,
            "bx_gs":bx_gs,
            "bx_fy":bx_fy,
            "dk_jrgs":dk_jrgs,
            "dk_dkfs":dk_dkfs,
            "address":address,
            "tel":tel,
            "srcsys":"BI",
            "url":response.url,
            "updatetime":self.batchno,
            "salesinfotype1":salesinfotype1,
            "keyword":'/'.join(hdgjc),
            "shijian":hdsj,
            "changneiwai":'/'.join(cncw),
            "content":cont,
            "salesinfotype2":salesinfotype2,
        }
        yield data

        

        
        