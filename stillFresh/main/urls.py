from django.urls import path
from django.contrib.auth.views import LogoutView

from main.views import main_view,\
    store_json_view,\
    product_json_view,\
    wish_json_view,\
    order_json_view,\
    create_wish_view

urlpatterns= [
    path('', main_view, name='main_view'),
    path('store', store_json_view, name='store_json_view'),
    path('product', product_json_view, name='product_json_view'),
    path('wish', wish_json_view, name='wish_json_view'),
    path('order', order_json_view, name='with_order_view'),
    path('add_wish/<category>/<needCount>/', create_wish_view, name='create_wish_view')
]