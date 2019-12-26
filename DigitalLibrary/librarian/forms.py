from django import forms
from login.models import Reader, readerType
from search.models import ebook_info ,bookEntity_info , bookshelf_info, booktype_info
from readerCenter.models import Borrowing
from readerService.models import CD,bookReser

'''class NewUserForm(forms.Form):
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
    sex = forms.ChoiceField(label='性别', choices=gender)'''

class ReaderForm(forms.ModelForm):
    class Meta:
        model = Reader
        fields = ['name','Password','balance','max_borrowing','Sex']

class AddReaderForm(forms.ModelForm):
    class Meta:
        model = Reader
        fields = ['name','Password','email','balance','max_borrowing','Sex']

class BookshelfForm(forms.ModelForm):
    class Meta:
        model = bookshelf_info
        fields = "__all__"
        exclude = ["bookshelfID"]

class BookForm(forms.ModelForm):
    class Meta:
        model = bookEntity_info
        fields = "__all__"


class EbookForm(forms.ModelForm):
    class Meta:
        model = ebook_info
        fields = "__all__"

class BookTypeForm(forms.ModelForm):
    class Meta:
        model = booktype_info
        fields = "__all__"
        exclude = ["btID"]

class ReaderTypeForm(forms.ModelForm):
    class Meta:
        model = readerType
        fields = "__all__"

class BorrowingForm(forms.ModelForm):
    class Meta:
        model = Borrowing
        fields = "__all__"


class CDForm(forms.ModelForm):
    class Meta:
        model = CD
        fields = "__all__"

class reserForm(forms.ModelForm):
    class Meta:
        model = bookReser
        fields = "__all__"
