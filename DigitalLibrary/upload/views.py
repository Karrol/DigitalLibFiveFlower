from django.shortcuts import render
from .models import *
import os
# Create your views here.
import os, shutil, copy
import time
from libs import ajax
from django.shortcuts import render
from login.models import Reader
import os
from django.http import HttpResponse,HttpResponseRedirect,StreamingHttpResponse
from . import models
from django.views.decorators.csrf import csrf_exempt


def upload_views(request):
	# 请求方法为POST时,进行处理;
	if request.method == "POST":
		# 获取上传的用户名称
		#nkname = request.POST['nkname']
		uname = request.POST['uname']
		#查询File表中与登录的用户一致的文件数据
		L = Files.objects.filter(uname=uname,isActive=True)
		L1 = Files.objects.filter(uname=uname,isActive=False)
		# 获取上传的文件,如果没有文件,则默认为None;
		File = request.FILES.get("myfile", None)
		LJ='./media/文件'
		folder_name='%s'%str(uname)

		if os.path.exists(LJ+'/'+folder_name):
			pass
		else:
			os.mkdir(os.path.join(LJ,folder_name))
		if File is None:
			a='请选择上传文件!'
			return render(request,'upload/fp1.html',locals())
		else:
			#判断该用户上传文件目录下是否有本次上传文件
			lujing = "./media/文件/"+"%s"%str(uname)+"/"+"%s"%File.name
			#用户已上传本次上传文件
			if File.name in os.listdir(r"./media/文件/"+"%s"%str(uname)):
				a='你已上传%s,上传失败!'%File.name
				return render(request,'upload/fp1.html',locals())
			else:
				# 打开特定的文件进行二进制的写操作;
				with open(lujing,'wb+') as f:
					# 分块写入文件;
					for chunk in File.chunks():
						f.write(chunk)
				#文件信息存储到数据库
				dic={
					'wenjian':File.name,
					'lujing':lujing,
					'uname':uname,
				}
				Files(**dic).save()
				a='上传成功!!'
				return render(request,'upload/fp1.html',locals())

@csrf_exempt
def index(request):
    uname=request.user.username
    L = Files.objects.filter(uname=request.user.username,isActive=True)
    L1 = Files.objects.filter(uname=request.user.username,isActive=False)
    """分片上传"""
    print("sssss")
    if request.method == 'POST':
    # print("分片上传")
        upload_file = request.FILES.get('file') # 获取分片
        task = request.POST.get('task_id')  # 获取文件唯一标识符
        print("分片", task)
        real_file_name = upload_file._name
        chunk = request.POST.get('chunk', 0)
        print("分片上传", chunk)
        filename = './media/file/%s%s' % (task, chunk)
        if not os.path.exists(filename):
            try:
               with open(filename, 'wb') as f:
                    # for obj in upload_file.chunks():
                    #     f.write(obj)
                    f.write(upload_file.read())
                    f.close()
            except Exception as e:
                print(e, 111)

    documents = Files.objects.all()
    return ajax.ajax_template(request, 'upload/fp1.html', locals())


@csrf_exempt
def upload_success(request):
    """所有分片上传成功"""
    uname = request.user.username
    print("所有分片上传成功")

    task = request.POST.get('task_id')
    print("所有分片", task)
    ext = request.POST.get('ext', '')
    print('ext:', ext)
    upload_type = request.POST.get('type')
    print('upload_type:', upload_type)
    name = request.POST.get('name')
    print('name:', name)
    if len(ext) == 0 and upload_type:
        ext = upload_type.split('/')[1]
    chunk = 0
    with open("./media/file/%s" % name, 'wb') as target_file:  # 创建新文件
        while True:
            try:
                filename = './media/file/%s%s' % (task, chunk)
                source_file = open(filename, 'rb')  # 按序打开每个分片
                target_file.write(source_file.read())  # 读取分片内容写入新文件
                source_file.close()
                os.remove(filename)  # 删除该分片，节约空间
            except Exception as e:
                # 找不到碎片文件跳出循环
                print(e, 222)
                break
            chunk += 1
        target_file.close()

        # 系统当前时间年份
        year = time.strftime('%Y')
        # 月份
        month = time.strftime('%m')
        # 日期
        day = time.strftime('%d')
        # 具体时间 小时分钟毫秒
        mdhms = time.strftime('%m%d%H%M%S')
        print("年", year)
        mymovefile("./media/file/%s" % name,
                   "./media/文件/"+"%s"%str(uname))

        # 把路径储存入数据库中
        models.Files.objects.create(
            lujing="./media/文件/"+"%s"%str(uname)+"/"+"%s" %name, wenjian=str(name),uname=uname,)

        return HttpResponse("上传成功")

    return ajax.ajax_data(name)

@csrf_exempt
def list_exist(request):
    """判断该文件上传了多少个分片"""
    name = request.POST.get('filename')
    uname = request.user.username
    chunk = 0
    data = {}
    filename = "./media/文件/%s/"%uname+"%s"%name
    print(filename)

    # 判断上传的文件是否存在
    if os.path.exists(filename):
        data['flag_exist'] = True
        data['file_path'] = filename
    else:
        data['flag_exist'] = False
    list = []
    while True:
        if os.path.exists("./media/file/%s%s" % (name, chunk)):
            list.append(chunk)
        else:
            break
        chunk += 1
    data['list'] = list
    print('判断该文件上传了多少个分片',data)
    return ajax.ajax_data(data)

