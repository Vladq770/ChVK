import pytest

from backend.models import Movie, Review, User, Genre, Subscription



@pytest.mark.django_db(True)
def test_user_create():
    data = {'first_name':"test name", 'last_name': 'test lname', 'role': '0', 'cash_password': 'qwerty',
            'login': 'test login', 'email': 'mail', 'balance': '0.4'}
    user = User(**data)
    user.save()
    assert 1 == 1
    users = User.objects.all()
    print(users[0].balance)



def test_genre_create():
    pass



def test_review_create():
    pass




def test_sub_create():
    pass




def test_movie_create():
    pass




