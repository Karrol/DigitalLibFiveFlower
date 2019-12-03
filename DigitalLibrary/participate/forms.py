# 引入文章模型
from .models import ArticlePost
# 引入评论模型
from .models import Comment
from django import forms


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
