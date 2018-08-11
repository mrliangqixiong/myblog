# -*-coding:utf-8-*-
from django.contrib.syndication.views import Feed

from .models import Post


# 编写自定义的Feed类
class AllPostFeed(Feed):
    # 配置显示在聚合阅读器上的标题
    title = 'Django博客'

    # 配置通过聚合阅读器访问博客的首页
    link = '/index/'

    # 配置显示在聚合阅读器上的描述信息
    description = 'Django博客项目演示测试'

    # 需要显示的内容条目
    def items(self):
        return Post.objects.all()

    # 聚合阅读器中显示的内容条目的标题
    def item_title(self, item):
        return '[%s]%s' % (item.category, item.title)

    # 聚合器中显示的内容条目的描述
    def item_description(self, item):
        return item.content
