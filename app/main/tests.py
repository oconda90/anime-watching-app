import os
import unittest

from datetime import date
 
from app import app, db, bcrypt
from app.models import Anime, Studio, Genre, Watchlist, User

"""
Run these tests with the command:
python -m unittest app.main.tests
"""

#________________________________________________
# Setup
#________________________________________________

def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)

def create_anime():
    a1 = Studio(name='Mappa')
    s1 = Anime(
        title='Jujutsu Kaisen',
        photo_url="https://static.wikia.nocookie.net/jujutsu-kaisen/images/8/88/Anime_Key_Visual_2.png/revision/latest?cb=20201212034001",
        date=date(2020, 9, 19),
        Studio=a1
    )
    db.session.add(s1)

    a2 = Studio(name='Bones')
    s2 = Anime(title='My Hero Academia', Studio=a2)
    db.session.add(s2)
    db.session.commit()

def create_user():
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='test1', name='Test1', password=password_hash)
    db.session.add(user)
    db.session.commit()

