# -*- coding: utf-8 -*-
from __future__ import absolute_import

import sys

import paramiko

reload(sys)
sys.setdefaultencoding('utf-8')


def collect(ip, user, passwd):
    '''
    收集物理服务器的信息
    :param ip:
    :param user:
    :param passwd:
    :return: 收集到的信息的字典
    '''
    # 需要安装ipmitool/dmidecode软件包
    cmds = {
        "cpunum": """dmidecode -t processor| grep Socket | grep -Eo 'CPU.*[0-9]'| wc -l | tr -d '\n'""",
        # "cpuphysicalcores": """dmidecode -t processor | grep "Core Count" | awk 'BEGIN{count=0}{if(count==0){count+=$NF};if(count==$NF){count==$NF}else{print "ERROR"}} END{print count}' | tr -d '\n'""",
        "cpuphysicalcores": """dmidecode -t processor | grep "Core Count" | awk 'BEGIN{count=0}{if(NR==1){count=$NF}else{count=$NF+count}} END{print count}' | tr -d '\n'""",
        "cpulogicalcores": """awk 'BEGIN{temp=$NF} /^processor/{if(NR==1){temp=$NF};if(NR!=1 && $NF>temp){temp=$NF}} END{print temp+1}' /proc/cpuinfo | tr -d '\n'""",
        "cpuother": """dmidecode -t processor | grep Version | sed 's/.*Version: //' | uniq | tr -d '\n'""",
        "memsize": """dmidecode -t memory | grep "Memory Device" -A 21 | awk 'BEGIN{sum=0}/Size: [0-9]+/{sum+=$2} END{print sum/1024"GB"}' | tr -d '\n'""",
        "idracip": "ipmitool lan print | awk '/^IP Address *:/{print $4}' | tr -d '\n'",
        "uuid": "dmidecode -t system | awk '/UUID/{print $NF}' | tr -d '\n'",
        "os": "uname -r | awk -F- '{print $1}' | tr -d '\n'",
        "hostname": "hostname | tr -d '\n'",
        "disksize": """/opt/MegaRAID/perccli/perccli64 /c0 show | awk 'BEGIN{string=""} /^32:/{if($6=="GB"){string=string+""+$5+""$6}}END{print string}' | tr -d '\n'""",
    }

    info = {}
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, 22, user, passwd)
    for key, value in cmds.items():
        if key == 'os':
            stdin, stdout, stderror = client.exec_command(value)
            result = stdout.read().split('.')
            print result
            if result[0] == '3' and result[1] == '13':
                info[key] = "Ubuntu 14.04 LTS"
            elif result[0] == '3' and result[1] == '16':
                info[key] = "Ubuntu 14.10"
            elif result[0] == '4' and result[1] == '4':
                info[key] = "Ubuntu 16.04 LTS"
            elif result[0] == '4' and result[1] == '8':
                info[key] = "Ubuntu 16.10"
            elif result[0] == '4' and result[1] == '15':
                info[key] = "Ubuntu 18.04 LTS"
            elif result[0] == '4' and result[1] == '17':
                info[key] = "Ubuntu 18.10"
            elif result[0] == '3' and result[1] == '10':
                info[key] = "CentOS 7.x"
            elif result[0] == '2' and result[1] == '6':
                info[key] = "CentOS 6.x"
            elif result[0] <= '2' and result[1] < '6':
                info[key] = "CentOS 5.x或更低版本"
        else:
            stdin, stdout, stderror = client.exec_command(value)
            result = stdout.read()
            info[key] = result.strip()

    client.close()
    return info


if __name__ == "__main__":
    print collect('120.78.184.217', 'root', 'ipanel123')
    print collect('94.191.79.133', 'root', 'ipanel123')
