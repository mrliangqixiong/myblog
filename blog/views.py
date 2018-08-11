import markdown
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Post, Category, Tag
from comments.forms import CommentForm
from utils import custom_paginator
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension


# Create your views here.
# def index(request):
#     post_list = Post.objects.all().order_by('-created_time')
#     return render(request, 'index.html', locals())

# 重写视图类
class IndexView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'post_list'
    # 开启分页功能,每页放2条数据
    paginate_by = 3

    # 重写get_context_data,以便放入我们的起始页码 和结束页码
    def get_context_data(self, **kwargs):
        # 调用父类的get_context_data方法
        context = super().get_context_data(**kwargs)
        # 获取分页相关的变量
        page = context.get('page_obj')
        paginator = context.get('paginator')
        # 调用我们自定义的分页方法
        start, end = custom_paginator(page.number, paginator.num_pages, 4)
        # 将我们的start 和 end 写入context中
        context.update({
            'page_range': range(start, end + 1)
        })
        # 返回context
        return context


# 归档日期标签时间
# def archives(request, year, month):
#     post_list = Post.objects.filter(created_time__year=year, created_time__month=month).order_by('-created_time')
#     return render(request, 'index.html', locals())

# 重写视图类,归档日期标签时间
class ArchivesView(IndexView):
    def get_queryset(self):
        return super().get_queryset().filter(created_time__year=self.kwargs.get('year'),
                                             created_time__month=self.kwargs.get('month'))


# 基于函数的视图函数
# 归档分类条数
# def categories(request, pk):
#     # 根据pk取得category对象
#     category = get_object_or_404(Category, pk=pk)
#     # 根据取得category来正向查找post
#     # post_list = Post.objects.filter(category=category).order_by('-created_time')
#
#     # 反向查
#     post_list = category.post_set.all()
#     return render(request, 'index.html', {'post_list': post_list})

# 重写视图类,归档分类条数
class CategoriesView(IndexView):
    def get_queryset(self):
        category = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(category=category)


# 详细内容markdown语法
# def detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     # 相当于对post.content多了一个中间步骤，先将 Markdown 格式的文本渲染成 HTML 文本再传递给模板
#     post.content = markdown.markdown(post.content, extensions=[
#         'markdown.extensions.extra',
#         'markdown.extensions.codehilite',
#         'markdown.extensions.toc', ])
#     # 生成评论form表单
#     form = CommentForm
#     # 把post评论列表传到前台
#     comment_list = post.comment_set.all().order_by('-created_time')
#     # 增加计算阅读次数
#     post.increase_views()
#     return render(request, 'blog/detail.html', locals())

# 重写视图详细类
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    # 重写get的方法,以便我们可以执行我们的自己定义的increase_views方法
    def get(self, *args, **kwargs):
        # 调用父类的get方法,以便self.object中有我们的需要的post实例对象
        response = super().get(*args, **kwargs)
        # 调用我们的自己定义的increase_views方法
        self.object.increase_views()
        return response

    # 重写get_object方法,以便支持markdown语法
    def get_object(self, queryset=None):
        # 复写get_object方法的目的是国为需要对post的body值进行渲染
        post = super().get_object()
        # 对post的content进行markdown处理
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])
        post.content = md.convert(post.content)
        post.toc = md.toc
        return post

    # 重写get_context_data方法,以便往context中写入额外的变量
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # 调用父类的get_context_data,获得已有context对象
        form = CommentForm()  # 生成前台需要使用的评论表单
        post = context['post']  # 获取post实例
        comment_list = post.comment_set.all().order_by('-created_time')  # 查出post对应的评论列表
        # 使用字典的update方法,来更新context字典
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context  # 最后返回更新后的context


# 标签视图函数
class TagsView(IndexView):
    # 重写get_queryset方法,修改默认的查询行为
    def get_queryset(self):
        # 先根据pk查出tag对象
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        # 有了tag对象之后,根据这个tag对象,查出tag下的post文章
        return super().get_queryset().filter(tag=tag)


def search(request):
    # 获取q变量
    q = request.GET.get('q')
    # 定义一个错误提示变量
    error_mg = ''
    # 判断q是否存在,即用户是否输入搜索关键词
    if not q:
        # 如果存在,则提示用户输入搜索关键词
        error_mg = '请输入搜索关键词'
        # 返回首页
        return render(request, 'index.html', {'error_mg':error_mg})
    # 如果用户提交了搜索关键词,那么使用搜索关键词搜索
    post_list = Post.objects.filter(Q(title__icontains=q)|Q(content__icontains=q))
    return render(request, 'index.html', {'post_list':post_list})

def about(request):
    return render(request,'blog/about.html')

def contact(request):
    return render(request,'blog/contact.html')