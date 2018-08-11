# -*-coding:utf-8-*-
from django import template
from ..models import Post, Category, Tag
from django.db.models import Count

register = template.Library()


# 最新文章模板标签, 可以切片
@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-created_time')[0:num]


# 归档模板标签
@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')


# 分类模板标签
@register.simple_tag
def get_categories():
    return Category.objects.annotate(num_post=Count('post')).filter(num_post__gt=0)


# 获取标签列表
@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_post=Count('post')).filter(num_post__gt=0)