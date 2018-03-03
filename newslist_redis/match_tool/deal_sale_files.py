# -*- coding:utf-8 -*-
import os
import re
import time 
import glob
import threading
import multiprocessing
from multiprocessing import Pool
import jieba
import pandas as pd
import sys
sys.path.append(r'.\newslist_redis\match_tool')
from match_sale import mianxi,dikou,shuangmian,zhihuan,yanbao,libao,baoxiao,shuixian

kwfundt = {'贴息': mianxi,'无息': mianxi,'免息': mianxi,
    '0息': mianxi,'零息': mianxi,'券': dikou,'抵': dikou,
    '双免': shuangmian,'置换': zhihuan,'换购': zhihuan,
    '保养': yanbao,'延保': yanbao,'保修': yanbao,
    '质保': yanbao,'礼': libao,'奖': libao,'油卡': libao,
    '精品': libao,'老客户': libao,'门票': libao,
    '补贴': libao,'报销': baoxiao,'险': shuixian,
    '税': shuixian
}   # 二级类别对应的函数

funcfydt = {
    mianxi: '金融',dikou: '金融',shuangmian: '金融',
    zhihuan: '置换',yanbao: '延保',baoxiao: '金融',
    shuixian: '其他',libao: '礼包类'
}   # 函数对应的一级类别
kwFilename = r'.\newslist_redis\match_tool\抽取的词汇.xlsx'

def deal_keyword(filename):
    kwDf = pd.read_excel(filename)
    kwSt = {kw for kw in kwDf['关键词']}
    kwDic = {kw:(cf,re.compile(ctn),re.compile(rm)) if ctn else (cf,ctn,re.compile(rm)) for kw,cf,ctn,rm in zip(kwDf['关键词'],kwDf['类别'],kwDf['包含'].fillna(''),kwDf['排除'])}
    cfIdxDic = {cf:1 for cf in kwDf['类别']}
    firstWdDic = {kw[0]:{'kws':set(),'maxLen':0} for kw in kwDf['关键词']}
    for kw in kwSt:
        if kw[0] in firstWdDic:
            firstWdDic[kw[0]]['kws'].add(kw)
            if len(kw) > firstWdDic[kw[0]]['maxLen']:
                firstWdDic[kw[0]]['maxLen'] = len(kw)
    ptn = '|'.join(kwSt)
    regexCompile = re.compile(ptn)
    return kwSt, kwDic, cfIdxDic, firstWdDic, regexCompile


kwSt, kwDic, cfIdxDic, firstWdDic, regexCompile = deal_keyword(kwFilename)
    
def deal_content(cont):
    cntLt = []
    content = re.sub('(\d)[,，](\d)','\\1\\2',cont)
    if re.search('\n',content):
        tmpCnt = re.split('[,，。!！?？;；\n]', content)
    else:
        tmpCnt = re.split('[,，。!！?？;；\s]', content)
    cntLt = [re.sub('[\s《》\'’‘:：、"“”]+','',x.strip()) 
                for x in tmpCnt if x.strip() and len(x.strip())>5]
    return set(cntLt)
    
def match_stc4(regexCompile, stc, kwDic):
    tmpWdLt = regexCompile.findall(stc)
    wdLt = [wd for wd in tmpWdLt if (not kwDic[wd][1] or kwDic[wd][1].search(stc)) and not kwDic[wd][2].search(stc)]
    return set(wdLt)

def match_from_file(file):
    """
        处理文件，断句，抽取，入库
        数据库有自动去重
        saleInfoList表中salesinfoid与postdate为联合主键
        saleInfoContent表 -- 抽取的结果
        saleInfoList表 -- 新闻基本信息
    """
    salesinfoid = os.path.basename(file).split('.')[0]
    postdate = ''.join(file.split('\\')[-4:-1])
    srcsys = file.split('\\')[-5]
    nextFileflag = False
    insertNewsinfoFlag = True
        
    for stc in deal_content(file):
        if nextFileflag:
            break
        kws = match_stc4(regexCompile, stc, kwDic)
        funs = {kwfundt[kw] for kw in kws}
        for fun in funs:
            if nextFileflag:
                break
            for cnt in fun(stc):
                if insertNewsinfoFlag:
                    # 新闻基本信息只入库一次
                    newsinfo = get_news_info(salesinfoid,postdate,srcsys)
                    if not newsinfo:
                        # 数据库未查询到记录，停止抽取
                        nextFileflag = True
                        break
                    newsinfo = [x if x else '' for x in newsinfo]
                    mentioncar = newsinfo[-2]
                    title = newsinfo[-1]
                    flag = [x for x in ['团购','车展'] if x in title]
                    newsinfo.append(','.join(flag))
                    isInsert = insert_data('saleInfoList', newsinfo)
                    if not isInsert:
                        # 检测到重复值时，停止抽取
                        nextFileflag = True
                        break
                    insertNewsinfoFlag = False
                    
                cnt.insert(0,salesinfoid)
                cnt.insert(1,funcfydt[fun])
                if not cnt[-1]:
                    # 提及车为空时，新闻的车型填充
                    cnt[-1] = mentioncar
                cnt.append(srcsys)
                insert_data('saleInfoContent',cnt)
    conn119.commit()
    
def match_from_cont(cont):
    """
        处理文件，断句，抽取，入库
        数据库有自动去重
        saleInfoList表中salesinfoid与postdate为联合主键
        saleInfoContent表 -- 抽取的结果
        saleInfoList表 -- 新闻基本信息
    """
    result = []
    for stc in deal_content(cont):
        
        # print(stc,regexCompile,kwDic,sep='\n')
        kws = match_stc4(regexCompile, stc, kwDic)
        funs = {kwfundt[kw] for kw in kws}
        for fun in funs:
            for cnt in fun(stc):
                cnt.insert(0,funcfydt[fun])
                result.append(cnt)
    return result
    

if __name__ == '__main__':
    # main()
    s = "理由年按揭免息思域"
    print(match_from_cont(s))



