from django.db import models



class Files(models.Model):
	#文件名
	wenjian = models.CharField(max_length=20)
	#文件路径
	lujing = models.CharField(max_length=60)
	#拥有此文件用户
	uname = models.CharField(max_length=14)
	#用户如何拥有的文件，默认True为上传，False为别人共享
	isActive = models.BooleanField(default=True)
	#共享给我的用户名，默认为null
	shareduser = models.CharField(max_length=14)
