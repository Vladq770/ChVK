from rest_framework import serializers

from .models import Movie, Genre, Review, User


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = "__all__"


class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(read_only=True, many=True)
    class Meta:
        model = Movie
        fields = "__all__"


class UserLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('login',)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('login', 'email', 'first_name', 'last_name', 'balance', 'role')


class ReviewSerializer(serializers.ModelSerializer):
    user = UserLoginSerializer(read_only=True, many=False)
    class Meta:
        model = Review
        fields = ('user', 'rating', 'review')
