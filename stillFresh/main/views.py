import random
import threading
import time
from django.http import JsonResponse
import http.client, urllib.request, urllib.parse, urllib.error
from main.models import Store, Products, Wish, Order, Order_p
import json
import hashlib
import email.utils
from fcm_django.models import FCMDevice

OcpApimSubscriptionKey = "936f1583b9384f7c83ce87e539210f3a"

# for p in Order.objects.all():
#     p.qr = hashlib.md5((email.utils.formatdate(usegmt=True)+ str(p.id)).encode('utf-8'))
#     p.save()


def check_products_for_wish():
    wishes = Wish.objects.all()
    for wish in wishes:
        products = Products.objects.all()
        need = wish.needCount
        order = Order(count=need, date=email.utils.formatdate(usegmt=True), qr="")
        order.save()
        for product in products:
            if wish.category in product.tags and need!=0:
                if need <= product.count:
                    order_product = Order_p(order=order, product_id=product.id_code, qty=need)
                    order_product.save()
                    need = 0
                else:
                    need-=product.count
                    order_product = Order_p(order=order, product_id=product.id_code, qty=product.count)
                    order_product.save()
            if need == 0:
                device = FCMDevice.objects.all()[2]
                order.save()

                orders_p = Order_p.objects.filter(order=order)
                i = 1
                answer = ""
                for order_p in orders_p:
                    answer += "{0}. {1} | qty : {2}\n".format(i, Products.objects.filter(id_code=order_p.product_id), order_p.qty)
                device.send_message(title="Your order is ready!",
                                    body=answer,
                                    )
                wish.delete()
            else:
                for o in Order_p.objects.filter(order=order):
                    o.delete()
                order.save()
                order.delete()

def timeCheck ():
    while True:
        check_products_for_wish()
        time.sleep(10)

tChThr = threading.Thread(target=timeCheck, name='tchThr')
tChThr.start()


def main_view(request):
    # products = Products.objects.all()
    # for product in products:
    #     product.date = datetime.strptime("10/29/19", "%m/%d/%y")
    #     product.save()
    return JsonResponse({})

def create_wish_view(request, category, needCount):

    date = email.utils.formatdate(usegmt=True)
    products = Products.objects.filter(tags=category)
    existCount = random.randint(0, int(needCount))
    for p in products:
        existCount += p.count

    wish = Wish(category=category, date=date, needCount=needCount, existCount=existCount)
    wish.save()
    answer = "ok"


    return JsonResponse({'answer': answer})


def wish_delete_view(request, id):
    try:
        wish=Wish.objects.get(id=id)
        wish.delete()
        answer ="deleted"
    except  Exception as e:
        answer = str(e)

    return JsonResponse({'answer': answer})

def confirm_view(request, id):
    ord = Order.objects.get(id=id)
    ord.status = "CONFIRMED"
    ord.qr = hashlib.md5((email.utils.formatdate(usegmt=True)+ str(ord.id)).encode('utf-8'))
    ord.save()
    return JsonResponse({})

def create_order_view(request, product, count):

    try:
        date = email.utils.formatdate(usegmt=True)
        order = Order(product=product, count=count, date=date, qr="")
        order.qr = hashlib.md5((email.utils.formatdate(usegmt=True)+ str(order.id)).encode('utf-8'))
        order.save()
        answer = "ok"
    except Exception as e:
        answer = str(e)

    return JsonResponse({'answer': answer})

def parse_product_view(request, product_name):

    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': OcpApimSubscriptionKey,
    }

    query = product_name
    offset = 0
    limit = 30

    params = urllib.parse.urlencode({
        'query': query,
        'offset': offset,
        'limit': limit,
    })

    conn = http.client.HTTPSConnection('dev.tescolabs.com')
    conn.request("GET", "/grocery/products/?query={0}&offset=20&limit={1}".format(query,limit), "{body}",
                 headers)
    response = conn.getresponse()
    data = response.read()
    data = data.decode()
    data = json.loads(data)
    products = Products.objects.all()
    for i in range(limit):
        res = data["uk"]["ghs"]["products"]["results"][i]
        price = 0
        discount = 0.1
        discount_price = price * discount
        id_code = res["id"]
        tags = product_name
        name = res["name"]
        image = res["image"]
        date = email.utils.formatdate(usegmt=True)
        count = random.randint(0,10)

        # тест
        for prod in products:
            if tags in prod.tags:
                tags = prod.tags
        #

        product = Products(store=Store.objects.get(id=random.randint(10,20)),
                           id_code=id_code,
                           tags=tags,
                           name=name,
                           image=image,
                           date=date,
                           count=count,
                           price=price,
                           discount=discount,
                           discount_price=discount_price)
        # product.save()

    conn.close()
    return JsonResponse({})


