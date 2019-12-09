from django import forms
from .models import person_info,Reader,librarian_info
from django.contrib.auth.models import User
class LoginForm(forms.Form):
    #张丽：widget的attrs是在设置渲染出来的HTML代码中的<textinput class="",name="",id="">
    role_type = (
        (0, '读者'),
        (1, '图书馆员'),
    )
    
    role = forms.ChoiceField(
        label='登录身份:',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'name': 'role',
            'id': 'id_role',
        }),
        choices=role_type,
        initial=role_type[0])

    username = forms.CharField(
        max_length=16,
        label=u'用户名：',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'name': 'username',
            'id': 'id_username',
        })
    )
    password = forms.CharField(
        label=u'密码：',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'password',
            'name': 'password',
            'id': 'id_password',
        }),
    )

#张丽：只有读者有注册界面
class RegisterForm(forms.Form):
    username = forms.CharField(
        label=u'用户名/电子邮箱：',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'name': 'username',
            'id': 'id_username',
        }),
    )
    name = forms.CharField(
        label=u'读者姓名：',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'name': 'name',
            'id': 'id_name',
        }),
    )
    password = forms.CharField(
        label=u'密码：',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'name': 'password',
            'id': 'id_password',
        }),
    )
    re_password = forms.CharField(
        label=u'重复密码：',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'type': 'password',
            'name': 're_password',
            'id': 'id_re_password',
        }),
    )
    '''phone = forms.CharField(
        label=u'联系电话：',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'name': 'phone',
            'id': 'id_phone',
        }),
        required=False,
    )  '''

    photo = forms.FileField(
        label=u'头像：',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'name': 'photo',
            'id': 'id_photo',
        }),
        required=False,
    )

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