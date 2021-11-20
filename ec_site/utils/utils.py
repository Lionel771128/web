from shop.models import Brand, ProductCategory
from .product_utils import get_one_product
import json


def get_all_department(para_dict):
    brands = Brand.objects.all()
    product_cat = ProductCategory.objects.all()
    for b in brands:
        for p_c in product_cat:
            dep = b.brand_name + ' ' + p_c.category_name
            dep_code = str(b.brand_id) + str(p_c.category_id)
            if p_c.category_id != 1:
                dep_code += 'X'
            para_dict['all_departments'].append([dep_code, dep])


# 取得shopping cart內商品的數量, 用以顯示在頁面右上角購物籃圖示上
def get_shoping_cart_info(request):
    shoping_cart_info = {'count': 0, 'total': 0}
    ec_cart = request.COOKIES.get('ec_cart', None)
    total = 0

    if ec_cart is not None:
        ec_cart = json.loads(ec_cart)
        for k, v in ec_cart.items():
            p = get_one_product(k)
            total += float(v) * float(p['sell_price'])
        shoping_cart_info['count'] = len(ec_cart)
        shoping_cart_info['total'] = total
    return shoping_cart_info