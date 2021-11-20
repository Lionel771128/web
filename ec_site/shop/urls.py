from django.urls import path, re_path
from . import views


urlpatterns = [
    re_path(r'^grid/(?P<product_category>\w+)', views.shop_grid_view),
    re_path(r'^details/(?P<product_category>\w+)', views.shop_details_view),
    path('add-to-cart', views.add_to_cart_view),
    path('cart/', views.shoping_cart_view, name='shoping_cart'),
    path('update_shoping-cart/', views.update_shoping_cart_view),
    path("checkout/", views.checkout_view),
]