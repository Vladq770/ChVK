from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime
import os
import redis
from dotenv import load_dotenv
from copy import copy

from .models import User, Genre, Subscription, Movie, Review
from .utils import get_tokens
from .serializers import MovieSerializer, ReviewSerializer, UserSerializer


load_dotenv()

err_login = {'mes': 'login already exists'}
err_email = {'mes': 'email already exists'}
success = {'mes': 'Successfully!'}
is_not_user = {'mes': 'User is not found'}
bad_password = {'mes': 'Incorrect password'}
bad_token = {'mes': 'Token is not found'}
not_enough = {'mes': 'Not enough money'}
movie_bought = {'mes': 'Movie already bought'}


REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
#REDIS_EXPIRATION_TIME = int(os.getenv("REDIS_EXPIRATION_TIME"))

redis_instance = redis.StrictRedis(host=REDIS_HOST, port=int(REDIS_PORT))



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
    if user := User.objects.filter(login=login).first():
        return Response(err_login, 400)
    if user := User.objects.filter(email=email).first():
        return Response(err_email, 400)
    #user_create.password = hashlib.pbkdf2_hmac('sha256', str.encode(user_create.password), str.encode("salt"), 100000)
    user = User(**data)
    #user.__dict__['first_name'] = "wasd"
    user.save()
    return Response(success, 200)



@api_view(['POST'])
def sign_in(request):
    data = request.data
    login = data['login']
    password = data['cash_password']
    if user := User.objects.filter(login=login).first():
        if user.cash_password == password:
            time = int(datetime.utcnow().timestamp())
            user.last_login = time
            user.save()
            id = user.pk
            tokens = get_tokens(id, time)
            tokens['id'] = id
            redis_instance.set(f'{id}access', tokens['access_token'], 600)
            redis_instance.set(f'{id}refresh', tokens['refresh_token'], 600)
            tokens['user'] = UserSerializer(user).data
            return Response(tokens, 200)
        return Response(bad_password, 400)
    return Response(is_not_user, 400)



@api_view(['POST'])
def refresh(request):
    data = request.data
    id = data['id']
    refresh_token = data['refresh_token']
    #print((redis_instance.get(f'{id}refresh')).decode("utf-8"))
    if f'{id}refresh' in redis_instance and refresh_token == (redis_instance.get(f'{id}refresh')).decode("utf-8"):
        user = User.objects.get(pk=id)
        time = int(datetime.utcnow().timestamp())
        user.last_login = time
        user.save()
        tokens = get_tokens(id, time)
        tokens['id'] = id
        redis_instance.set(f'{id}access', tokens['access_token'], 600)
        redis_instance.set(f'{id}refresh', tokens['refresh_token'], 600)
        tokens['user'] = UserSerializer(user).data
        return Response(tokens, 200)
    return Response(bad_token, 400)


@api_view(['GET'])
def get_movies(request):
    data = Movie.objects.all()
    print(data)
    res = {}
    for i in range(len(data)):
        res[str(i)] = MovieSerializer(data[i]).data
    print(res)
    return Response(res, 200)


@api_view(['POST'])
def top_up_balance(request):
    data = request.data
    id = data['id']
    access_token = data['access_token']
    # print((redis_instance.get(f'{id}refresh')).decode("utf-8"))
    if f'{id}access' in redis_instance and access_token == (redis_instance.get(f'{id}access')).decode("utf-8"):
        user = User.objects.get(pk=id)
        user.balance += data['payment']
        user.save()
        mes = copy(success)
        mes['user'] = UserSerializer(user).data
        return Response(mes, 200)
    return Response(bad_token, 400)


@api_view(['POST'])
def subscription(request):
    data = request.data
    id = data['id']
    access_token = data['access_token']
    if f'{id}access' in redis_instance and access_token == (redis_instance.get(f'{id}access')).decode("utf-8"):
        user = User.objects.get(pk=id)
        movie = Movie.objects.get(pk=data['id_movie'])
        if not Subscription.objects.filter(user=user, movie=movie):
            if user.balance >= movie.price:
                sub = Subscription(user=user, movie=movie, price=movie.price)
                user.balance -= sub.price
                user.save()
                sub.save()
                mes = copy(success)
                mes['user'] = UserSerializer(user).data
                return Response(mes, 200)
            return Response(not_enough, 400)
        return Response(movie_bought, 400)
    return Response(bad_token, 400)


@api_view(['GET'])
def bought_movies(request):
    data = request.data
    id = data['id']
    access_token = data['access_token']
    if f'{id}access' in redis_instance and access_token == (redis_instance.get(f'{id}access')).decode("utf-8"):
        user = User.objects.get(pk=id)
        subs = Subscription.objects.filter(user=user)
        res = {}
        for i in range(len(subs)):
            res[str(i)] = MovieSerializer(subs[i].movie).data
        print(res)
        return Response(res, 200)
    return Response(bad_token, 400)


@api_view(['POST'])
def review(request):
    data = request.data
    id = data['id']
    access_token = data['access_token']
    if f'{id}access' in redis_instance and access_token == (redis_instance.get(f'{id}access')).decode("utf-8"):
        user = User.objects.get(pk=id)
        movie = Movie.objects.get(pk=data['id_movie'])
        if review := Review.objects.filter(user=user, movie=movie).first():
            review.delete()
        review = Review(user=user, movie=movie, rating=data['rating'], review=data['review'])
        review.save()
        revs = Review.objects.filter(movie=movie)
        avg = 0
        for i in range(len(revs)):
            avg += revs[i].rating
        avg /= len(revs)
        movie.average_rating = avg
        movie.save()
        return Response(success, 200)
    return Response(bad_token, 400)


@api_view(['GET'])
def movie_revs(request):
    data = request.data
    id = data['id_movie']
    movie = Movie.objects.get(pk=id)
    refs = Review.objects.filter(movie=movie)
    res = {}
    for i in range(len(refs)):
        res[str(i)] = ReviewSerializer(refs[i]).data
    res['movie'] = MovieSerializer(movie).data
    return Response(res, 200)
