import random
from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse
import http.client, urllib.request, urllib.parse, urllib.error, base64
from main.models import Store, Products, Wish, Order
import json

OcpApimSubscriptionKey = "936f1583b9384f7c83ce87e539210f3a"


def main_view(request):
    pass

def create_wish_view(request, category, needCount):

    try:
        date = str(datetime.today().strftime('%Y-%m-%d'))
        products = Products.objects.filter(tags=category)
        existCount = 0
        for p in products.caunt:
            existCount += p

        wish = Wish(category=category, date=date, needCount=needCount, existCount=existCount)
        wish.save()
        print(needCount)
        answer = "ok"
    except Exception as e:
        answer = str(e)

    return JsonResponse({'answer': answer})


# def parse_product_view(request, product_name):
#
#     headers = {
#         # Request headers
#         'Ocp-Apim-Subscription-Key': OcpApimSubscriptionKey,
#     }
#
#     query = product_name
#     offset = 0
#     limit = 10
#
#     params = urllib.parse.urlencode({
#         'query': query,
#         'offset': offset,
#         'limit': limit,
#     })
#
#     try:
#         conn = http.client.HTTPSConnection('dev.tescolabs.com')
#         conn.request("GET", "/grocery/products/?query={0}&offset=0&limit=20".format(query,), "{body}",
#                      headers)
#         response = conn.getresponse()
#         data = response.read()
#         data = data.decode()
#         data = json.loads(data)
#         for i in range(19):
#             res = data["uk"]["ghs"]["products"]["results"][i]
#
#             id_code = res["id"]
#             tags = product_name
#             name = res["name"]
#             image = res["image"]
#             date = str(datetime.today().strftime('%Y-%m-%d'))
#             count = random.randint(0,100)
#             product = Products(store=Store.objects.get(id=20), id_code=id_code, tags=tags, name=name, image=image, date=date, count=count)
#             product.save()
#             print(product)
#         conn.close()
#     except Exception as e:
#         print("error : ", e )
#
#     return JsonResponse({})



# def parse_store_view(request):
#     headers = {
#         # Request headers
#         'Ocp-Apim-Subscription-Key': OcpApimSubscriptionKey,
#     }
#
#     offset = 0
#     limit = 20
#     sort = "near:'Budapest, HU'"
#     check = True
#     res = ''
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
#
#         conn.close()
#         print(store)
#     except Exception as e:
#         print('error', e)
#
#
#     return JsonResponse({})


def store_json_view(request):

    return JsonResponse({
                        "id": "4730c2b7-c46b-426b-bf1c-64d3fa55c0a8",
                        "name": "Astoria Expressz",
                        "address": {
                            "text": "Rákóczi út 1-3.",
                            "coordinates": {
                                "latitude": 47.495165,
                                "longitude": 19.062358
                            }
                        },
                        "phone": "",
                        "products": {
                            "id": "253555203",
                            "name": "Tesco Bananas Loose",
                            "image": "http://img.tesco.com/Groceries/pi/000/0261480000000/IDShot_90x90.jpg",
                            "date": "Fri, 25 Oct 2019 21:13:39 GMT",
                            "count": "3"
                        }
    })

def product_json_view(request):

    return JsonResponse({
            "id": "253555203",
            "store": "Store",
            "name": "Tesco Bananas Loose",
            "image": "http://img.tesco.com/Groceries/pi/000/0261480000000/IDShot_90x90.jpg",
            "date": "Fri, 25 Oct 2019 21:13:39 GMT",
            "count": "3"
    })

def wish_json_view(request):
    return JsonResponse({
        "id": "",
        "category": "",
        "date": "",
        "needCount": 3,
        "existCount": 1,
    })

def order_json_view(request):
    return JsonResponse({
        "id": "",
        "content": {
            "product": "Product",
            "count": "1",
        },
        "date": "",
        "qr": "",
        "status": "true"
    })