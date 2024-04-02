# 运维管理系统



### 简介

> 该系统主要是为了减少工作中人力的重复劳动，提升工作效率。主要两方面的功能：
- 收集虚机信息
- 生成基础报表信息
- 虚机自动化管理(虚拟机流程化申请、自动分配、到时销毁)

### 技术栈

- Code Language: Python2.7
- Python Web Framework: Django 1.11
- Asynchronous Framework: Celery3.1.25
- DB: MySQL Community Server 5.7.24
- Remote Connect: paramiko 2.4.2
- DB Connect Driver: pymysql 0.9.2
- ESXI Connect Driver: pyvmomi 6.5
- RabbitMQ

### 项目运行

#### 数据库

```bash
assetManage]# python manage.py makemigrations
assetManage]# python manage.py migrate
```

#### 工程运行

```bash
assetManage]# python manage.py runserver 0.0.0.0:8000
```

#### 创建管理员用户

```bash
assetManage]# python manage.py  createsuperuser --email xxxx@qq.com --username admin 
```

#### 异步任务进程

```bash
assetManage]# python manage.py celery -A assetManage worker -l info
```
