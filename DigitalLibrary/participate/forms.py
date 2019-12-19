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



