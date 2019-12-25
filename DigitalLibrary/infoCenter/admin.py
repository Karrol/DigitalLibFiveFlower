from django.contrib import admin
from .models import newsColumn_info, newsArticle_info, weekbook_info, rank_info, rank_book

class newsColumnAdmin(admin.ModelAdmin):
    list_display = ('columnName','columnSlug', 'abstract', 'nav_display')

class newsArticleAdmin(admin.ModelAdmin):
    list_display = ('newsTitle', 'newsColumn', 'newsAuthor', 'newsPubdate', 'newsPublished')
    raw_id_fields = ("newsAuthor",)

class RecbookAdmin(admin.ModelAdmin):
    raw_id_fields = ("ISBN",'promugator')
    list_display = ('bookName', 'recTime', 'promugator')

class BookInline(admin.TabularInline):
    model = rank_book
    raw_id_fields = ("book",)

class RankAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['rankName', 'rankIntro', 'rankDisplay']}),
    ]
    inlines = [BookInline]


admin.site.register(weekbook_info, RecbookAdmin)
admin.site.register(newsColumn_info, newsColumnAdmin)
admin.site.register(newsArticle_info, newsArticleAdmin)
admin.site.register(rank_info, RankAdmin)