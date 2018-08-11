from django.conf.urls import url
from .views import register, edit, UserUpdateView

app_name = 'users'

urlpatterns = [

    url(r'^register/$', register, name='register'),
    # edit
    # url(r'^edit/(\d+)/$', edit, name='edit'),

    # 通用视图类
    url(r'^edit/(?P<pk>\d+)/$', UserUpdateView.as_view(), name='edit'),

]
