# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys

from django.db import models
from django.utils.html import format_html
from django.utils.six import python_2_unicode_compatible

reload(sys)
sys.setdefaultencoding("utf-8")


@python_2_unicode_compatible
class Asset(models.Model):
    id = models.AutoField(verbose_name="ID", primary_key=True)
    name = models.CharField(verbose_name="资产名称", max_length=30, null=True, blank=True)
    DTYPE = (
        ('1', '生产设备'),
        ('2', '办公设备'),
        ('3', '测试设备'),
    )
    type = models.CharField(verbose_name="资产类别", choices=DTYPE, default=DTYPE[1], max_length=1)
    assetcode = models.CharField(verbose_name="资产编码", max_length=60, null=True, blank=True)

    def __str__(self):
        return "%s-%s" % (self.name, self.assetcode)

    class Meta:
        verbose_name = '资产编码表'
        verbose_name_plural = '资产编码表'


@python_2_unicode_compatible
class Items(models.Model):
    WHETHER = (
        ('1', '是'),
        ('2', '否'),
    )

    id = models.AutoField(verbose_name="ID", primary_key=True)
    name = models.CharField(verbose_name="项目", max_length=20)
    level = models.CharField(verbose_name="是否一级项目", choices=WHETHER, max_length=1, default=WHETHER[1])
    parent = models.ForeignKey('self', null=True, blank=True, verbose_name="上级项目")

    def __str__(self):
        if self.level == '1':
            return '%s' % self.name
        elif self.level == '2':
            return '%s->%s' % (self.parent, self.name)

    def save(self):
        if self.parent is None:
            self.level = '1'
        else:
            self.level = '2'
        super(Items, self).save()

    class Meta:
        verbose_name = '项目表'
        verbose_name_plural = '项目表'


@python_2_unicode_compatible
class Department(models.Model):
    WHETHER = (
        ('1', '是'),
        ('2', '否'),
    )

    id = models.AutoField(verbose_name="ID", primary_key=True)
    name = models.CharField(verbose_name="部门", max_length=20)
    level = models.CharField(verbose_name="是否一级部门", choices=WHETHER, max_length=1, default=WHETHER[1])
    parent = models.ForeignKey('self', null=True, blank=True, verbose_name="上级部门", on_delete=models.CASCADE)

    def __str__(self):
        if self.level == '1':
            return '%s' % self.name
        elif self.level == '2':
            return '%s->%s' % (self.parent, self.name)

    def save(self):
        if self.parent is None:
            self.level = '1'
        else:
            self.level = '2'
        super(Department, self).save()

    class Meta:
        verbose_name = '部门表'
        verbose_name_plural = '部门表'


