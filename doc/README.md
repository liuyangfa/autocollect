### 运维管理系统

#### 简介

该系统主要是为了减少工作中人力的重复劳动，提升工作效率。主要两方面的功能：
1. 报表生成
2. 虚拟机流程化申请、自动分配、到时销毁

#### 技术栈

1. Code Language: Python2.7
2. Python Web Framework: Django 1.11
3. Asynchronous Framework: Celery3.1.25
4. DB: MySQL Community Server 5.7.24
5. Remote Connect: paramiko 2.4.2
6. DB Connect Driver: pymysql 0.9.2
7. ESXI Connect Driver: pyvmomi 6.5

#### 项目运行

- 数据库

```bash
assetManage]# python manage.py makemigrations
assetManage]# python manage.py migrate

```

- 工程运行

```bash
assetManage]# python manage.py runserver 0.0.0.0:8000
```

- 创建管理员用户

```shell
assetManage]# python manage.py  createsuperuser --email liuyangfa@juzix.net --username admin 
```

- 异步任务进程

```bash
assetManage]# python manage.py celery -A assetManage worker -l info

```

