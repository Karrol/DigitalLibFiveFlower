from django.shortcuts import render, redirect

# 导入 HttpResponse 模块
from django.http import HttpResponse,FileResponse

# 导入数据模型ArticlePost
from .models import ArticlePost

from taggit.managers import TaggableManager
from taggit.models import Tag


# 引入markdown模块
import markdown

# 引入redirect重定向模块
from django.shortcuts import render, redirect, get_object_or_404
# 引入HttpResponse
from django.http import HttpResponse
# 引入刚才定义的ArticlePostForm表单类
from .forms import ArticlePostForm ,CommentForm
# 引入User模型
from django.contrib.auth.models import User
from login.models import Reader

# 引入分页模块
from django.core.paginator import Paginator

# 引入Q对象，实现对多个参数进行查询（标题+正文）
from django.db.models import Q

# 引入栏目Model
from .models import ArticleColumn

# 导入评论Model
from .models import Comment

# 导入推荐图书Model,联系我们的model
from .models import RecbooklistInfo, ContactInfo

#导入新闻公告和服务指南的model
from infoCenter.models import newsColumn_info
from service.models import Category



# 导入刚才定义的RecbooklistInfoForm表单类
from .forms import RecbooklistInfoForm, readerrecomForm

# 引入验证登录的装饰器
from django.contrib.auth.decorators import login_required

import datetime




# Create your views here.

# 读者推荐列表
def recom_list(request):
    recuserinfos = RecbooklistInfo.objects.all()
    return render(request, 'participate/reclist.html',{'recuserinfos':recuserinfos})


# 视图函数
# 文章列表
def article_list(request):
    # 重写文章列表，为了实现排序和搜索
    # 根据GET请求中查询条件
    # 从 url 中提取查询参数，返回不同排序的对象数组
    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column')
    tag = request.GET.get('tag')
    #初始化查询集
    article_list = ArticlePost.objects.all()

    # 用户搜索逻辑,搜索查询集
    if search:
        # 用 Q对象 进行联合搜索
        article_list = article_list.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    else:
        # 将 search 参数重置为空
        search = ''

        # 栏目查询集
        if column is not None and column.isdigit():
            article_list = article_list.filter(column=column)

        # 标签查询集
        if tag and tag != 'None':
            article_list = article_list.filter(tags__name__in=[tag])

        # 查询集排序
        if order == 'total_views':
            article_list = article_list.order_by('-total_views')

    # 每页显示 3 篇文章
    paginator = Paginator(article_list, 3)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    articles = paginator.get_page(page)

    # 需要传递给模板（templates）的对象，并按照order排序
    context = {'articles': articles, 'order': order, 'search': search, 'column': column, 'tag': tag, }
    # render函数：载入模板，并返回context对象
    return render(request, 'participate/list.html', context)

# 文章详情
def article_detail(request, id):
    # 取出相应的文章
    article = ArticlePost.objects.get(id=id)
    # 浏览量+1
    article.total_views += 1
    article.save(update_fields=['total_views'])

    # 取出文章评论
    comments = Comment.objects.filter(article=id)


    # 将markdown语法渲染成html样式
    # 修改markdown样式
    md = markdown.Markdown(
         extensions=[
             # 包含 缩写、表格等常用扩展
             'markdown.extensions.extra',
             # 语法高亮扩展
             'markdown.extensions.codehilite',
             # 目录扩展
             'markdown.extensions.toc',
         ]
    )
    article.body = md.convert(article.body)

    # 需要传递给模板的对象
    context = {'article': article, 'toc': md.toc, 'comments': comments}
    # 载入模板，并返回context对象
    return render(request, 'participate/detail.html', context)

# 写文章的视图
def article_create(request):
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        # # 因为POST的表单中包含了图片文件，所以要将request.FILES也一并绑定到表单类中，否则图片无法正确保存
        article_post_form = ArticlePostForm(request.POST, request.FILES)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_form.save(commit=False)
            # 指定数据库中 id=1 的用户为作者
            # 如果你进行过删除数据表的操作，可能会找不到id=1的用户
            # 此时请重新创建用户，并传入此用户的id
            new_article.author = User.objects.get(id=1)
            # 新增的代码，添加栏目
            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])
            # 将新文章保存到数据库中
            new_article.save()

            # 新增代码，保存 tags 的多对多关系
            article_post_form.save_m2m()

            # 完成后返回到文章列表
            return redirect("participate:article_list")
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        # 赋值上下文
        context = { 'article_post_form': article_post_form, 'columns': columns }
        # 返回模板
        return render(request, 'participate/create.html', context)

# 删文章
def article_delete(request, id):
    # 根据 id 获取需要删除的文章
    article = ArticlePost.objects.get(id=id)
    # 调用.delete()方法删除文章
    article.delete()
    # 完成删除后返回文章列表
    return redirect("participate:article_list")