def parse_store_view(request):
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': OcpApimSubscriptionKey,
    }

    offset = 0
    limit = 20
    sort = "near:'Budapest, HU'"
    check = True
    res = ''

    params = urllib.parse.urlencode({
        # Request parameters
        'offset': offset,
        'limit': limit,
        'sort': sort,
    })

    try:
        conn = http.client.HTTPSConnection('dev.tescolabs.com')
        conn.request("GET", "/locations/search?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        data = data.decode()
        data = json.loads(data)
        for i in range(limit):
            res = data["results"][i]["location"]
            id_code = res["id"]
            name = res["name"]
            name = name.replace("TESCO", "")
            address = res["contact"]["address"]["town"] + res["contact"]["address"]["lines"][0]["text"]
            latitude = res["geo"]["coordinates"]["latitude"]
            longitude = res["geo"]["coordinates"]["longitude"]
            phone = res["contact"]["phoneNumbers"][0]["number"]

            store = Store(id_code=id_code, name=name, address=address, latitude=latitude, longitude=longitude, phone=phone)
            store.save()

        conn.close()

    except Exception as e:
        print('error', e)


    return JsonResponse({})

def store_json_tag_view(request,tag):
    try:
        stores = Store.objects.all()
        answer = []
        for store in stores:
            dct = {
                "id": store.id_code,
                "name": store.name,
                "address": {
                    "text": store.address,
                    "coordinates": {
                        "latitude": store.latitude,
                        "longitude": store.longitude
                    }
                },
                "phone": store.phone
            }
            products = Products.objects.filter(store=store)
            product_list = []
            for product in products:
                if tag.lower() in product.tags.lower():
                    product_list.append(
                        {
                            "id": product.id_code,
                            "name": product.name,
                            "image": product.image,
                            "date": product.date,
                            "count": product.count,
                        }
                    )

            dct.update({'products': product_list })
            answer.append(dct)
    except Exception as e:
        print(e)

    return JsonResponse(answer,safe=False)

def store_json_view(request):
    try:
        stores = Store.objects.all()
        answer = []
        for store in stores:
            dct = {
                "id": store.id_code,
                "name": store.name,
                "address": {
                    "text": store.address,
                    "coordinates": {
                        "latitude": store.latitude,
                        "longitude": store.longitude
                    }
                },
                "phone": store.phone
            }
            products = Products.objects.filter(store=store)
            product_list = []

            for product in products:
                product_list.append(
                    {
                        "id": product.id_code,
                        "name": product.name,
                        "image": product.image,
                        "date": product.date,
                        "count": product.count,
                    }
                )

            dct.update({'products': product_list })
            answer.append(dct)
    except Exception as e:
        print(e)

    return JsonResponse(answer,safe=False)

def product_json_view(request):

    products = Products.objects.all()
    answer = []
    for product in products:
        answer.append(
            {
                "id": product.id_code,
                "store": product.store.id,
                "name": product.name,
                "image": product.image,
                "date": product.date,
                "count": product.count,
                "price": product.price,
                "discount": product.discount,
                "discount_price": product.discount_price
            }
        )
    return JsonResponse(answer, safe=False)



def wish_json_view(request):

    wishes = Wish.objects.all()

    answer = []

    for wish in wishes:
        dct = {
            "id": wish.id,
            "category": wish.category,
            "date": wish.date,
            "needCount": wish.needCount,
            "existCount": wish.existCount,
        }
        answer.append(dct)

    return JsonResponse(answer, safe=False)

def order_json_view(request):
    orders = Order.objects.all()
    answer = []
    for order in orders:
        orders_p = Order_p.objects.filter(order=order)
        product_list = []

        for order_p in orders_p:
            try:
                product = Products.objects.get(id_code=order_p.product_id)
                product_list.append({
                    "product":{
                        "id": product.id_code,
                        "name": product.name,
                        "image": product.image,
                        "date": product.date,
                        "count": order_p.qty
                    },
                    "count": order.count,
                    "store": product.store.name
                })
            except:
                pass

        dct = {
            "id": order.id,
            "content": product_list,
            "date": order.date,
            "qr": order.qr,
            "status": order.status
        }
        answer.append(dct)
    return JsonResponse(answer, safe=False)

def order_delete_view(request, id):
    order = Order.objects.get(id=id)
    order_p = Order_p.objects.filter(order=order)
    for op in order_p:
        op.delete()
    order.delete()
    return JsonResponse({"answer" : "deleted"})

def search_product_view(request, tag):

    products = Products.objects.all()
    pun = []
    for product in products:
        if tag.lower() in product.tags.lower():
            pun.append(product)
    answer = []
    for product in pun:
        answer.append({
            "id": product.id_code,
            "store": product.store.id,
            "name": product.name,
            "image": product.image,
            "date": product.date,
            "count": product.count,
            "price": product.price,
            "discount": product.discount,
            "discount_price": product.discount_price
        })

    return JsonResponse(answer, safe=False)

# def give_product_to_show_view(request, query):
#     headers = {
#         # Request headers
#         'Ocp-Apim-Subscription-Key': OcpApimSubscriptionKey,
#     }
#
#     offset = 0
#     limit = 20
#     sort = "near:'Budapest, HU'"
#
#     params = urllib.parse.urlencode({
#         # Request parameters
#         'offset': offset,
#         'limit': limit,
#         'sort': sort,
#     })
#
#     try:
#         conn = http.client.HTTPSConnection('dev.tescolabs.com')
#         conn.request("GET", "/locations/search?%s" % params, "{body}", headers)
#         response = conn.getresponse()
#         data = response.read()
#         data = data.decode()
#         data = json.loads(data)
#         for i in range(limit):
#             res = data["results"][i]["location"]
#             print(res)
#             id_code = res["id"]
#             name = res["name"]
#             name = name.replace("TESCO", "")
#             address = res["contact"]["address"]["town"] + res["contact"]["address"]["lines"][0]["text"]
#             latitude = res["geo"]["coordinates"]["latitude"]
#             longitude = res["geo"]["coordinates"]["longitude"]
#             phone = res["contact"]["phoneNumbers"][0]["number"]
#
#             store = Store(id_code=id_code, name=name, address=address, latitude=latitude, longitude=longitude, phone=phone)
#             print(store)
#             store.save()
#         conn.close()
#     except Exception as e:
#         print('error', e)
#
#     return JsonResponse(data)