@csrf_exempt
# 移动文件到新文件路径
def mymovefile(srcfile, dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))
    else:
        fpath, fname = os.path.split(dstfile)  # 分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)  # 创建路径
        shutil.move(srcfile, dstfile)  # 移动文件
        print("move %s -> %s" % (srcfile, dstfile))

@csrf_exempt
# 复制文件到新文件路径
def mycopyfile(srcfile, dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))
    else:
        fpath, fname = os.path.split(dstfile)  # 分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)  # 创建路径
        shutil.copyfile(srcfile, dstfile)  # 复制文件
        print("copy %s -> %s" % (srcfile, dstfile))

def wother_views(request):
	#我上传的文件
	if request.method=='GET':
		uname=request.GET['uname']
		L=Files.objects.filter(uname=uname,isActive=True)
		LJ='media/文件'
		a='只能操作单个文件'
		return render(request,'other/file.html',locals())
	elif request.method=='POST':
		#获取登陆用户
		uname=request.POST['uname']
		#获取登陆用户的昵称
		#nkname=Users.objects.get(uname=uname).nkname
		#获取要共享给的用户
		yonghu=request.POST['yonghu']
		#获取要共享出去的文件
		file=request.POST['wenjian']
		#得到登陆用户所有上传的文件L
		L=Files.objects.filter(uname=uname,isActive=True)
		L1=Files.objects.filter(uname=uname,isActive=False)
		#查看文件表中file文件是否为登陆用户上传，
		list1=Files.objects.filter(uname=uname,wenjian=file,isActive=True)
		#查看用户表是否存在yonghu的数据
		user_list=Reader.objects.filter(email=yonghu)
		if list1 :
			#如果是登陆用户上传，再判断共享给的用户yonghu是否拥有file文件
			list2=Files.objects.filter(uname=yonghu,lujing=list1[0].lujing,wenjian=file)
			if len(user_list)==0:
				a='%s'%yonghu+'不存在'
				return render(request,'other/file.html',locals())
			elif yonghu=='' or yonghu==uname:
				a='请选择要共享的用户'
				return render(request,'other/file.html',locals())
			elif list2 :
				#共享给的用户拥有file文件！共享不成功
				a='%s'%yonghu+'已拥有'+'%s'%file
				return render(request,'other/file.html',locals())
			else:
				#共享隔得用户没有file文件，添加数据到数据库保存，共享成功
				dic={'wenjian':file,'lujing':list1[0].lujing,'uname':yonghu,'isActive':False,'shareduser':uname}
				Files(**dic).save()
				a='共享成功'
				return render(request,'other/file.html',locals())
		else:
			#如果不是登陆用户上传，获取file文件信息，
			list3=Files.objects.filter(uname=uname,wenjian=file,isActive=False)
			#判断file文件是否已有用户共享给要共享的用户
			list4=Files.objects.filter(uname=yonghu,wenjian=file,lujing=list3[0].lujing)
			if len(user_list)==0:
				a='%s'%yonghu+'不存在'
				return render(request,'other/file.html',locals())
			elif yonghu=='' or yonghu==uname:
				a='请选择要共享的用户'
				return render(request,'other/file1.html',locals())
			elif list4 :
				#如果需共享的用户已拥有file文件
				a='%s'%yonghu+'已拥有'+'%s'%file
				return render(request,'other/file1.html',locals())
			else:
				#如果需共享的用户没有file文件，添加数据保存数据库，共享成功
				dic={'wenjian':file,'lujing':list3[0].lujing,'uname':yonghu,'isActive':False,'shareduser':uname}
				Files(**dic).save()
				a='共享成功'
				return render(request,'other/file1.html',locals())

def other_views(request):
	#别人共享给我的文件
	if request.method=='GET':
		#nkname=request.GET['nkname']
		uname=request.GET['uname']
		L1=Files.objects.filter(uname=uname,isActive=False)
		return render(request,'other/file1.html',locals())

def open_views(request):
	if request.method=='GET':
		file=request.GET['i']
		uname=request.GET['uname']
		l=Files.objects.get(uname=uname,wenjian=file)
		f=open(l.lujing,'rb')
		#如果要打开的文件后缀为'.bmp','.jif','.jpg','.png'时打开方式为图片打开，否则直接打开源文件
		if os.path.splitext(l.lujing)[1]=='.bmp' or os.path.splitext(l.lujing)[1]=='.jif'\
		or os.path.splitext(l.lujing)[1]=='.jpg' or os.path.splitext(l.lujing)[1]=='.png':
			return StreamingHttpResponse(f,content_type="image/png")
		else:
			return StreamingHttpResponse(f)
	elif request.method=='POST':
		file=request.POST['wenjian']
		uname=request.POST['uname']
		lujing=request.POST['lujing']
		file_list=Files.objects.get(wenjian=file,uname=uname,lujing=lujing)
		f=open(file_list.lujing,'rb')
		response=HttpResponse(f)
		#文件下载类型选择未知
		response['Content-Type']='application/octet-stream'
		#选择下载类型弹出保存框,下载后文件名为wjm或x.wenjian
		response['Content-Disposition']="attachment;filename="+file_list.wenjian
		return response
