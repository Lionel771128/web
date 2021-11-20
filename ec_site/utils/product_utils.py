from shop.models import Product
def get_one_product(product_id):
    product = Product.objects.filter(product_id=product_id).values()[0]
    p_info = {}

    for k, v in product.items():
        p_info[k] = v
    return p_info


def get_related_products(brand_id, category_id, game_category_id, count=4):
    related_product_list = []
    if category_id == '0':
        related_products = Product.objects.filter(brand_id=brand_id, category_id=2)
    elif category_id == '1':
        related_products = Product.objects.filter(brand_id=brand_id, category_id=1,
                                                  game_category_id=game_category_id)
    else:
        related_products = Product.objects.filter(brand_id=brand_id, category_id=0)

    idx = 0
    while idx < count and idx < len(related_products):
        print(idx)
        r_p = related_products[idx]
        print(r_p)
    # for r_p in related_products:
        r_p_dict = {
            'brand_id': r_p.brand_id,
            'category_id': r_p.category_id,
            'game_id': r_p.game_category_id if r_p.game_category_id != 999 else 'X',
            'brand': r_p.brand.brand_name,
            'product_category': r_p.category.category_name,
            'product_name': r_p.product_name,
            'game_category': r_p.game_category,
            'sell_price': r_p.sell_price,
            'img_path': r_p.image_path,
        }

        related_product_list.append(r_p_dict)
        idx += 1

    return related_product_list