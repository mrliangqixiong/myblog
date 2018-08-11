import markdown
from django.db import models
from users.models import User
from django.urls import reverse
from django.utils.html import strip_tags


# Create your models here.
# 类别
class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


# 标签
class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


# 帖子
class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    # 摘要
    excerpt = models.CharField(max_length=200, blank=True, null=True, verbose_name='简介')
    # 创建时间
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 更新时间
    modified_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    # 定义关联关系
    category = models.ForeignKey('Category', verbose_name='类别')
    tag = models.ManyToManyField('Tag', blank=True, verbose_name='标签')
    author = models.ForeignKey(User, verbose_name='作者')
    # 增加文章阅读次数,默认为0
    views = models.PositiveIntegerField(default=0)

    # 重写save方法
    def save(self, *args, **kwargs):
        # 如果没有指定摘要,则自动生成
        if not self.excerpt:
            # 首先生成markdown的对象实例
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 先将 Markdown 文本渲染成 HTML 文本
            # strip_tags 去掉 HTML 文本的全部 HTML 标签
            # 从文本摘取前 54 个字符赋给 excerpt
            self.excerpt = strip_tags(md.convert(self.content))[:100]
            # 调用父类的save方法将数据保存到数据库中
        super(Post, self).save(*args, **kwargs)

    # 增加计算阅读次数方法,
    def increase_views(self):
        # 每次调用此方法,就把views+1
        self.views += 1
        self.save(update_fields=['views'])

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # /post/1/
        return reverse('blog:detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = '帖子'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']
