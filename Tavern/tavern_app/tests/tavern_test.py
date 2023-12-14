import datetime

import pytest
from tavern_app.models import MasterSession, User, GamerSession


@pytest.mark.django_db
def test_sessions(client):
    response = client.get('/sessions/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_main(client):
    response = client.get('//')
    assert response.status_code == 200


@pytest.mark.django_db
def test_login(client):
    User.objects.create_user(username="Username", password="123qwe")
    response = client.login(username="Username", password="123qwe")

    assert response is True


@pytest.mark.django_db
def test_create_user(client):
    User.objects.create_user(username="Username", password="123qwe")

    assert len(User.objects.all()) == 1


@pytest.mark.django_db
def test_user_details(client):
    User.objects.create_user(username="Username", password="123qwe")
    user = User.objects.get(username="Username")

    response = client.get(f'/user/{user.id}/')

    assert response.status_code == 200


# If user not logged- redirect to login form
@pytest.mark.django_db
def test_mastersession_not_logged_so_redirected(client):
    title = 'TestMasterSession'
    date = '2024-03-03'
    time = '21:00:00'
    number_of_players = 3
    description = "Random description"
    difficulty = "Zrównoważona"
    adult_only = "NIE"
    other_requirements = "Brak"

    response = client.post('/create-master-session/', {'title': title,
                                                       'date': date,
                                                       'time': time,
                                                       'number_of_players': number_of_players,
                                                       'description': description,
                                                       'difficulty': difficulty,
                                                       'adult_only': adult_only,
                                                       'other_requirements': other_requirements,
                                                       })

    assert response.status_code == 302
    assert response.url == "/log-in/?next=/create-master-session/"


# if user logged- Create MasterSession
@pytest.mark.django_db
def test_mastersession_created(client):
    User.objects.create_user(username="Username", password="123qwe")
    response = client.login(username="Username", password="123qwe")

    title = 'TestMasterSession'
    date = '2024-03-03'
    time = '21:00:00'
    number_of_players = 3
    description = "Random description"
    difficulty = "Zrównoważona"
    adult_only = "NIE"
    other_requirements = "Brak"

    response = client.post('/create-master-session/', {'title': title,
                                                       'date': date,
                                                       'time': time,
                                                       'number_of_players': number_of_players,
                                                       'description': description,
                                                       'difficulty': difficulty,
                                                       'adult_only': adult_only,
                                                       'other_requirements': other_requirements,
                                                       })

    assert len(MasterSession.objects.all()) == 1

    session = MasterSession.objects.get(title=title)
    assert session.title == title
    assert session.date == datetime.date(2024, 3, 3)
    assert session.time == datetime.time(21, 0)
    assert session.number_of_players == number_of_players
    assert session.description == description
    assert session.difficulty == difficulty
    assert session.adult_only == adult_only
    assert session.other_requirements == other_requirements


# If user not logged- redirect to login form
@pytest.mark.django_db
def test_gamersession_not_logged_so_redirected(client):
    title = 'TestGamerSession'
    date = '2024-03-03'
    time = '21:00:00'
    description = "Random description"
    difficulty = "Zrównoważona"
    adult_only = "NIE"
    master_requirements = "Brak"
    other_requirements = "Brak"

    response = client.post('/create-gamer-session/', {'title': title,
                                                      'date': date,
                                                      'time': time,
                                                      'description': description,
                                                      'difficulty': difficulty,
                                                      'adult_only': adult_only,
                                                      'master_requirements': master_requirements,
                                                      'other_requirements': other_requirements,
                                                      })

    assert response.status_code == 302
    assert response.url == "/log-in/?next=/create-gamer-session/"


# if user logged- Create GamerSession
@pytest.mark.django_db
def test_gamersession_created(client):
    User.objects.create_user(username="Username", password="123qwe")
    response = client.login(username="Username", password="123qwe")

    title = 'TestGamerSession'
    date = '2024-03-03'
    time = '21:00:00'
    description = "Random description"
    difficulty = "Zrównoważona"
    adult_only = "NIE"
    master_requirements = "Brak"
    other_requirements = "Brak"

    response = client.post('/create-gamer-session/', {'title': title,
                                                      'date': date,
                                                      'time': time,
                                                      'description': description,
                                                      'difficulty': difficulty,
                                                      'adult_only': adult_only,
                                                      'master_requirements': master_requirements,
                                                      'other_requirements': other_requirements,
                                                      })

    assert len(GamerSession.objects.all()) == 1

    session = GamerSession.objects.get(title=title)
    assert session.title == title
    assert session.date == datetime.date(2024, 3, 3)
    assert session.time == datetime.time(21, 0)
    assert session.description == description
    assert session.difficulty == difficulty
    assert session.adult_only == adult_only
    assert session.master_requirements == master_requirements
    assert session.other_requirements == other_requirements
