from django.db import models
from numpy import identity
from prometheus_client import Summary

# Create your models here.

# 表名为APP名_类名,如下表为sciapp_Article

#----------建表
#修改后，都需要python manage.py makemigrations  先创建模型
# 接着python manage.py migrate     真正建表


#sciapp_article表，表示收藏
class Article0(models.Model):
    # 属性 name
    article_title = models.CharField(max_length=128)
    authors=models.CharField(max_length=50)
    publish_date=models.CharField(max_length=50)
    # 要么文件地址，要么网站链接
    source=(
        ('local','本地'),
        ('online','网络'),
    )
    onlineorlocal=models.CharField(max_length=32, choices=source, default="网络")
    
    url=models.CharField(max_length=128)
    #使用__str__方法帮助人性化显示对象信息；
    c_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.article_title
    #元数据里定义用户按创建时间的反序排列，也就是最近的最先显示；
    class Meta:
        ordering = ["-c_time"]
        verbose_name = "文章"
        verbose_name_plural = "文章"


#sciapp_article表，表示收藏
class Article(models.Model):
    # 属性 name
    article_title = models.CharField(max_length=128)
    authors=models.CharField(max_length=50)
    publish_date=models.CharField(max_length=50)
    # 要么文件地址，要么网站链接
    source=(
        ('local','本地'),
        ('online','网络'),
    )
    onlineorlocal=models.CharField(max_length=32, choices=source, default="网络")
    
    url=models.CharField(max_length=128)
    stardate=models.CharField(max_length=50)
    belonger=models.CharField(max_length=50)       #所属于用户

   
    #使用__str__方法帮助人性化显示对象信息；
    c_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.article_title
    #元数据里定义用户按创建时间的反序排列，也就是最近的最先显示；
    class Meta:
        ordering = ["-c_time"]
        verbose_name = "收藏文章"
        verbose_name_plural = "收藏文章"

class latestread(models.Model):
    article_title = models.CharField(max_length=128)
    authors=models.CharField(max_length=50)
    publish_date=models.CharField(max_length=50)
    source=(
            ('local','本地'),
            ('online','网络'),
        )

    onlineorlocal=models.CharField(max_length=32, choices=source, default="网络")
    
    url=models.CharField(max_length=128)
    readdate=models.CharField(max_length=50)
    belonger=models.CharField(max_length=50)       #所属于用户

    #使用__str__方法帮助人性化显示对象信息；
    c_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.article_title
    #元数据里定义用户按创建时间的反序排列，也就是最近的最先显示；
    class Meta:
        ordering = ["-c_time"]
        verbose_name = "最近阅读"
        verbose_name_plural = "最近阅读"

class latestdownload(models.Model):
    article_title = models.CharField(max_length=128)
    authors=models.CharField(max_length=50)
    publish_date=models.CharField(max_length=50)
    source=(
            ('local','本地'),
            ('online','网络'),
        )
    onlineorlocal=models.CharField(max_length=32, choices=source, default="网络")
    
    belonger=models.CharField(max_length=50)       #所属于用户
    url=models.CharField(max_length=128)
    downloaddate=models.CharField(max_length=50)
    c_time = models.DateTimeField(auto_now_add=True)
    #使用__str__方法帮助人性化显示对象信息；
    def __str__(self):
        return self.article_title
    #元数据里定义用户按创建时间的反序排列，也就是最近的最先显示；
    class Meta:
        ordering = ["-c_time"]
        verbose_name = "最近下载"
        verbose_name_plural = "最近下载"

# 笔记本功能
class notebook(models.Model):
    title = models.CharField(max_length=128)   #笔记本标题
    date=models.CharField(max_length=50)    #创建日期
    content=models.CharField(max_length=256)    #内容
    belonger=models.CharField(max_length=50)       #所属于用户
    
    c_time = models.DateTimeField(auto_now_add=True)
    #使用__str__方法帮助人性化显示对象信息；
    def __str__(self):
        return self.title
    #元数据里定义用户按创建时间的反序排列，也就是最近的最先显示；
    class Meta:
        ordering = ["-c_time"]
        verbose_name = "笔记本"
        verbose_name_plural = "笔记本"






#用户表，包括用户名，密码，邮箱，性别，创建时间
class User(models.Model):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    #name: 必填，最长不超过128个字符，并且唯一，也就是不能有相同姓名；
    name = models.CharField(max_length=128, unique=True)
    #password: 必填，最长不超过256个字符（实际可能不需要这么长
    password = models.CharField(max_length=256)
    #email: 使用Django内置的邮箱类型，并且唯一；
    email = models.EmailField(unique=True)
    #sex: 性别，使用了一个choice，只能选择男或者女，默认为男；
    sex = models.CharField(max_length=32, choices=gender, default="男")

    c_time = models.DateTimeField(auto_now_add=True)
    #使用__str__方法帮助人性化显示对象信息；
    def __str__(self):
        return self.name
    #元数据里定义用户按创建时间的反序排列，也就是最近的最先显示；
    class Meta:
        ordering = ["-c_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"