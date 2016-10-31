# -*- coding: UTF-8 -*-
import requests
from openpyxl import Workbook
import pymysql.cursors
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.

from books.models import *


def index(request):
    return render(request, 'index.html')


def loginpage(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signUp.html')


def realSignup(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    passwordAgain = request.POST.get('passwordAgain')
    if (username == ""):
        return HttpResponse(u"账号不能为空!")
    else:
        if (password == ""):
            return HttpResponse(u"密码不能为空!")
        else:
            if (password != passwordAgain):
                return HttpResponse(u'两次输入的密码不一致！')
            else:
                try:
                    connection = pymysql.connect(host='127.0.0.1',
                                                 port=3306,
                                                 user='root',
                                                 password='123456',
                                                 db='lagou',
                                                 charset='utf8',
                                                 cursorclass=pymysql.cursors.DictCursor)
                    cursor = connection.cursor()
                    create_sql = "INSERT INTO `books_user` (`userName`, `passWord`) VALUES (%s, %s)"
                    search_user_sql = "SELECT userName, passWord FROM lagou.books_user WHERE userName = '%s'" % (username)
                    if (cursor.execute(search_user_sql) == 0):
                        user = (username, password)
                        cursor.execute(create_sql, user)
                        connection.commit()
                        return render(request, 'login.html')
                    else:
                        return HttpResponse(u'用户名已存在！')
                finally:
                    connection.close()


def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    if (username == ""):
        return HttpResponse(u"账号不能为空!")
    else:
        if (password == ""):
            return HttpResponse(u"密码不能为空!")
        else:
            connection = pymysql.connect(host='127.0.0.1',
                                         port=3306,
                                         user='root',
                                         password='123456',
                                         db='lagou',
                                         charset='utf8',
                                         cursorclass=pymysql.cursors.DictCursor)
            cursor = connection.cursor()
            lookup_sql = "SELECT userName, passWord FROM lagou.books_user WHERE userName = '%s' AND passWord = '%s';" % (
            username, password)
            if(cursor.execute(lookup_sql) >= 1):
                return render(request, 'search.html')
            else:
                return HttpResponse(u"账号或者密码不正确!")


def table(request):
    lagous = Result.objects.all()
    return render_to_response('table.html', {'lagou_list': lagous})


def search(request):
    return render(request, 'search.html')


def search_lagou(request):
    search_content = request.POST.get('searchbox', '')
    keep_data(search_content)
    response = HttpResponseRedirect('/table/')
    return response


def get_json(url, page, lang_name):
    data = {'first': 'true', 'pn': page, 'kd': lang_name}
    json = requests.post(url, data).json()
    list_con = json['content']['positionResult']['result']
    info_list = []
    for i in list_con:
        info = [i['companyShortName'], i['companySize'], i['positionName'], i['salary'], i['positionAdvantage'],
                i['workYear'], i['city'], i['education'], i['createTime']]
        info_list.append(info)
    return info_list


def keep_data(name):
    connection = pymysql.connect(host='127.0.0.1',
                                 port=3306,
                                 user='root',
                                 password='123456',
                                 db='lagou',
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    lang_name = name
    page = 0
    url = 'http://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
    info_result = []
    while page < 31:
        info = get_json(url, page, lang_name)
        info_result = info_result + info
        page += 1
    # wb = Workbook()
    # ws1 = wb.active
    # ws1.title = lang_name
    delete_sql = "TRUNCATE TABLE `books_result`;"
    cursor.execute(delete_sql)
    try:
        with connection.cursor() as cursor:
            # Create a new record
            for row in info_result:
                sql = "INSERT INTO `books_result` (`companyShortName`, `companySize`,`positionName`,`salary`," \
                      " `positionAdvantage`,`workYear`," \
                      "`city`,`education`,`createTime`) VALUES (%s, %s, %s,%s,%s, %s, %s,%s,%s)"
                job_list = [row]
                create_time = job_list[0][8].split(" ")
                job_list[0].pop()
                job_list[0].append(create_time[0])
                cursor.execute(sql, (job_list[0][0:9]))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()

    finally:
        connection.close()

        # for row in info_result:
        #     ws1.append(row)
        # wb.save(lang_name + '.xlsx')
