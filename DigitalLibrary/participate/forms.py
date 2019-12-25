# 引入表单类
from django import forms
# 引入文章模型
from .models import ArticlePost, RecbooklistInfo
# 引入评论模型
from .models import Comment


# 写文章的表单类
class ArticlePostForm(forms.ModelForm):
    class Meta:
        # 指明数据模型来源
        model = ArticlePost
        # 定义表单包含的字段
        fields = ('title', 'body', 'tags', 'avatar')

# 写评论的表单
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['commentbody']


# 推荐书的表单

class RecbooklistInfoForm(forms.ModelForm):
    class Meta:
        # 指明数据模型来源
        model = RecbooklistInfo
        # 定义表单包含的字段
        fields = ('bookName', 'bookAuthor', 'bpublisher', 'bpubTime', 'bookISBN', 'bookIntroduction', 'RecName', 'RecIdentity', 'RecDepartment')
        # 禁止模型转换的字段，可选，若设置了该属性，fields则可以不设置
        # 设置HTML元素控件的label标签，可选

        # 设置表单字段的CSS样式，可选
        # 定义字段的类型，可选，默认时自动转换的
        # 设置提示信息
        # 自定义错误信息
        error_messages = {
            # 设置全部错误信息
            '__all__': {'required': '请输入内容',
                        'invalid': '请检查输入内容'},
        }

    # 步骤3： 自定义表单字段的数据清洗


class readerrecomForm(forms.Form):
    RecIdentitychoice = [
        (u'本科生', u'本科生'),
        (u'研究生', u'研究生'),
    ]
    RecDepartmentchoice = [
        (u'公共管理学院', u'公共管理学院'),
        (u'文学与新闻学院', u'文学与新闻学院'),
        (u'电子信息学院', u'电子信息学院'),
    ]

    bookName = forms.CharField(
        max_length=50,
        label="图书名称",
        widget=forms.TextInput(attrs={
            'class': 'form-control  ',
            'name': 'bookName',
        }),
        required=False,)

    bookAuthor = forms.CharField(
        max_length=20,
        label="图书作者",
        widget=forms.TextInput(attrs={
            'class': 'form-control  ',
            'name': 'bookAuthor',
        }),
        required=False, )

    bpublisher = forms.CharField(
        max_length=30,
        label="出版社",
        widget=forms.TextInput(attrs={
            'class': 'form-control  ',
            'name': 'bpublisher',
        }),
        required=False, )

    bpubTime = forms.DateField(

        label="出版时间",
        widget=forms.TextInput(attrs={
            'class': 'form-control  ',
            'name': 'bpubTime',
        }),
        required=False, )

    bookISBN = forms.CharField(

        label="ISBN编号",
        widget=forms.TextInput(attrs={
            'class': 'form-control  ',
            'name': 'bookISBN',
        }),
        required=False, )

    bookIntroduction = forms.CharField(

        label="简短介绍",
        widget=forms.TextInput(attrs={
            'class': 'form-control  ',
            'name': 'bookIntroduction',
        }),
        required=False, )

    RecName = forms.CharField(

        label="推荐人",
        widget=forms.TextInput(attrs={
            'class': 'form-control  ',
            'name': 'RecName',
        }),
        required=False, )


    RecIdentity = forms.CharField(
        max_length=20,
        label="推荐人身份：",
        widget=forms.widgets.Select(
            choices=RecIdentitychoice,
            attrs={
                'class': 'form-control input-lg',
                'name': 'RecIdentity',
            },

        ),
        required=False, )

    RecDepartment = forms.CharField(
        max_length=50,
        label="推荐人单位：",
        widget=forms.widgets.Select(
            choices=RecDepartmentchoice,
            attrs={
                'class': 'form-control input-lg',
                'name': 'RecDepartment',
            },
        ),
        required=False, )





