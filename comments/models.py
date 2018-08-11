from django.db import models


# Create your models here.

class Comment(models.Model):
    name = models.CharField(max_length=20, verbose_name='名字')
    email = models.EmailField(verbose_name='邮箱')
    url = models.URLField(verbose_name='网址')
    text = models.TextField(verbose_name='评论内容')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')

    # 定义外键关系
    post = models.ForeignKey('blog.Post')

    def __str__(self):
        return self.text[:20]
