"""finalsci URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views,testdb,search
from django.conf.urls import url
from django.urls import include
from captcha.views import captcha_refresh

urlpatterns = [
    #数据库管理
    url(r'^admin/', admin.site.urls),

    #主页
    path('',views.index),

    #登录
    path('login/',views.login),
    #注册
    path('register/',views.register),

    #退出
    path('logout/',views.logout),
    path('search/logout/',views.logout),
    path('self_index/logout/',views.logout),

    #path('testdb/', testdb.testdb),
    #搜索跳转
    url(r'^search/$', search.search),
    
    
    

    
    path('captcha/', include('captcha.urls'))   ,
    path('refresh/', captcha_refresh),      # 点击可以刷新验证码


    path('self_index/',views.self_index ),
    #所有收藏
    path('allstar/', views.self_index_allstar, name='allstar'),
    #最近下载
    path('latestdownload/', views.self_index_latestdownload, name='latestdownload'),
    #最近阅读
    path('latestread/', views.self_index_latestread, name='latestread'),
    #删除记录
    
    
   
    # 摘要生成窗口

    url(r'^summary/$',views.summary ),

    url(r'^xiaogongju/$',views.xiaogongju),
    
]
