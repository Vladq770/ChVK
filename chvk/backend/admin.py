from django.contrib import admin

from .models import User, Genre, Subscription, Movie, Review


class UserAdmin(admin.ModelAdmin):
    save_as = True
    save_on_top = True
    list_display = ('first_name', 'last_name', 'login')
    search_fields = ('first_name', 'last_name', 'login')
    list_filter = ('first_name', 'last_name')
    readonly_fields = ('created_at','last_login')


class MovieAdmin(admin.ModelAdmin):
    save_as = True
    save_on_top = True
    list_display = ('title', 'director', 'year')
    search_fields = ('title', 'director', 'year')
    list_filter = ('director', 'year', 'genres')
    readonly_fields = ('average_rating',)


class GenreAdmin(admin.ModelAdmin):
    save_as = True
    save_on_top = True
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
    #readonly_fields = ('name',)


class SubscriptionAdmin(admin.ModelAdmin):
    save_as = True
    save_on_top = True
    list_display = ('user', 'movie', 'price')
    search_fields = ('user', 'movie', 'price')
    list_filter = ('user', 'movie', 'price')
    readonly_fields = ('user', 'movie', 'price', 'created_at')

    def has_add_permission(self, request, obj=None):
        return False


class ReviewAdmin(admin.ModelAdmin):
    save_as = True
    save_on_top = True
    list_display = ('movie', 'user', 'rating')
    search_fields = ('movie', 'user', 'rating')
    list_filter = ('movie', 'user', 'rating')
    readonly_fields = ('user', 'movie', 'rating', 'created_at', 'review')

    def has_add_permission(self, request, obj=None):
        return False



admin.site.register(User, UserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Review, ReviewAdmin)