@python_2_unicode_compatible
class Physical(models.Model):
    id = models.AutoField(verbose_name="ID", primary_key=True)
    ip = models.GenericIPAddressField(verbose_name="IP地址", blank=True, null=True)
    hostname = models.CharField(verbose_name="主机名", max_length=200, blank=True, null=True)
    username = models.CharField(verbose_name="用户名", max_length=60, blank=True, null=True)
    password = models.CharField(verbose_name="密码", max_length=100, blank=True, null=True)
    assertid = models.ForeignKey(Asset, verbose_name="资产编码", null=True, blank=True, on_delete=models.DO_NOTHING)
    idracip = models.GenericIPAddressField(verbose_name="IDRAC_IP", blank=True, null=True)
    cpunum = models.SmallIntegerField(verbose_name="CPU数量(物理)", blank=True, null=True)
    cpuphysicalcores = models.SmallIntegerField(verbose_name="单个CPU物理核心数", blank=True, null=True)
    cpulogicalcores = models.SmallIntegerField(verbose_name="逻辑CPU数", blank=True, null=True)
    cpuother = models.CharField(verbose_name="CPU其他信息", max_length=80, blank=True, null=True)
    memsize = models.CharField(verbose_name="内存大小", max_length=100, blank=True, null=True)
    disksize = models.CharField(verbose_name="硬盘大小", max_length=400, blank=True, null=True)
    os = models.CharField(verbose_name="操作系统", max_length=50, blank=True, null=True)
    # os = models.ForeignKey(Os, verbose_name="操作系统", on_delete=models.DO_NOTHING)
    uuid = models.CharField(verbose_name="识别码", max_length=60, blank=True, null=True)
    vcenterid = models.ForeignKey('self', null=True, blank=True, verbose_name="所属vCenter")
    DTYPE = (
        ('1', '物理机'),
        ('2', 'VMWARE'),
        ('3', 'vCenter')
    )
    type = models.CharField(verbose_name="设备类型", choices=DTYPE, default=DTYPE[0], max_length=1, blank=True, null=True)
    item = models.ForeignKey(Items, verbose_name="所属项目", null=True, blank=True)
    department = models.ForeignKey(Department, verbose_name="所属部门", null=True, blank=True)
    STAT = (
        ('1', '在线'),
        ('2', '下线'),
        ('3', '故障'),
    )
    status = models.CharField(verbose_name="设备状态", choices=STAT, default=STAT[0], max_length=1)
    POS = (
        ('1', '深圳办公机房'),
        ('2', '上海办公机房'),
        ('3', '世纪互联机房'),
    )
    position = models.CharField(verbose_name="位置", max_length=1, choices=POS, default=POS[0], blank=True, null=True)
    createtime = models.DateField(verbose_name="项目开始时间", blank=True, null=True)
    destroytime = models.DateField(verbose_name="项目完成时间", blank=True, null=True)
    starttime = models.DateField(verbose_name="设备启用时间", blank=True, null=True)
    endtime = models.DateField(verbose_name="设备弃用时间", blank=True, null=True)
    updatetime = models.DateTimeField(verbose_name="修改时间", auto_now=True, blank=True, null=True)

    def __str__(self):
        return u'%s' % (self.ip)

    def devicestatus(self):
        if self.status == '1':
            format_ht = format_html("<span style='font-weight:bold;padding:2px;color:#008800'>在线</span>")
        elif self.status == '2':
            format_ht = format_html("<span style='font-weight:bold;padding:2px;color:#BBBBBB'>下线</span>")
        elif self.status == '3':
            format_ht = format_html("<span style='font-weight:bold;padding:2px;color:#DD0000'>故障</span>")

        return format_ht

    devicestatus.short_description = "状态"

    class Meta:
        verbose_name = '物理服务器表'
        verbose_name_plural = '物理服务器表'


@python_2_unicode_compatible
class Virtual(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    ip = models.CharField(verbose_name="IP", max_length=500, blank=True, null=True)
    hostname = models.CharField(max_length=200, verbose_name="主机名", null=True, blank=True)
    cpunum = models.SmallIntegerField(verbose_name="CPU核心数", null=True, blank=True)
    memsize = models.CharField(max_length=100, verbose_name="内存(MB)", null=True, blank=True)
    disksize = models.CharField(max_length=400, verbose_name="磁盘(GB)", null=True, blank=True)
    os = models.CharField(verbose_name="OS", max_length=50, blank=True, null=True)
    uuid = models.CharField(verbose_name="识别码", max_length=60, blank=True, null=True)
    host = models.ForeignKey(Physical, verbose_name="所属物理主机", null=True, blank=True)
    item = models.ForeignKey(Items, verbose_name="所属项目", null=True, blank=True)
    department = models.ForeignKey(Department, verbose_name="所属部门", null=True, blank=True)
    createtime = models.DateField(verbose_name="创建时间", blank=True, null=True)
    destroytime = models.DateField(verbose_name="销毁时间", blank=True, null=True)
    updatetime = models.DateTimeField(auto_now=True, verbose_name="修改时间", blank=True, null=True)

    def __str__(self):
        return u'%s->%s' % (self.hostname, self.ip)

    class Meta:
        verbose_name = '虚拟机表'
        verbose_name_plural = '虚拟机表'


@python_2_unicode_compatible
class Weight(models.Model):
    id = models.AutoField(verbose_name="ID", primary_key=True)
    type = models.CharField(verbose_name="组件类型", max_length=10)
    weight = models.CharField(verbose_name="所占权重", max_length=10, blank=True, null=True)

    def __str__(self):
        return "%s-%s" % (self.type, self.weight)

    class Meta:
        verbose_name = '权重表'
        verbose_name_plural = '权重表'


@python_2_unicode_compatible
class Statistics(models.Model):
    id = models.AutoField(verbose_name="ID", primary_key=True)
    proportion = models.CharField(verbose_name="项目所占比重", max_length=10, null=True, blank=True)
    host = models.ForeignKey(Physical, verbose_name="物理服务器", on_delete=models.DO_NOTHING, null=True, blank=True)
    item = models.ForeignKey(Items, verbose_name="项目", on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return u'%s-%s' % (self.host__ip, self.item__name)

    class Meta:
        verbose_name = '统计表'
        verbose_name_plural = '统计表'
