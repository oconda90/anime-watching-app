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

#_______________________________________________
# Tests
#_______________________________________________

class MainTests(unittest.TestCase):
 
    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
    

    
    def test_create_anime(self):
        """Test creating a anime."""
        create_anime()
        create_user()
        login(self.app, 'test1', 'password')

        post_data = {
            'title':'Jujutsu Kaisen',
            'photo_url':"https://static.wikia.nocookie.net/jujutsu-kaisen/images/8/88/Anime_Key_Visual_2.png/revision/latest?cb=20201212034001",
            'date': '2020-09-19',
            'Studio':1
        }
        self.app.post('/create_anime', data=post_data)

        created_anime = Anime.query.filter_by(title='Jujutsu Kaisen')
        self.assertIsNotNone(created_anime)
    
    
    
    def test_create_anime_logged_out(self):
        """
        Test that the user is redirected when trying to access the create anime
        route if not logged in.
        """
        create_anime()
        create_user()

        response = self.app.get('/create_anime')

        self.assertEqual(response.status_code, 302)
        self.assertIn('/login?next=%2Fcreate_anime', response.location)