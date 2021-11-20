from django.shortcuts import render, HttpResponseRedirect, HttpResponse, redirect
from django.urls import reverse
import os, sys
from utils.log_in_out import process_reg, process_login, process_logout, validate_login_state
from utils.product_utils import get_one_product, get_related_products
from utils.utils import get_all_department, get_shoping_cart_info
from shop.models import Brand, ProductCategory, Product
import json


def login_view(request):
    # 進入登入頁面
    if request.method == 'GET':
        resp = render(request, 'login/login.html')
    # 送出登入請求
    elif request.method == 'POST':
        resp = process_login(request)

    return resp


def logout_view(request):
    resp = process_logout(request)
    return resp

def reg_view(request):
    # 進入註冊頁面
    if request.method == 'GET':
        resp = render(request, 'login/reg.html')
    # 送出註冊請求
    elif request.method == 'POST':
        user_name = request.POST.get('user_name')
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')

        try:
            process_reg(user_name, user_id, password)
        except:
            print('DB ERROR')

        resp = redirect(reverse('home_page'))
    return resp


def index_view(request):
    # create_test_data()
    param = {
        'all_departments': [],
        'feature_product': [],
        'shopping_cart_item_count': 0,
        'shopping_cart_item_total': 0,
        'user_id': None,
        'login': False
    }

    if validate_login_state(request):
        print(validate_login_state(request))
        print(request.session.get('user_id', None))
        param['login'] = True
        param['user_id'] = request.session.get('user_id', None)
    # all departments
    get_all_department(param)
    shoping_cart_info = get_shoping_cart_info(request)
    param['shopping_cart_item_count'] = shoping_cart_info['count']
    param['shopping_cart_item_total'] = shoping_cart_info['total']
    # feature product
    # 從db抓出銷售量 > xxx 的商品， 每種brand至少2, 3個, 將image path整理好送入render
    products = Product.objects.all()
    i = 0
    for product in products:
        p = {
            'product_id': product.product_id,
            'brand_id': product.brand_id,
            'category_id': product.category_id,
            'game_id': product.game_category_id if product.game_category_id != 999 else 'X',
            'brand': product.brand.brand_name,
            'product_category': product.category.category_name,
            'product_name': product.product_name,
            'sell_price': product.sell_price,
            'img_path': product.image_path
        }
        param['feature_product'].append(p)
    return render(request, 'index.html', param)



def create_test_data():
    from create_test_data import create_cat_data, create_product_data, create_brand_data, create_game_cat_data, create_user_data
    create_brand_data()
    create_game_cat_data()
    create_cat_data()
    create_product_data()
    create_user_data()

