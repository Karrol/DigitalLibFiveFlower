from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Reader
from .forms import LoginForm,RegisterForm,ResetPasswordForm

# Create your views here.


#用户登录，通过role角色选择决定跳转页面
def user_login(request):
    #避免用户重复登录
    if request.user.is_authenticated:
        #TO DO:这里跳转回图书馆首页，逻辑上才通顺
        return redirect("readerCenter:profile")
    
    state = None

    if request.method == 'POST':
        #获取表单数据
        userRole=request.POST.get('role')
        username = request.POST.get('username')
        password = request.POST.get('password')
        #利用Django内置登录方法进行用户验证
        user = auth.authenticate(username=username, password=password)
        if user:
            #TO DO:如果用户是激活状态的，就登录-这有安全bug
            if user.is_active:
                auth.login(request, user)
                #判断用户分组，读者跳转个人中/检索界面
                if int(userRole)==0:
                    return redirect('readerCenter:profile')
                #馆员跳转管理界面
                if int(userRole)==1:
                    return redirect('librarian:index')
                #防止数据库端在输入馆员信息时出现误操作
                return HttpResponse(u'Your account do not blong to any type of user in this website.')
            else:
                return HttpResponse(u'Your account is disabled.')
        else:
            state = 'not_exist_or_password_error'

    context = {
        'loginForm': LoginForm(),
        'state': state,
    }

    return render(request, 'login/login.html', context)


#用户注册（采用邮箱注册的方式）
def user_register(request):
    #已登录用户不可在登录状态下注册
    if request.user.is_authenticated:
        # TO DO:这里跳转回图书馆首页，逻辑上才通顺
        return redirect('readerCenter:profile')
    #实例化注册表单，只有读者需要注册
    registerForm = RegisterForm()
    state = None
    if request.method == 'POST':
        #为了上传头像
        registerForm = RegisterForm(request.POST, request.FILES)
        #首先判断表单的密码输入是否正确，获取password\repeat_password字段
        password = request.POST.get('password', '')
        repeat_password = request.POST.get('re_password', '')
        if password == '' or repeat_password == '':
            state = 'empty'
        elif password != repeat_password:
            state = 'repeat_error'
        else:
            #判断用户名是否存在，获取username、name字段
            username = request.POST.get('username', '')
            name = request.POST.get('name', '')
            if User.objects.filter(username=username):
                state = 'user_exist'
            else:
                #检查无误后创建新用户
                #给内置User表单赋值
                new_user = User.objects.create(username=username)
                new_user.set_password(password)
                new_user.save()
                #给Reader表单赋值,email和User中的username应该一致
                new_reader = Reader.objects.create(user=new_user, name=name, email=username)
                new_reader.photo = request.FILES['photo']
                new_reader.save()
                #用户注册成功：User注册+Reader表中注册
                state = 'success'
                #注册成功后自动登录
                auth.login(request, new_user)
                
                context = {
                    'state': state,
                    'registerForm': registerForm,
                }
                return render(request, 'login/register.html', context)
    #在没有成功注册时，state=none,此时应返回未提交前的表单
    context = {
        'state': state,
        'registerForm': registerForm,
    }

    return render(request, 'login/register.html', context)



#用户修改验证码
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
    auth.logout(request)
    return redirect("login:login")
