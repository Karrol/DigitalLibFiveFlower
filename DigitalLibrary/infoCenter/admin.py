from django.contrib import admin
from .models import newsColumn_info, newsArticle_info, weekbook_info, rank_info, rank_book

class newsColumnAdmin(admin.ModelAdmin):
    list_display = ('columnName','columnSlug', 'abstract', 'nav_display', 'newsIndexDiaplay')
    list_filter = ['nav_display', 'newsIndexDiaplay']

class newsArticleAdmin(admin.ModelAdmin):
    list_display = ('newsTitle', 'newsColumn', 'newsAuthor', 'newsPubdate', 'newsPublished', 'topDisplay')
    list_filter = ['newsColumn', 'newsPubdate', 'newsPublished']

    raw_id_fields = ("newsAuthor",)

    search_fields = ['newsTitle']

class RecbookAdmin(admin.ModelAdmin):
    raw_id_fields = ("ISBN",'promugator')
    list_display = ('bookName', 'recTime', 'promugator')
    list_filter = ['recTime']

class BookInline(admin.TabularInline):
    model = rank_book
    raw_id_fields = ("book",)

class RankAdmin(admin.ModelAdmin):
    list_display = ('rankName', 'rankDisplay', 'rankIntro')
    list_filter = ['rankDisplay']
    search_fields = ['rankName']

    fieldsets = [
        (None, {'fields': ['rankName', 'rankIntro', 'rankDisplay']}),
    ]
    inlines = [BookInline]


admin.site.register(weekbook_info, RecbookAdmin)
admin.site.register(newsColumn_info, newsColumnAdmin)
admin.site.register(newsArticle_info, newsArticleAdmin)
admin.site.register(rank_info, RankAdmin)