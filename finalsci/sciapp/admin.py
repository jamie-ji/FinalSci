from django.contrib import admin

# Register your models here.

# 注册模型
# 实现数据库增删改查
from . import models

admin.site.register(models.User)
admin.site.register(models.Article)
admin.site.register(models.latestdownload)
admin.site.register(models.latestread)
admin.site.register(models.Article0)
admin.site.register(models.notebook)
