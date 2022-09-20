from email import message
import os
from turtle import title
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.shortcuts import render,HttpResponse,redirect
import json
from fsspec import filesystem
from jinja2 import FileSystemBytecodeCache
from requests import request
from sqlalchemy import outparam
from sciapp.models import Article
from sciapp import models
from . import forms
# Create your views here.
import hashlib
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt,csrf_protect #Add this
from chardet import detect
from django.core.files.storage import FileSystemStorage
import PyPDF2
import sys
sys.path.append("D:\discourse_code\code\preprocess\pdfminer")
import re
from pdftest2 import PDFprocess
from getSummary import getSummary
from autogenerate import autogenerate
from pdf2doc import todoc

# from txtprocess import txtprocess

#密码加密
def hash_code(s, salt='mysite'):# 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def index(request):
    if request.session.get('is_login', None):     #已经登录
        message="您已经登录，如需注册请退出登录"
        return render(request, 'index.html',locals())


    return render(request, 'index.html')


def login(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        
        return redirect('/')

    if request.method == "POST":
            login_form = forms.UserForm(request.POST)
            #print(username, password)
            message = '请检查填写的内容！'
            
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
            # 用户名字符合法性验证
            # 密码长度验证
            # 更多的其它验证.....

            #python内置的locals(),它返回当前所有的本地变量字典
                try:
                    # 那一串数据
                    user = models.User.objects.get(name=username)
                except:
                    message = '用户不存在！'
                    return render(request, 'login.html', locals())

                #登陆成功，修改session的登陆状态
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name

                    return redirect('/')
                else:
                    message = '密码不正确！'
                    return render(request, 'login.html', locals())
            else:
                return render(request, 'login.html', locals())
    login_form = forms.UserForm()
    return render(request, "login.html",locals())

#登出，需要修改session
def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/login/")

    #flush清空
    #request.session.flush()
    # 或者使用下面的方法
    del request.session['is_login']
    del request.session['user_id']
    del request.session['user_name']
    return redirect("/")



def register(request):

    if request.session.get('is_login', None):     #已经登录
        message="您已经登录，如需注册请退出登录"
    
    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')

            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, 'register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已经被注册了！'
                    return render(request, 'register.html', locals())

                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()

                return redirect('/login')     #跳转到登录界面
        else:
            return render(request, 'register.html', locals())
    register_form = forms.RegisterForm()
    
    return render(request, 'register.html', locals())

def self_index(request):

    # aritcles=models.Article.objects.all()
    articles=models.Article.objects.all()
    return render(request,'self_index.html',locals())

@csrf_exempt
#所有收藏
def self_index_allstar(request):
   
    if request.is_ajax():
        # 直接获取所有的post请求数据
       
        title = request.POST.get("title")
        author=request.POST.get("authors")
        publishdate=request.POST.get("published1")
        source=request.POST.get("source1")
        address=request.POST.get("address1")
        stardate=request.POST.get("stardate1")
        # 获取其中的某个键的值
        new_article = models.Article()        
        new_article.article_title=title
        new_article.authors=author
        new_article.publish_date=publishdate
        new_article.onlineorlocal=source
        new_article.url=address
        new_article.stardate=stardate
        new_article.belonger=request.session['user_name']
        new_article.save()

        article = models.Article0()     
        article.article_title=title
        article.authors=author
        article.publish_date=publishdate
        article.onlineorlocal=source
        article.url=address 
        article.save()
       
    articles=models.Article.objects.all()
    return render(request, 'allstar.html', locals())

@csrf_exempt  
#最近下载
def self_index_latestdownload(request):
    if request.is_ajax():
        # 直接获取所有的post请求数据
        

        title = request.POST.get("title")
        author=request.POST.get("authors")
        publishdate=request.POST.get("published1")
        source=request.POST.get("source1")
        address=request.POST.get("address1")
        stardate=request.POST.get("stardate1")
        # 获取其中的某个键的值
        new_article = models.latestdownload()
        new_article.article_title=title
        new_article.authors=author
        new_article.publish_date=publishdate
        new_article.onlineorlocal=source
        new_article.url=address
        new_article.downloaddate=stardate
        new_article.belonger=request.session['user_name']
        
        new_article.save()

        article = models.Article0()     
        article.article_title=title
        article.authors=author
        article.publish_date=publishdate
        article.onlineorlocal=source
        article.url=address 
        article.save()
       
    articles=models.latestdownload.objects.all()
    return render(request, 'latestdownload.html', locals())

@csrf_exempt  
#最近阅读
def self_index_latestread(request):
    if request.is_ajax():
        # 直接获取所有的post请求数据
        
        title = request.POST.get("title")
        author=request.POST.get("authors")
        publishdate=request.POST.get("published1")
        source=request.POST.get("source1")
        address=request.POST.get("address1")
        stardate=request.POST.get("stardate1")
        # 获取其中的某个键的值
        new_article = models.latestread()
        new_article.article_title=title
        new_article.authors=author
        new_article.publish_date=publishdate
        new_article.onlineorlocal=source
        new_article.url=address
        new_article.readdate=stardate
        new_article.belonger=request.session['user_name']
        new_article.save()


        article = models.Article0()     
        article.article_title=title
        article.authors=author
        article.publish_date=publishdate
        article.onlineorlocal=source
        article.url=address 
        article.save()
       
    articles=models.latestread.objects.all()
    return render(request, 'latestread.html', locals())




@csrf_exempt 
def summary(request):
    needtosummary=''
    
    if request.method == 'POST':

        if request.POST.get("filepath"):
            if str(request.POST.get("filepath")).split('.')[-1]!='pdf':
                message="请勿上传非PDF文件"
                return render(request, 'summary.html', locals())
            
            
            else:
                path=request.POST.get("filepath")
                pdfprocess=PDFprocess(path)
                abstracttxt,origintxt=pdfprocess.parse()
                
                summary1=getSummary(origintxt)
                result,englishresult=summary1.getsummary()
                
        else:
            if request.POST.get("input_summary"):
                needtosummary=str(request.POST.get("input_summary"))
                summary1=getSummary(needtosummary)
                
                result1,englishresult1=summary1.getrawsummary()
        
        # 导出成PPT
    return render(request, 'summary.html', locals())


@csrf_exempt 
def xiaogongju(request):
    #PPT
    if request.POST.get("input"):
        #md生成
        info=request.POST.get("input")
        lines=info.split('\n')
        outputresult=''
        
        for line in lines:
            if re.findall('^[0-9]{1}[\.\s]+[A-Z][a-zA-Z\s\w\S]+$|^[0-9]{1}[\.\s]*[0-9]{1}[\.\s]+[A-Z][a-zA-Z\s\w\S]+$',line):
                outputresult=outputresult+r"\newpage"+'\n'
                outputresult=outputresult+'#'+line+'\n'
            elif line:
                outputresult=outputresult+'p>'+line+'\n'
            else:
                continue
        ppt_outputpath=request.POST.get("pptsavepath")
        ppt_outputpath=ppt_outputpath+"\\1.md"
        with open(ppt_outputpath,"a",encoding='UTF-8',errors='ignore') as test:
            test.write(outputresult)

        pptsavepath=request.POST.get("pptsavepath")+"\\output.pptx"
        #PPT生成         
        a=autogenerate(pptsavepath,ppt_outputpath,15)
        a.allmain()   
        

        return render(request, 'pdf2word.html', locals())
    #word

    if request.POST.get("pdfpath"):
        pdfpath=request.POST.get("pdfpath")
        savepath=request.POST.get("savepath")
        savepath=savepath+"\\output.doc"
        a=todoc(pdfpath,savepath)
        a.doc()

        return render(request, 'pdf2word.html', locals())
    
    return render(request, 'pdf2word.html', locals())
    
   


