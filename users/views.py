import json
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from django.conf import settings
import jwt
import datetime
import pymongo

from users import utils


@api_view(['POST'])
def login(request, **kwargs):
    req_user = json.loads(request.body)

    # Check email & password against DB
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    # mydb = myclient["mydb"]
    # userColl = mydb['user']
    # userObj = userColl.find({'email':req_user['email']})
    # if userObj['password']==req_user['password']:
    if req_user['email'] != 'test@test.com' or req_user['password'] != 'test':
        return HttpResponse('Unauthorized', status=401)

    # create a token
    token = jwt.encode(
        {'email': req_user['email'],
         'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=24 * 60 * 60)
         },
        settings.SECRET_KEY,
        algorithm="HS256").decode('utf-8')

    return JsonResponse({'status': True, 'token': token})


@utils.requireLogin
@api_view(['GET'])
def getData(request, **kwargs):
    data = 'some data'
    return JsonResponse({'status': True, 'data': data})


@utils.requireLogin
@api_view(['GET'])
def getProducts(request, **kwargs):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    mydb = myclient["mydb"]

    prdColl = mydb['product']

    products = prdColl.find()
    return JsonResponse({'status': True, 'data': [p['name'] for p in products]})
