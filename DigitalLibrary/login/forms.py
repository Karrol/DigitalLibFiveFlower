from django import forms
from .models import person_info,Reader,librarian_info
from django.contrib.auth.models import User
from captcha.fields import CaptchaField

#读者登录表单
class readerLogin(forms.Form):
    username = forms.CharField(
        max_length=256,
        label="邮箱",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'name': 'username',
            'id': 'id_username',
        })
    )
    password = forms.CharField(
        label="密码",
        max_length=256,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'type': 'password',
            'name': 'password',
            'id': 'id_password',
        }),)
    captcha = CaptchaField(label='验证码')

#馆员登录表单
class librarianLogin(forms.Form):
    username = forms.CharField(
        max_length=16,
        label="工号",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'name': 'username',
            'id': 'id_username',
        })
    )
    password = forms.CharField(
        label="密码",
        max_length=256,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'type': 'password',
            'name': 'password',
            'id': 'id_password',
        }),)
    captcha = CaptchaField(label='验证码')





#张丽：只有读者有注册界面
class RegisterForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    username = forms.CharField(
        label=u'用户名/邮箱',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'name': 'username',
            'id': 'id_username',
        }),
    )

    password1 = forms.CharField(
        label=u'密码',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'name': 'password',
            'id': 'id_password',
        }),
    )
    password2 = forms.CharField(
        label=u'重复密码',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'type': 'password',
            'name': 're_password',
            'id': 'id_re_password',
        }),
    )

    name = forms.CharField(
        label=u'读者姓名',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'name': 'name',
            'id': 'id_name',
        }),
    )

    '''photo = forms.FileField(
        label=u'头像',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'name': 'photo',
            'id': 'id_photo',
        }),
        required=False,
    )      '''

    sex = forms.ChoiceField(label='性别', choices=gender)
    captcha = CaptchaField(label='验证码')



class ResetPasswordForm(forms.Form):
    old_password = forms.CharField(
        label=u'原始密码：',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'name': 'old_password',
            'id': 'id_old',
        }),
    )
    new_password = forms.CharField(
        label=u'新密码：',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'name': 'new_password',
            'id': 'id_new',
        }),
    )
    repeat_password = forms.CharField(
        label=u'重复密码：',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'name': 'repeat_password',
            'id': 'id_repeat',
        }),
    )