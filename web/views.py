from django.shortcuts import render, HttpResponse, redirect
from web import models
import json
from backend import sqltools
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from backend.security import login_required
import sys
# Create your views here.


@csrf_exempt
def my_login(request):
    """

    :param request:
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            result = {'status': 1, 'message': "登录成功"}
        else:
            result = {'status': 0, 'message': "用户名或密码错误"}
        return HttpResponse(json.dumps(result))
    else:
        if request.user.is_authenticated:
            return redirect("/")
        else:
            return render(request, "login.html")


def my_logout(request):
    """

    :param request:
    :return:
    """
    logout(request)
    return redirect("/login/")


@login_required
def index(request):
    """

    :param request:
    :return:
    """
    result = {}
    if request.method == 'GET':
        return render(request, "index.html")
    elif request.method == 'POST':
        prod = request.POST.get('product', '')
        env = request.POST.get('env', '')
        sql = request.POST.get('sql', '')
        database = request.POST.get('database', '')
        table = sql.split()[3]
        if "." in table:
            result['message'] = "不允许使用'库名'.'表名'形式查询"
            result['code'] = '300000'
            return HttpResponse(json.dumps(result))
        if "limit" not in sql:
            result['message'] = "请添加limit限制返回条数"
            result['code'] = '300001'
            return HttpResponse(json.dumps(result))
        if prod == '' or env == '' or sql == '' or database == '':
            result['message'] = "The param prod or env or sql or database can not null"
            result['code'] = "300002"
            return HttpResponse(json.dumps(result))
        dbobj_list = models.SecretDB.objects.filter(name=database)
        if len(dbobj_list) > 0:
            result['message'] = "The database can not to select"
            result['code'] = "300004"
            return HttpResponse(json.dumps(result))
        if database == "exchange":
            sql_list = sql.split()
            if sql_list[3] == "pks":
                result['message'] = "The table can not to select"
                result['code'] = "300005"
                return HttpResponse(json.dumps(result))
        try:
            userobj = models.UserProfile.objects.get(product__name=prod, env=env)
            result = sqltools.select(userobj.mysql_host, userobj.mysql_port, userobj.mysql_user, userobj.mysql_pwd, sql, database)
            return HttpResponse(json.dumps(result))
        except Exception as e:
            print(e)
            result['message'] = str(e)
            result['code'] = "300006"
            return HttpResponse(json.dumps(result))


@csrf_exempt
def select_env(request):
    """

    :param request:
    :return:
    """
    result = {}
    if request.method != "POST":
        result['message'] = "The method is not support"
        return HttpResponse(json.dumps(result))
    else:
        prod = request.POST.get('product', '')
        try:
            user_list = models.UserProfile.objects.filter(product__name=prod)
            result = [user.env for user in user_list]
            return HttpResponse(json.dumps(result))
        except Exception as e:
            print(e)
            result['message'] = "The product and env is not exists"
            result['code'] = "300003"
            return HttpResponse(json.dumps(result))


@csrf_exempt
def select_product(request):
    """

    :param request:
    :return:
    """
    result = {}
    if request.method != "POST":
        result['message'] = "The method is not support"
        return HttpResponse(json.dumps(result))
    else:
        try:
            product_list = models.Product.objects.all()
            result = [product.name for product in product_list]
            return HttpResponse(json.dumps(result))
        except Exception as e:
            print(e)
            result['message'] = "The product is empty!"
            result['code'] = "300003"
            return HttpResponse(json.dumps(result))


@csrf_exempt
def select_database(request):
    """

    :param request:
    :return:
    """
    result = {}
    if request.method != "POST":
        result['message'] = "The method is not support"
        return HttpResponse(json.dumps(result))
    else:
        prod = request.POST.get('product', '')
        env = request.POST.get('env', '')
        try:
            userobj = models.UserProfile.objects.get(product__name=prod, env=env)
            result = sqltools.select_database(userobj.mysql_host, userobj.mysql_port, userobj.mysql_user, userobj.mysql_pwd)
            return HttpResponse(json.dumps(result))
        except Exception as e:
            print(e)
            result['message'] = "The product and env is not exists"
            result['code'] = "300003"
            return HttpResponse(json.dumps(result))


def page_error(request):
    error = sys.exc_info()
    context = {
        'error': error
    }
    return render(request, '500.html', context=context)
