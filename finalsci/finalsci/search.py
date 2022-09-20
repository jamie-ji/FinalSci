# HTTP协议以"请求－回复"的方式工作。客户发送请求时，可以在请求中附加数据。
# 服务器通过解析请求，就可以获得客户传来的数据，并根据URL来提供特定的服务。

#接受用户的请求,请求处理和视图显示

import imp
from datasets import AutomaticSpeechRecognition
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators import csrf
import arxiv
from torchaudio import list_audio_backends
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import sys
sys.path.append("../preprocess/")
import ydfanyi


# 接收请求数据,默认按照时间排序
def search(request):  
    fanyi=ydfanyi.YouDaoFanyi('7a8e1e60f26f8514','rSZorXXlhX6tglvqvZsOXl2jQVn81MOI')




    request.encoding='utf-8'
    sort="relevence"
    year=[]
    if 'sort' in request.POST and request.POST['sort']:
        sort = request.POST['sort']

    if 'search' in request.GET and request.GET['search']:
        message = request.GET['search']

    if 'year' in request.POST and request.POST['year']:
        year=request.POST.getlist('year')
    


    search_sortbyrelevence = arxiv.Search(
        
    query = request.GET['search'],
    #max_results=5,
    sort_by = arxiv.SortCriterion.Relevance    #排序类型，可以选择根据时间submittedDate，最近更新lastUpdatedDate，相关度relevance
)
    #根据发表时间
    search_sortbypublish = arxiv.Search(
        
    query = request.GET['search'],
   #max_results=5,
    sort_by = arxiv.SortCriterion.SubmittedDate    #排序类型，可以选择根据时间submittedDate，最近更新lastUpdatedDate，相关度relevance
)   

    #根据更新日期
    search_sortbyupdate = arxiv.Search(
        
    query = request.GET['search'],
    #max_results=5,
    sort_by = arxiv.SortCriterion.LastUpdatedDate   #排序类型，可以选择根据时间submittedDate，最近更新lastUpdatedDate，相关度relevance
)   




    list_title=[]
    list_chinese_title=[]
    list_author=[]                #作者
    list_pdfurl=[]                 #下载链接
    list_abstract=[]               #摘要
    list_url=[]                   #原文链接
    list_published=[]                          #最新更新日期
    list_chinese_abstract=[]            #中文简介
    list_links1=[]
    

    if sort=="publishdate":
        for result in search_sortbypublish.results():
            if year:
                for tiaojian in year:
                    if str(result.published).split('-')[0] ==tiaojian:


                        list_title.append(result.title)
                        list_chinese_title.append(fanyi.translate(result.title))
                        list_author.append(str(result.authors[0]))
                        list_pdfurl.append(result.pdf_url)
                        list_abstract.append(result.summary)
                        list_url.append(result.entry_id)
                        list_published.append(str(result.published))
                        list_chinese_abstract.append(fanyi.translate(result.summary))
            else:
                        list_title.append(result.title)
                        list_chinese_title.append(fanyi.translate(result.title))
                        list_author.append(str(result.authors[0]))
                        list_pdfurl.append(result.pdf_url)
                        list_abstract.append(result.summary)
                        list_url.append(result.entry_id)
                        list_published.append(str(result.published))
                        list_chinese_abstract.append(fanyi.translate(result.summary))
            
            
        
       
    elif sort=="update":
        for result in search_sortbyupdate.results():
            if year:
                for tiaojian in year:
                    if str(result.published).split('-')[0] ==tiaojian:


                        list_title.append(result.title)
                        list_chinese_title.append(fanyi.translate(result.title))
                        list_author.append(str(result.authors[0]))
                        list_pdfurl.append(result.pdf_url)
                        list_abstract.append(result.summary)
                        list_url.append(result.entry_id)
                        list_published.append(str(result.published))
                        list_chinese_abstract.append(fanyi.translate(result.summary))
            else:
                        list_title.append(result.title)
                        #list_chinese_title.append(fanyi.translate(result.title))
                        list_author.append(str(result.authors[0]))
                        list_pdfurl.append(result.pdf_url)
                        list_abstract.append(result.summary)
                        list_url.append(result.entry_id)
                        list_published.append(str(result.published))
                        list_chinese_abstract.append(fanyi.translate(result.summary))
              
        
    else:
        for result in search_sortbyrelevence.results():
            if year:
                for tiaojian in year:
                    if str(result.published).split('-')[0] ==tiaojian:


                        list_title.append(result.title)
                        list_chinese_title.append(fanyi.translate(result.title))
                        list_author.append(str(result.authors[0]))
                        list_pdfurl.append(result.pdf_url)
                        list_abstract.append(result.summary)
                        list_url.append(result.entry_id)
                        list_published.append(str(result.published))
                        list_chinese_abstract.append(fanyi.translate(result.summary))
            else:
                        list_title.append(result.title)
                        list_chinese_title.append(fanyi.translate(result.title))
                        list_author.append(str(result.authors[0]))
                        list_pdfurl.append(result.pdf_url)
                        list_abstract.append(result.summary)
                        list_url.append(result.entry_id)
                        list_published.append(str(result.published))
                        list_chinese_abstract.append(fanyi.translate(result.summary))
            
            
        
    titlenum=len(list_title)
        
    return render(request, 'result.html',{"result":message,
                                        "year":year,
                                        "sort":sort,
                                        "list_title":list_title,
                                        "list_chinese_title":json.dumps(list_chinese_title),
                                        "list_chinese_abstract":json.dumps(list_chinese_abstract),
                                        "titlenum":titlenum,
                                        "list_author":list_author,
                                        "list_pdfurl":list_pdfurl,
                                        "list_url":list_url,
                                        "list_published":list_published,
                                        "list_abstract":list_abstract})
   
   
    #return render(request, 'result.html')

