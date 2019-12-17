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
