# -*- coding: utf-8 -*-
 
from re import A
from django.http import HttpResponse
 
from sciapp.models import Article
 
# 数据库操作
def testdb(request):
    test1 = Article(publish_date='123')
    test1.save()
    return HttpResponse("<p>数据添加成功！</p>")

