# -*-coding:utf-8-*-
from django.conf.urls import url
# from .views import index, detail, archives, categories
# 重写视图类
from .views import IndexView, CategoriesView, ArchivesView, PostDetailView, TagsView, search, about, contact


app_name = 'blog'

# urlpatterns = [
#     url(r'^index/$', index, name='index'),
#     url(r'^post/(?P<pk>\d+)/$', detail, name='detail'),
#     url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', archives, name='archives'),
#     url(r'^categories/(?P<pk>\d+)/$', categories, name='categories')
# ]

# 重写视图类
urlpatterns = [
    url(r'^index/$', IndexView.as_view(), name='index'),
    url(r'^post/(?P<pk>\d+)/$', PostDetailView.as_view(), name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', ArchivesView.as_view(), name='archives'),
    url(r'^categories/(?P<pk>\d+)/$', CategoriesView.as_view(), name='categories'),
    url(r'^tags/(?P<pk>\d+)/$', TagsView.as_view(), name='tags'),
    # 简单的搜索功能
    # url(r'^search/$',search,name='search'),
    url(r'^about/$',about,name='about'),
    url(r'^contact/$',contact,name='contact'),

]