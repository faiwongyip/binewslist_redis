# 新闻分布式爬虫

采集易车网经销商的促销新闻，并进行数据清洗、解析、入库。能够每天爬取新闻更新数据，解析出车型相关的促销和活动的分类、金额。爬虫结束时记录爬虫的运行状态。反爬虫可设置开启中间件proxy_middleware切换随机ip、UA。

## 主要技术：
scrapy、scrapy-redis、正则表达式、sqlserver

## 流程图：

![流程图](https://github.com/faiwongyip/binewslist_redis/blob/master/imgs/%E6%B5%81%E7%A8%8B%E5%9B%BE.png)

##数据表：

- **ccp_xz_newslist_1** ——新闻列表

![ccp_xz_newslist_1](https://github.com/faiwongyip/binewslist_redis/blob/master/imgs/ccp_xz_newslist_1.png)

- **ccp_xz_newslist_hd** ——活动列表
- **saleInfoContent** ——解析车型促销数据列表

![saleInfoContent](https://github.com/faiwongyip/binewslist_redis/blob/master/imgs/saleInfoContent.png)

- **stats_list** ——爬虫运行状态

![stats_list](https://github.com/faiwongyip/binewslist_redis/blob/master/imgs/stats_list.png)