# 安全删除文章
def article_safe_delete(request, id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        article.delete()
        return redirect("participate:article_list")
    else:
        return HttpResponse("仅允许post请求")


# 更新文章
def article_update(request, id):
    """
    更新文章的视图函数
    通过POST方法提交表单，更新titile、body字段
    GET方法进入初始表单页面
    id： 文章的 id
    """

    # 获取需要修改的具体文章对象
    article = ArticlePost.objects.get(id=id)
    # 判断用户是否为 POST 提交表单数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存新写入的 title、body 数据并保存
            article.title = request.POST['title']
            article.body = request.POST['body']
            # 新增栏目代码
            if request.POST['column'] != 'none':
                article.column = ArticleColumn.objects.get(id=request.POST['column'])
            else:
                article.column = None
            article.save()
            # 新增上传图片代码
            if request.FILES.get('avatar'):
                article.avatar = request.FILES.get('avatar')

            article.tags.set(*request.POST.get('tags').split(','), clear=True)
            article.save()
            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect("participate:article_detail", id=id)
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户 GET 请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 新增栏目代码
        columns = ArticleColumn.objects.all()
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        context = {'article': article, 'article_post_form': article_post_form, 'columns': columns, 'tags': ','.join([x for x in article.tags.names()]),}
        # 将响应返回到模板中
        return render(request, 'participate/update.html', context)

# 文章评论
@login_required(login_url='/login/readerLogin/')
def post_comment(request, article_id):
        article = get_object_or_404(ArticlePost, id=article_id)
        # 处理 POST 请求
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                commentbody = comment_form.cleaned_data['commentbody']
                new_comment=Comment.objects.create(article=article,user=request.user,commentbody=commentbody)
                new_comment.save()
                return redirect(article)
            else:
                return HttpResponse("表单内容有误，请重新填写。")
        # 处理错误请求
        else:
            return HttpResponse("发表评论仅接受POST请求。")



# 读者好书推荐列表
def recom_list(request):
    recuserinfos = RecbooklistInfo.objects.all()
    return render(request, 'participate/reclist.html',{'recuserinfos':recuserinfos})

def donation_rules(request):
    return render(request, 'participate/rules.html')

def group_book(request):
        return render(request, 'participate/groupbook.html')

def donation_treatments(request):
        return render(request, 'participate/treatments.html')

def donation_contact(request):
        return render(request, 'participate/contact.html')

def curatorMail(request):
    return render(request, 'participate/curatorMail.html')

def listHelp(request):
    return render(request, 'participate/listHelp.html')

def listTip(request):
    return render(request, 'participate/listTip.html')

def map(request):
    news_intro_columns = newsColumn_info.objects.filter(nav_display=True)
    side_cotegories = Category.objects.filter(side_display=True)
    context = {
        'news_intro_columns': news_intro_columns,
        'side_cotegories': side_cotegories,
    }

    return render(request, 'participate/map.html', context)

def columnTag(request):
    articles = Tag.objects.all()
    return render(request, 'participate/columnTag.html', {'articles': articles})


def contactus(request):
    contactinfos = ContactInfo.objects.all()
    return render(request, 'participate/contactus.html',{'contactinfos':contactinfos})

# 读者好书推荐
@login_required
def reader_recom(request):
    '''把已有的用户信息读出来，然后判断用户请求是POST还是GET。如果是GET，则显示表单,并将用户已有信息也显示在其中，如果是POST，则接收用户提交的表单信息，然后更新各个数据模型实例属性的值'''
    response = HttpResponse('')
    id = request.user.id
    readerrecom_form = readerrecomForm()
    if request.method == "POST":
        message = '请注意检查填写内容'
        readerrecom_form = readerrecomForm(request.POST)
        if readerrecom_form.is_valid():
            #获取前端表单中的数据，并用变量进行保存
            #zl:表单的数据无效错误在于数据库设计不合理，出版年份不能为DateField
            bookName = readerrecom_form.cleaned_data['bookName']#推荐书名
            bookAuthor = readerrecom_form.cleaned_data['bookAuthor']#书的作者
            bpublisher = readerrecom_form.cleaned_data['bpublisher']
            bpubTime =readerrecom_form.cleaned_data['bpubTime']
            bookISBN =readerrecom_form.cleaned_data['bookISBN']
            bookIntroduction = readerrecom_form.cleaned_data['bookIntroduction']  # 自动完整显示记录数
            RecIdentity =readerrecom_form.cleaned_data['RecIdentity']
            RecDepartment = readerrecom_form.cleaned_data['RecDepartment']
            #创建“读者推荐表”实例，用以在数据库中创建记录
            user=request.user
            reader = Reader.objects.get(user=user)
            today=datetime.date.today()
            recbook = RecbooklistInfo.objects.create(bookName=bookName, bookAuthor=bookAuthor, bpublisher=bpublisher,RecIdentity=RecIdentity,RecDepartment=RecDepartment,RecTime=today  ,bookISBN=bookISBN,bookIntroduction=bookIntroduction, RecName=reader,bpubTime=bpubTime)
            recbook.save()
            message = '推荐成功！感谢您的参与！'
        context = {
                'readerrecom_form': readerrecom_form,
                'message': message,
            }
        return render(request, 'participate/bookrecom.html', context)
    return render(request, 'participate/bookrecom.html', locals())

def download_files(request):
    file = open('./participate/static/files/2016-2018OxfordUniversityPress.xlsx' , 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="2016-2018OxfordUniversityPress.xlsx"'
    return response
