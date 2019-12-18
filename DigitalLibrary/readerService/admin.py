from django.contrib import admin
from .models import RedSer


class RedSerAdmin(admin.ModelAdmin):
    list_display = ('get_redSerName', 'get_redSerOperator', 'get_redSerPublished', 'get_redSerPubdate')

    def get_redSerName(self, obj):
        return obj.redSerName.name

    def get_redSerOperator(self, obj):
        return obj.redSerOperator.name

    def get_redSerPublished(self, obj):
        return obj.redSerPublished.name

    def get_redSerPubdate(self, obj):
        return obj.redSerPubdate.name

    get_redSerName.short_description = '读者服务'

admin.site.register(RedSer, RedSerAdmin)