import pymssql
import redis
import sys
sys.path.append("./newslist_redis")
import settings

def main():
    conn = pymssql.connect(host=settings.MSSQL_HOST, database=settings.MSSQL_DB_DOWN, user=settings.MSSQL_USER, password=settings.MSSQL_PWD, charset="UTF-8")
    
    r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    r.delete('binewslist:dupefilter', 'binewslist:idle_close_key', 'binewslist:requests', 'binewslistScanpage:start_urls')

    cur = conn.cursor()
    sql = '''select distinct agencyid from down_agency where srcsys='BI'and effective_to=99991231 and iseffectiveflag=1'''
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        # print (raw[0])
        start_url1 = 'http://dealer.bitauto.com/' + str(row[0]) + '/news.html'
        r.lpush('binewslistScanpage_ali:start_urls', start_url1)
        # start_url2 = 'http://dealer.autohome.com.cn/' + str(row[0]) + '/informationList.html'
        # r.lpush('ahnewslistScanpage:start_urls', start_url2)

    conn.close()
    
if __name__ == '__main__':
    main()
    
    
