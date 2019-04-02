# -*- coding: utf-8 -*-

import sys

from celery import task
from django.utils import timezone

from collector.physical import collect
from collector.vmwarecollector import Esxi
from models import Physical, Virtual

reload(sys)
sys.setdefaultencoding("utf-8")


@task
def add(x, y):
    return x + y


@task
def collectdata(queryset):
    # pdata = []
    # vdata = []
    for i in queryset.all():
        if i.type == '1':
            print "---------- starting collect physical data ------------"
            info = collect(i.ip, i.username, i.password)
            Physical.objects.filter(id=i.id).update(**info)
            # pdata.append(info)
            print "---------- ending collect physical data ------------"
        elif i.type == '2':
            print "---------- starting collect vmware host data ------------"
            vcenter = Physical.objects.get(id=i.vcenterid.id)
            print(i.ip)
            esxi = Esxi(address=vcenter.ip, user=vcenter.username, password=vcenter.password)

            # get the Esxi host's info & update the host info
            code, hosts, message = esxi.search_host(i.ip)
            print(code, hosts, message)
            # for host in hosts:
            info = esxi.gethostinfo(hosts)
            print(info)
            Physical.objects.filter(id=i.id).update(**info)

            # get the Esxi host's vms info & update their info
            vms = esxi.get_vms_by_ip(i.ip)
            for vm in vms:
                obj = Virtual.objects.filter(hostname=vm["hostname"])
                vm['host'] = Physical.objects.get(ip=i.ip)
                # vm['createtime'] = timezone.now().strftime("%Y-%m-%d")
                vm['updatetime'] = timezone.now()
                if obj.count() == 0:
                    print "count is 0"
                    Virtual.objects.create(**vm)
                elif obj.count() == 1:
                    print "count is 1"
                    for item in obj:
                        print item.id
                        Virtual.objects.filter(id=item.id).update(**vm)
                elif obj.count() >= 2:
                    print "count more than 2"
                    print "%s's count has more than 2" % vm.ip

            print "---------- ending collect vmware host data ------------"
        elif i.type == '3':
            print "---------- starting collect vcenter data ------------"
            esxi = Esxi(address=i.ip, user=i.username, password=i.password)
            hosts = esxi.gethosts()
            for host in hosts:
                info = esxi.gethostinfo(host)
                obj = Physical.objects.filter(ip=info["ip"])
                info['vcenterid'] = i
                info['updatetime'] = timezone.now()
                # obj is a QuerySet, it is a generator
                if obj.count() == 0:
                    Physical.objects.create(**info)

                elif obj.count() == 1:
                    for o in obj:
                        Physical.objects.filter(id=o.id).update(**info)
                elif obj.count() >= 2:
                    print "something is error"

                # 更新Virtual表
                print(host)
                vms = esxi.getvms(host)
                # print vms
                for vm in vms:
                    print(vm["hostname"])
                    obj = Virtual.objects.filter(hostname=vm["hostname"])
                    vm['host'] = Physical.objects.get(ip=info['ip'])
                    # vm['createtime'] = timezone.now().strftime("%Y-%m-%d")
                    vm['updatetime'] = timezone.now()
                    if obj.count() == 0:
                        print "count is 0"
                        Virtual.objects.create(**vm)
                    elif obj.count() == 1:
                        print "count is 1"
                        for item in obj:
                            print item.id
                            Virtual.objects.filter(id=item.id).update(**vm)
                    elif obj.count() >= 2:
                        print "count more than 2"
                        print "%s's count has more than 2" % vm.ip
                # vdata.append(info)
            print "---------- ending collect vcenter data ------------"
    # return pdata, vdata
