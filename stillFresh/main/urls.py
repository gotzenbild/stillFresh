from django.urls import path
from django.contrib.auth.views import LogoutView


from main.views import parse_product_view,\
    store_json_view,\
    product_json_view,\
    wish_json_view,\
    order_json_view,\
    create_wish_view,\
    create_order_view,\
    search_product_view,\
    main_view,\
    store_json_tag_view,\
    wish_delete_view,\
    order_delete_view,\
    confirm_view

urlpatterns = [
    path('', main_view, name='main_view'),
    path('parse/<product_name>/', parse_product_view, name='parse_product_view'),
    path('store/<tag>/', store_json_tag_view, name='store_json_tag_view'),
    path('store', store_json_view, name='store_json_view'),
    path('product', product_json_view, name='product_json_view'),
    path('wish', wish_json_view, name='wish_json_view'),
    path('order', order_json_view, name='with_order_view'),
    path('add_wish/<category>/<needCount>/', create_wish_view, name='create_wish_view'),
    path('add_order/<product>/<count>/',create_order_view, name='create_order_view'),
    path('search_product/<tag>/', search_product_view, name='search_product_view'),
    path('wish_delete/<id>/', wish_delete_view, name='wish_delete_view'),
    path('order_delete/<id>/', order_delete_view, name='order_delete_view'),
    path('confirm/<id>/', confirm_view, name='confirm_view')
]