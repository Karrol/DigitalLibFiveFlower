from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from login.models import Reader
from .forms import LoginForm,RegisterForm,ResetPasswordForm

# Create your views here.


#用户登录（目前采用的电话登录方式）
def user_login(request):
    # 判断用户是否已经登录,会有自动登录的情况存在，主要是浏览器记录了账号密码
    if request.user.is_authenticated:
        return redirect('search:searchindex')
    # 状态变量，用于在决定视图中渲染的提示消息
    state = None
    # 获取表单数据
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 检验账号、密码是否正确匹配数据库中的某个用户
        # 如果均匹配则返回这个 user 对象，authenticate()方法验证用户名称和密码是否匹配，如果是，则将这个用户数据返回
        user = auth.authenticate(username=username, password=password)
        # 判断登录用户是否属于系统中已注册用户
        if user:
            # 检验用户账号是否被激活，系统默认登录时，此语句将永远不会被执行
            #当用户自行登录时，登录成功会跳转到用户个人中心中
            if user.is_active:
                auth.login(request, user)
                return redirect('readerCenter:profile')
            else:
                return HttpResponse(u'您的账户未激活！')
        else:
            state = 'not_exist_or_password_error'

    context = {
        'loginForm': LoginForm(),
        'state': state,
    }

    return render(request, 'login/login.html', context)


#用户注册（目前采用的电话登录方式）  (to do:转换注册方式)
def user_register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    registerForm = RegisterForm()

    state = None
    if request.method == 'POST':
        registerForm = RegisterForm(request.POST, request.FILES)
        password = request.POST.get('password', '')
        repeat_password = request.POST.get('re_password', '')
        if password == '' or repeat_password == '':
            state = 'empty'
        elif password != repeat_password:
            state = 'repeat_error'
        else:
            username = request.POST.get('username', '')
            name = request.POST.get('name', '')
            if User.objects.filter(username=username):
                state = 'user_exist'
            else:
                new_user = User.objects.create(username=username)
                new_user.set_password(password)
                new_user.save()
                new_reader = Reader.objects.create(user=new_user, name=name, phone=int(username))
                new_reader.photo = request.FILES['photo']
                new_reader.save()
                state = 'success'

                auth.login(request, new_user)

                context = {
                    'state': state,
                    'registerForm': registerForm,
                }
                return render(request, 'login/register.html', context)

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
    return HttpResponseRedirect('/')
