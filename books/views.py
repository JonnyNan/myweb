# -*- coding: UTF-8 -*-
import requests
from openpyxl import Workbook
import pymysql.cursors
from django.shortcuts import render_to_response
from django.shortcuts import render

# Create your views here.

# sutdent list
from books.models import *

def table(request):
    lagous = Result.objects.all()
    return render_to_response('table.html', {'lagou_list': lagous})

def search(request):
    return render(request,'search.html')

def search_lagou(request):
    return render(request, 'search.html')

connection = pymysql.connect(host='127.0.0.1',
                             port=3306,
                             user='root',
                             password='123456',
                             db='lagou',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

def get_json(url, page, lang_name):
    data = {'first': 'true', 'pn': page, 'kd': lang_name}
    json = requests.post(url, data).json()
    list_con = json['content']['positionResult']['result']
    info_list = []
    for i in list_con:
        info = []
        info.append(i['companyShortName'])
        info.append(i['companySize'])
        info.append(i['positionName'])
        info.append(i['salary'])
        info.append(i['positionAdvantage'])
        info.append(i['workYear'])
        info.append(i['city'])
        info.append(i['education'])
        info.append(i['createTime'])
        info_list.append(info)
    return info_list

def main():
    lang_name = input('keywords:')
    page = 0
    url = 'http://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
    info_result = []
    while page < 31:
        info = get_json(url, page, lang_name)
        info_result = info_result + info
        page += 1
    wb = Workbook()
    ws1 = wb.active
    ws1.title = lang_name
    try:
        with connection.cursor() as cursor:
            # Create a new record
            for row in info_result:
                sql = "INSERT INTO `books_result` (`companyShortName`, `companySize`,`positionName`,`salary`,`positionAdvantage`,`workYear`," \
                      "`city`,`education`,`createTime`) VALUES (%s, %s, %s,%s,%s, %s, %s,%s,%s)"
                list = []
                list.append(row)
                createTime = list[0][8].split(" ")
                list[0].pop()
                list[0].append(createTime[0])
                cursor.execute(sql, (list[0][0:9]))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()

    finally:
        connection.close()


    for row in info_result:
        ws1.append(row)
    wb.save(lang_name+'.xlsx')