from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    cash_password = models.CharField(max_length=256)
    login = models.CharField(max_length=30, unique=True)
    email = models.CharField(max_length=256, unique=True)
    balance = models.DecimalField(default=.0, validators=[MinValueValidator(.0)], max_digits=10, decimal_places=2)
    last_login = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    role = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])

    def __str__(self):
        return self.login


class Genre(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Movie(models.Model):
    genres = models.ManyToManyField(Genre)
    title = models.CharField(max_length=256)
    runtime = models.IntegerField(default=60)
    plot = models.CharField(max_length=256)
    average_rating = models.DecimalField(default=.0, validators=[MinValueValidator(.0), MaxValueValidator(5.0)],
                                         max_digits=5, decimal_places=2)
    price = models.DecimalField(default=.0, validators=[MinValueValidator(.0)], max_digits=5, decimal_places=2)
    year = models.IntegerField(validators=[MinValueValidator(1800), MaxValueValidator(2030)])
    director = models.CharField(max_length=128)
    posterUrl = models.CharField(default='', max_length=256)

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete = models.CASCADE)
    price = models.DecimalField(validators=[MinValueValidator(.0)], max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.CharField(max_length=256)
    created_at = models.DateTimeField(default=timezone.now)