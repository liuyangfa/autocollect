# -*- coding: utf-8 -*-
from __future__ import print_function

import atexit
import math
import sys

from pyVim.connect import SmartConnectNoSSL, Disconnect

reload(sys)
sys.setdefaultencoding('utf-8')


class Esxi(object):

    def __init__(self, address, user, password):
        self.__address = address
        self.__user = user
        self.__pawword = password

    def __connect(self):
        try:
            si = SmartConnectNoSSL(host=self.__address, user=self.__user, pwd=self.__pawword)
            content = si.RetrieveContent()
        except Exception, e:
            return (1, '', e.message)
        else:
            atexit.register(Disconnect, si)
        return (0, content, '')

    def gethosts(self):
        code, result, message = self.__connect()
        if code:
            return code, message
        rootchild = []
        if hasattr(result, 'rootFolder'):
            for child in result.rootFolder.childEntity:
                rootchild.append(child)

        hostchild = []
        for child in rootchild:
            if hasattr(child, "hostFolder"):
                for i in child.hostFolder.childEntity:
                    hostchild.append(i)

        hosts = []

        for child in hostchild:
            if hasattr(child, "host"):
                for i in child.host:
                    hosts.append(i)
        return hosts

    def gethostinfo(self, host):
        hostinfo = {}
        hostinfo["ip"] = host.name
        hostinfo["hostname"] = host.name

        cpu_desc = []
        for j in host.hardware.cpuPkg:
            cpu_desc.append(j.description)
        hostinfo["cpunum"] = len(cpu_desc)
        hostinfo["cpuother"] = "".join(set(cpu_desc))
        hostinfo["cpuphysicalcores"] = host.hardware.cpuInfo.numCpuCores
        hostinfo["cpulogicalcores"] = host.hardware.cpuInfo.numCpuThreads
        hostinfo["memsize"] = str(math.ceil(host.hardware.memorySize / 1024.0 / 1024 / 1024)) + "GB"
        hostinfo["os"] = host.config.product.fullName
        disksize = []
        for n in host.datastore:
            disksize.append(str(round(n.summary.capacity / 1024.0 / 1024 / 1024, 2)) + "GB")
        hostinfo["disksize"] = ",".join(disksize)
        hostinfo["type"] = "2"
        hostinfo["uuid"] = host.hardware.systemInfo.uuid
        hostinfo["status"] = "1"
        hostinfo["position"] = "1"
        return hostinfo

    def getvms(self, host):
        vms = []
        for vm in host.vm:
            vm_info = {}

            # vm's status
            # vm_info["state"] = vm.guest.guestState

            # vm's hostname
            vm_info["hostname"] = vm.name
            vm_info["ip"] = vm.name

            # vm's os name
            vm_info["os"] = vm.summary.config.guestFullName

            # vm's ips
            ip_info = []
            for ips in vm.guest.net:
                if len(ips.ipAddress) > 0 and ("." in ips.ipAddress[0]):
                    ip_info.append(ips.ipAddress[0])

            if len(ip_info):
                vm_info["ip"] = ip_info
            else:
                vm_info["ip"] = vm.guest.ipAddress

            # disk size
            print(vm)
            if vm.summary.storage != None:
                # vm_disk_info = round(vm.summary.storage.committed / 8.0 / 1024 / 1024, 2)
                vm_disk_info = round(
                    (vm.summary.storage.uncommitted + vm.summary.storage.unshared) / 1024.0 / 1024 / 1024,
                    2)
                vm_info["disksize"] = vm_disk_info

            # memory size
            vm_info["memsize"] = vm.summary.config.memorySizeMB

            # numcpu
            vm_info["cpunum"] = vm.summary.config.numCpu

            # uuid
            # if vm.config.uuid != None:
            vm_info["uuid"] = vm.summary.config.uuid

            vms.append(vm_info)
        return vms

    def getvmsinfo(self, host):
        vms = []
        for vm in host.vm:
            vm_info = {}

            # vm's status
            # vm_info["state"] = vm.guest.guestState

            # vm's hostname
            vm_info["hostname"] = vm.name
            vm_info["ip"] = vm.name

            # vm's os name
            vm_info["os"] = vm.summary.config.guestFullName

            # vm's status
            vm_info["vmtools"] = vm.guest.guestState
            vm_info["status"] = vm.summary.runtime.powerState

            # vm's ips
            ip_info = []
            for ips in vm.guest.net:
                if len(ips.ipAddress) > 0 and ("." in ips.ipAddress[0]):
                    ip_info.append(ips.ipAddress[0])

            if len(ip_info):
                vm_info["ip"] = ip_info
            else:
                vm_info["ip"] = vm.guest.ipAddress

            # disk size
            # vm_disk_info = round(vm.summary.storage.committed / 8.0 / 1024 / 1024, 2)
            vm_disk_info = round((vm.summary.storage.uncommitted + vm.summary.storage.unshared) / 1024.0 / 1024 / 1024,
                                 2)
            vm_info["disksize"] = vm_disk_info

            # memory size
            vm_info["memsize"] = vm.summary.config.memorySizeMB

            # numcpu
            vm_info["cpunum"] = vm.summary.config.numCpu

            # uuid
            vm_info["uuid"] = vm.config.uuid
            vms.append(vm_info)
        return vms

    def search_host(self, ip):
        try:
            si = SmartConnectNoSSL(host=self.__address, user=self.__user, pwd=self.__pawword)
            content = si.content.searchIndex
            # content = si.content.searchIndex()
        except Exception, e:
            return (1, '', e.message)
        else:
            atexit.register(Disconnect, si)
            # datastore = si.content.rootFolder.childEntity
            # for ds in datastore:
            # for item in ds.hostFolder.childEntity:
        # hosts = content.FindAllByIp(ip=ip, vmSearch=False)
        hosts = content.FindByIp(ip=ip, vmSearch=False)
        # print(hosts)
        return (1, hosts, '')

    def get_vms_by_ip(self, ip):
        code, hosts, message = self.search_host(ip)
        # if len(hosts) == 1:
        # for host in hosts:
        _vms = self.getvms(hosts)
        return _vms
    # else:
    #     print("something error!")
    #     return


if __name__ == '__main__':
    esxi = Esxi(address='192.168.111.115', user='administrator@vsphere.xx', password='test1123123!')
    # print(esxi.get_vms_by_ip('192.168.9.8'))
    # hosts = esxi.gethosts()
    # for host in hosts:
    #     print("*" * 100)
    #     print(esxi.gethostinfo(host))
    #     print("-"*100)
    #     print(json.dumps(esxi.getvmsinfo(host)))
    # esxi.search_host("192.168.112.9")
    vms = esxi.get_vms_by_ip("192.168.9.8")
