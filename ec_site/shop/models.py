from django.db import models
from user.models import UserProfile


class Brand(models.Model):
    # 0: ps5, 1: xbox, 2: nitendo
    brand_id = models.IntegerField(primary_key=True, auto_created=True)
    brand_name = models.CharField('Category Name', max_length=20, unique=True)
    image_path = models.ImageField(default='#path#')
    is_active = models.BooleanField(default=True)


# Create your models here.
class ProductCategory(models.Model):
    # 0: machine, 1: game, 2: accessories
    category_id = models.IntegerField(primary_key=True, auto_created=True)
    category_name = models.CharField('Category Name', max_length=20, unique=True)
    is_active = models.BooleanField(default=True)


class GameCategory(models.Model):
    # 0: RPG(Role-playing Game)  1: ACT(Action Game) 2: AVG(Adventure Game)
    # 3: SPG(Sports Game) 4: STG(Shooting Game)
    # 999: not a game
    category_id = models.IntegerField(primary_key=True, auto_created=True)
    category_name = models.CharField('Category Name', max_length=50, unique=True)
    # image_path = models.ImageField(default='#path#')
    is_active = models.BooleanField(default=True)


class Product(models.Model):
    product_id = models.IntegerField(primary_key=True, auto_created=True)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, default=999)
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT)
    # null: machine or equitment
    game_category = models.ForeignKey(GameCategory, on_delete=models.PROTECT, default=999)
    product_name = models.CharField(max_length=100, unique=True, null=False, default='#')
    product_detail = models.TextField()
    cost_price = models.DecimalField(max_digits=7, decimal_places=1)
    sell_price = models.DecimalField(max_digits=7, decimal_places=1)
    quantity = models.IntegerField(default=0)
    sales_volume = models.IntegerField(default=0)
    image_path = models.ImageField(default='#path#',  max_length=200)
    is_active = models.BooleanField(default=True)
    create_time = models.DateTimeField(auto_now_add=True)
    last_modify_time = models.DateTimeField(auto_now=True)


class Order(models.Model):
    order_id = models.IntegerField(primary_key=True)
    client_id = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    address = models.CharField(max_length=100, null=False, default='#')
    tel_no = models.CharField(max_length=15, null=False, default='#')
    create_time = models.DateTimeField(auto_now_add=True)
    last_modify_time = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField()
    is_active = models.BooleanField()


class OrderDetail(models.Model):
    client_id = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, default=9999)
    quantity = models.IntegerField()
    product_price = models.DecimalField(max_digits=7, decimal_places=1)


