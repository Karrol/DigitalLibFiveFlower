from django import forms


class NewUserForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    readertypeName = forms.CharField(label="读者类型名称", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    bookNumber = forms.IntegerField(label="最大可借图书数", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=gender)


class ChangeUserForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    oldusername = forms.CharField(label="原始用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control','id':'oldusername','placeholder':"请输入原来的用户名"}))
    username = forms.CharField(label="新的用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control','id':'updateusername','placeholder':"请输入新的用户名"}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    readertypeName = forms.CharField(label="读者类型名称", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    bookNumber = forms.IntegerField(label="最大可借图书数", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=gender)
