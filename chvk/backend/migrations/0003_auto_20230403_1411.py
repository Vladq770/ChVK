from django.db import migrations

from ..movies import movies


def create_movies(apps, schema_editor):
    Genre = apps.get_model('backend', 'Genre')
    Movie = apps.get_model('backend', 'Movie')
    for i in movies:
        genres = i['genres']
        del i['genres']
        movie = Movie(**i)
        movie.save()
        for j in genres:
            movie.genres.add(Genre.objects.get(name=j))
        movie.save()


class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0002_auto_20230403_1411"),
    ]

    operations = [migrations.RunPython(create_movies)]