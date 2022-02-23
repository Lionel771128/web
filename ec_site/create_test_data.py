from shop.models import Brand , GameCategory, Product, ProductCategory, Order, OrderDetail
from user.models import UserProfile, PayInfo
import os
import random
import hashlib
import csv
# Category file name : id_cat.jpg
def create_brand_data():
    folder_path = './static/img/brand'
    img_list = os.listdir(folder_path)

    for img in sorted(img_list):
        img_name_split = os.path.splitext(img)
        if img_name_split[-1] in ['.jpg', '.jpeg', '.png']:
            img_path = os.path.join(folder_path, img)
            b_id = img_name_split[0].split('_')[0]
            b_name = img_name_split[0].split('_')[1]
            Brand.objects.create(brand_id=b_id, brand_name=b_name, image_path=img_path)


def create_cat_data():
    idx = 0
    for cat in ['machine', 'game', 'accessories']:
        ProductCategory.objects.create(category_id=idx, category_name=cat)
        idx += 1


def create_user_data():
    s = hashlib.sha1()
    s.update('ppp'.encode("utf-8"))
    pw_sha = s.hexdigest()
    UserProfile.objects.create(user_id='aaa', user_name='bbb', password=pw_sha)


def create_game_cat_data():
    idx = 0
    for cat in ['RPG(Role-playing Game)', 'ACT(Action Game)', 'AVG(Adventure Game)',
                'SPG(Sports Game)', 'STG(Shooting Game)', 'not a game']:
        if cat != 'not a game':
            GameCategory.objects.create(category_id=idx, category_name=cat)
            idx += 1
        else:
            GameCategory.objects.create(category_id=999, category_name=cat)


# prodcut file name : brand_cat_pname_gcat.jpg
def create_product_data():
    folder_path = './static/img/product/'
    relative_path = 'img/product'
    img_list = os.listdir(folder_path)
    # with open('/web/product.csv', newline='') as csvfile:
    with open('/Users/lionl771128/Documents/Django_test/web/ec_site/product_local.csv', newline='') as csvfile:
        rows = csv.reader(csvfile)

        for r in rows:
            # print(r)
            # try:
            Product.objects.create(brand_id=r[1],
                                   category_id=r[2],
                                   game_category_id=r[3],
                                   product_id=r[0],
                                   product_name=r[4],
                                   product_detail=r[5],
                                   cost_price=r[6],
                                   sell_price=r[7],
                                   quantity=r[8],
                                   sales_volume=r[9],
                                   image_path=r[10])

            # except:
            #     print('=====', r[4], '====')


    # for img in sorted(img_list):
    #     img_name_split = os.path.splitext(img)
    #     if img_name_split[-1] in ['.jpg', '.jpeg', '.png']:
    #         img_path = os.path.join(relative_path, img)
    #         img_name_info = img_name_split[0].split('_')
    #         b_id = img_name_info[0]
    #         c_id = img_name_info[1]
    #         p_name = img_name_info[2]
    #         game_cat = img_name_info[-1]
    #         sales_volume = random.uniform(0, 2000)
    #         # brand_instance = Brand.objects.filter(brand_id=b_id)
    #         # cat_instance = ProductCategory.objects.filter(category_id=c_id)
    #         # game_cat_instance = GameCategory.objects.filter(category_id=game_cat)
    #
    #         Product.objects.create(brand_id=b_id,
    #                                category_id=c_id,
    #                                game_category_id=game_cat,
    #                                product_id=img_list.index(img),
    #                                product_name=p_name,
    #                                product_detail=f'###########{p_name}###########',
    #                                cost_price=100,
    #                                sell_price=random.randint(30, 180),
    #                                quantity=1000,
    #                                sales_volume=sales_volume,
    #                                image_path=img_path)




