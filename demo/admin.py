# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from demo.models import *
from forms import PhysicalForm
from .tasks import collectdata

reload(sys)
sys.setdefaultencoding("utf-8")

admin.site.site_header = "运维自动化管理系统"
admin.site.site_title = "运维自动化管理系统"
admin.site.site_url = "/admin"


class BaseAdmin(admin.ModelAdmin):
    list_per_page = 50
    show_full_result_count = True
    ordering = ('id',)


@admin.register(Items)
class ItemsAdmin(BaseAdmin):
    list_display = ('id', 'name', 'level', 'parent')
    search_fields = ('name',)
    list_filter = ('parent', 'level')


@admin.register(Physical)
class PhysicalAdmin(BaseAdmin):
    def collectdata(self, request, queryset):
        result = collectdata.delay(queryset)
        self.message_user(request, "采集任务的ID是: %s" % result.id)

    list_display = (
        'ip', 'devicestatus', 'cpunum', 'cpuphysicalcores', 'cpulogicalcores',
        'cpuother', 'memsize', 'disksize', 'os', 'uuid', 'type', 'item', 'department', 'position', 'updatetime')
    search_fields = ('hostname', 'assertid__name')
    list_filter = ('type',)
    list_display_links = ('ip',)
    actions = (collectdata,)
    form = PhysicalForm
    fieldsets = [
        ('初始数据', {'fields': ['ip', 'hostname', 'username', 'password', 'type', 'os', 'status', 'position']}),
        ('关联项', {'fields': ['item', 'department', 'assertid', 'vcenterid']}),
        ('时间', {'fields': ['starttime', 'endtime', 'createtime', 'destroytime']}),
        ('自动采集项', {
            'fields': ['idracip', 'cpunum', 'cpuphysicalcores', 'cpulogicalcores', 'cpuother', 'disksize', 'memsize',
                       'uuid']}),
    ]
    collectdata.short_description = "收集选中服务器的信息"


@admin.register(Virtual)
class VirtualAdmin(BaseAdmin):
    list_display = (
        'hostname', 'cpunum', 'memsize', 'disksize', 'uuid', 'os', 'host', 'item', 'department',
        'createtime',
        'destroytime', 'updatetime')
    list_filter = ('host__ip','os')
    search_fields = ('ip','hostname')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'level', 'parent')
    list_filter = ('parent', 'name')


@admin.register(Weight)
class WeightAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'weight')
    search_fields = ('type',)


@admin.register(Statistics)
class StatisticsAdmin(admin.ModelAdmin):
    list_display = ('id', 'host', 'item', 'proportion')


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'assetcode')

# user = User.objects.get(username='admin')
# user.set_password('ipanel123')
# print 'save'
# user.save()
