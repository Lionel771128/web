from django.shortcuts import render, HttpResponseRedirect, HttpResponse, redirect
from django.urls import reverse
import json
from utils.log_in_out import process_reg, process_login, process_logout, validate_login_state
from utils.product_utils import get_one_product, get_related_products
from utils.utils import get_all_department, get_shoping_cart_info
from .models import Brand, ProductCategory, Product


# Create your views here.
def shop_grid_view(request, product_category):
    # 頁面預設為PS5商品, 除非有特別傳入某類商品
    # [頁面呈現]
    # 刪去動態移動的grid 只保留下方有filter的 grid , 透過for loop去生成
    # p.s. 點商品進入detail的部分先不做
    param = {
        'all_departments': [],
        'product_list': [],
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
    if request.method == 'GET':
        get_all_department(param)
        shoping_cart_info = get_shoping_cart_info(request)
        param['shopping_cart_item_count'] = shoping_cart_info['count']
        param['shopping_cart_item_total'] = shoping_cart_info['total']

        if product_category[-1] == 'X' or len(product_category) == 2:
            products = Product.objects.filter(brand_id=int(product_category[0]),
                                              category_id=int(product_category[1]),
                                              is_active=True)
        # 010, 011, 210, .....
        else:
            products = Product.objects.filter(brand_id=int(product_category[0]),
                                              category_id=int(product_category[1]),
                                              game_category=product_category[-1],
                                              is_active=True)
    elif request.method == 'POST':
        search_string = request.POST['search_string']
        products = Product.objects.filter(product_name__icontains=search_string)
        print(search_string)
    for p in products:
        p_dict = {
            'product_id': p.product_id,
            'brand_id': p.brand_id,
            'category_id': p.category_id,
            'game_id': p.game_category_id if p.game_category_id != 999 else 'X',
            'brand': p.brand.brand_name,
            'product_category': p.category.category_name,
            'product_name': p.product_name,
            'game_category': p.game_category,
            'sell_price': p.sell_price,
            'img_path': p.image_path,
        }

        param['product_list'].append(p_dict)
    return render(request, 'shop-grid.html', param)


def shop_details_view(request, product_category):
    if request.method == 'GET':
        param = {
            'all_departments': [],
            'product': {},
            'related_product_list': [],
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
        get_all_department(param)
        query_string_dict = request.GET
        shoping_cart_info = get_shoping_cart_info(request)
        param['shopping_cart_item_count'] = shoping_cart_info['count']
        param['shopping_cart_item_total'] = shoping_cart_info['total']
        try:
            import json
            print(query_string_dict['pc'])
            all_id = request.path.split('/')[2]
            print(all_id)
            param['product'] = get_one_product(query_string_dict['pc'])
            param['related_product_list'] = get_related_products(brand_id=all_id[0],
                                                                 category_id=all_id[1],
                                                                 game_category_id=all_id[2])
            print(request.path)

        except:
            print('no data')

    return render(request, 'shop-details.html', param)


# ec_cart : { id1: q1, id2: q2, .....}
def add_to_cart_view(request):

    full_catc = request.GET['full_catc']
    pc = request.GET["ec_cart"]

    # 透過shop detail頁面
    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        redirect_url = f'/shop/details/{full_catc}?pc={pc}'
    # 透過購物車圖形按鈕
    elif request.method == 'GET':
        quantity = 1
        redirect_url = f'/index'

    ec_cart = request.COOKIES.get('ec_cart')

    # 如果之前有將商品加入到購物車
    if ec_cart is not None:
        ec_cart_dict = json.loads(ec_cart)

        # 如果該商品已經在購物車內
        if ec_cart_dict.get(pc) is not None:
            count = int(ec_cart_dict[pc])
            ec_cart_dict[pc] = count + quantity
        else:
            ec_cart_dict[pc] = quantity
        ec_cart = json.dumps(ec_cart_dict)
    else:
        ec_cart = json.dumps({pc: quantity})

    max_age = 7 * 24 * 60 * 60
    resp = HttpResponseRedirect(redirect_url)
    resp.set_cookie(key='ec_cart', value=ec_cart, max_age=max_age)

    return resp


def shoping_cart_view(request):
    param = {
        'products': [],
        'related_product_list': [],
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
    else:
        return redirect(reverse('login_view'))

    if request.COOKIES.get('ec_cart', None) is not None:
        product_dict = json.loads(request.COOKIES['ec_cart'])
        total_price = 0
        for k, v in product_dict.items():
            p = get_one_product(k)
            p['quantity'] = v
            p['total'] = int(v) * p['sell_price']
            total_price += p['total']
            param['products'].append(p)
        param['total_price'] = total_price
        shoping_cart_info = get_shoping_cart_info(request)
        param['shopping_cart_item_count'] = shoping_cart_info['count']
        param['shopping_cart_item_total'] = shoping_cart_info['total']

    return render(request, 'shoping-cart.html', param)


def update_shoping_cart_view(request):
    if request.method == 'POST':

        ec_cart = json.loads(request.body)['ec_cart']
        ec_cart_cookie = json.loads(request.COOKIES['ec_cart'])
        print(ec_cart)
        print(ec_cart_cookie)
        for p_id in list(ec_cart_cookie.keys()):
            if ec_cart.get(p_id, None) is not None:
                ec_cart_cookie[p_id] = ec_cart[p_id]
            else:
                del ec_cart_cookie[p_id]

        max_age = 7 * 24 * 60 * 60
        # resp = HttpResponseRedirect(reverse('ec_site.views.shoping_cart_view'))
        resp = redirect(reverse('shoping_cart'))
        resp.set_cookie(key='ec_cart', value=json.dumps(ec_cart_cookie), max_age=max_age)

    return resp


def checkout_view(request):
    ec_cart = request.COOKIES['ec_cart']
    param = {
        'all_departments': [],
        'product_list': [],
        'shopping_cart_item_count': 0,
        'shopping_cart_item_total': 0,
        'user_id': None,
        'login': False
    }
    get_all_department(param)
    if validate_login_state(request):
        print(validate_login_state(request))
        print(request.session.get('user_id', None))
        param['login'] = True
        param['user_id'] = request.session.get('user_id', None)
        shoping_cart_info = get_shoping_cart_info(request)
        param['shopping_cart_item_count'] = shoping_cart_info['count']
        param['shopping_cart_item_total'] = shoping_cart_info['total']
        if ec_cart is not None:
            ec_cart = json.loads(ec_cart)
            subtotal = 0
            total = 0
            for k, v in ec_cart.items():
                p = get_one_product(k)
                p['quantity'] = v
                p['total'] = int(v) * p['sell_price']
                subtotal += p['total']
                total += p['total']
                param['product_list'].append(p)
            param['total'] = total
            param['subtotal'] = subtotal
            resp = render(request, 'checkout.html', param)
    else:
        resp = redirect(reverse('login_view'))

    return resp

