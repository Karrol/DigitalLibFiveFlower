from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
import datetime
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Reader
from .forms import readerLogin,librarianLogin,RegisterForm,ResetPasswordForm

# Create your views here.

#reader_login
def reader_login(request):
    #禁止用户重复登录
    if request.session.get('is_login', None):
        return redirect('/index')
    #设置Tag用于login.html进行识别
    Tag='readerLogin'
    if request.method == "POST":
        login_form = readerLogin(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            email = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                # 与数据中的User表进行对比
                user = User.objects.get(username=email)
                if user.password == password:
                    # 往session中写值，session可以作为一个字典集合，在HTTP请求时会同时进行传递，可以实现页面传参鸭
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_email'] = user.username
                    #张丽：TO DO 用户存在返回首页，这里的首页暂且search的检索首页
                    return redirect("readerCenter:profile")
                else:
                    message = "登录密码不正确！"
            except:
                message = "读者不存在！"
        #locals()可以返回views中所有的变量
        return render(request, 'login/login.html', locals())
    #没有传输数据的话，就重新返回登录界面，这里也是初始登录界面的渲染
    login_form = readerLogin()
    return render(request, 'login/login.html', locals())


#librarian_login
def librarian_login(request):
    # 禁止用户重复登录
    if request.session.get('is_login', None):
        return redirect('/index')
    #判断数据传输模式
    if request.method == "POST":
        login_form = readerLogin(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            email = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                # 与数据中的User表进行对比
                user = User.objects.get(username=email)
                if user.password == password:
                    # 往session中写值，session可以作为一个字典集合，在HTTP请求时会同时进行传递，可以实现页面传参鸭
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_email'] = user.username
                    #张丽：TO DO 用户存在返回首页，这里的首页暂且search的检索首页
                    return redirect("readerCenter:profile")
                else:
                    message = "登录密码不正确！"
            except:
                message = "读者不存在！"
        #locals()可以返回views中所有的变量
        return render(request, 'login/login.html', locals())
    #没有传输数据的话，就重新返回登录界面，这里也是初始登录界面的渲染
    login_form = readerLogin()
    return render(request, 'login/login.html', locals())

#reader sign in
def user_register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST,request.FILES)
        nowtime=datetime.date.today()
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            name = register_form.cleaned_data['name']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/register.html', locals())
            else:
                same_email_user = Reader.objects.filter(email=username)
                if same_email_user:  # 用户名唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'login/register.html', locals())

                # 当一切都OK的情况下，创建新用户
                new_user = User.objects.create(username=username)
                new_user.set_password(password1)#set_password方法可以实现密码加密
                new_user.save()
                new_reader = Reader.objects.create(user=new_user, name=name, email=username,inTime = nowtime)
                new_reader.Sex = sex
                auth.login(request, new_user)
                new_reader.save()
                message="注册成功"

                return redirect('login:readerLogin')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())


#用户修改密码
@login_required
def set_password(request):
    user = request.user
    state = None
    if request.method == 'POST':
        old_password = request.POST.get('old_password', '')
        new_password = request.POST.get('new_password', '')
        repeat_password = request.POST.get('repeat_password', '')

        if user.check_password(old_password):
            if not new_password:
                state = 'empty'
            elif new_password != repeat_password:
                state = 'repeat_error'
            else:
                user.set_password(new_password)
                user.save()
                state = 'success'

    context = {
        'state': state,
        'resetPasswordForm': ResetPasswordForm(),
    }

    return render(request, 'login/set_password.html', context)


#用户登出
@login_required
def user_logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/index/")


