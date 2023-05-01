from django.db import migrations

from ..genres import genres


def create_genres(apps, schema_editor):
    Genre = apps.get_model('backend', 'Genre')
    for i in genres:
        Genre.objects.create(name=i)



class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0001_initial"),
    ]

    operations = [migrations.RunPython(create_genres)]