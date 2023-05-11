from rest_framework.response import Response
from rest_framework.decorators import api_view
from .services import *



@api_view(['POST', 'GET'])
def index(request):
    data = request.data
    print(data)
    return Response(data, 200)



@api_view(['POST'])
def sign_up(request):
    data = request.data
    login = data['login']
    email = data['email']
    mes, code = sign_up_service(login, email, data)
    return Response(mes, code)


@api_view(['POST'])
def sign_in(request):
    data = request.data
    login = data['login']
    password = data['cash_password']
    mes, code = sign_in_service(login, password)
    return Response(mes, code)


@api_view(['POST'])
def refresh(request):
    data = request.data
    id = data['id']
    refresh_token = data['refresh_token']
    mes, code = refresh_service(id, refresh_token)
    return Response(mes, code)


@api_view(['GET'])
def get_movies(request):
    mes, code = get_movies_service()
    return Response(mes, code)


@api_view(['POST'])
def top_up_balance(request):
    data = request.data
    id = data['id']
    access_token = data['access_token']
    payment = data['payment']
    mes, code = balance_service(id, access_token, payment)
    return Response(mes, code)


@api_view(['POST'])
def subscription(request):
    data = request.data
    id = data['id']
    access_token = data['access_token']
    id_movie = data['id_movie']
    mes, code = subscription_service(id, access_token, id_movie)
    return Response(mes, code)



@api_view(['POST'])
def bought_movies(request):
    data = request.data
    id = data['id']
    access_token = data['access_token']
    mes, code = bought_service(id, access_token)
    return Response(mes, code)


@api_view(['POST'])
def review(request):
    data = request.data
    id = data['id']
    access_token = data['access_token']
    mes, code = review_service(id, access_token, data)
    return Response(mes, code)


@api_view(['POST'])
def movie_revs(request):
    data = request.data
    id = data['id_movie']
    mes, code = revs_service(id)
    return Response(mes, code)

