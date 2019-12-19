from django.contrib import admin
from .models import bookshelf_info, bookEntity_info,book_info,ebook_info,booktype_info

admin.site.register(bookshelf_info)
admin.site.register(bookEntity_info)
admin.site.register(book_info)
admin.site.register(ebook_info)
admin.site.register(booktype_info)
# Register your models here.
