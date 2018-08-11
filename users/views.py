from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView

from users.models import User
from .forms import RegisterForm, EditForm


# Create your views here.
def register(request):
    # 获取next即跳转地址
    redirect_to = request.POST.get('next', request.GET.get('next', ''))
    # 首先判断request.method是否是post方法
    if request.method == 'POST':
        # 使用request中的数据,初始化form表单
        form = RegisterForm(request.POST, request.FILES)
        # 判断form表单的数据是否合法
        if form.is_valid():
            # 合法则保存
            form.save()
            # 提示信息
            messages.success(request, '注册成功,请登录!')
            # 处理跳转
            if redirect_to:
                # 跳转到redirect_to所指定的页面
                return redirect(redirect_to)
            else:
                # 跳转到首页
                return redirect(reverse('login'))
    else:
        # 如果不是post方法,即是get方法,返回注册页面
        # 创建一个fomr实例对象
        form = RegisterForm()
        # 渲染注册页面
        return render(request, 'users/register.html', {'form': form, 'next': redirect_to})


# 定义用户信息修改的视图函数
@login_required(login_url='/users/login/')
def edit(request):
    # 判断request的请求方法,如果是post方法,那么就处理数据
    if request.method == 'POST':
        # 使用post数据去更新一个model的数据的写法,传入post数据的同时还要传入实例对象
        form = EditForm(request.POST, instance=request.user)
        # 判断是否合法
        if form.is_valid():
            # 如果合法,则保存数据
            user = form.save(commit=False)
            # 设置手动保存用户上传的头像
            user.headshot = request.FILES.get('headshot')
            user.save()
            # 保存成功,提示用户
            messages.success(request, '信息修改成功!')
    # 让前台能够显示已有的信息,使用user对象去初始化form表单
    form = EditForm(instance=request.user)
    return render(request, 'users/edit_form.html', {'form': form})
    # 如果是get方法,就返回用户信息修改页面


# 　通用视图类
class UserUpdateView(UpdateView):
    model = User
    form_class = EditForm
    template_name = 'users/edit_form.html'

    # 重写form_valid 自定义form表单的行为
    def form_valid(self, form):
        # 获取用户上传的头像
        headshot = self.request.FILES.get('headshot')
        # 将用户上传的头像赋给user对象
        form.instance.headshot = headshot
        # 调用父类的form_valid方法
        return super().form_valid(form)
