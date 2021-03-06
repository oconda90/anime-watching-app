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
    
     def test_create_studio(self):
        """Test creating an studio."""
        create_user()
        login(self.app, 'test1', 'password')

        post_data = {
            'name': 'Mappa',
            'about': 'MAPPA Co., Ltd. is a Japanese animation studio. It was founded on June 14, 2011, by Masao Maruyama, a founder and former producer of Madhouse, and has produced anime works including Kids on the Slope, Terror in Resonance, Yuri!!! on Ice, and In This Corner of the World.'
        }
        self.app.post('/create_studio', data = post_data)

        new_studio = Studio.query.filter_by(name='Mappa').one()
        self.assertIsNotNone(new_studio)
    

    # TEST PASSED
    def test_create_genre(self):
        """Test creating a genre."""
        create_user()
        login(self.app, 'test1', 'password')

        post_data = {
            'name': 'Shounen'
        }
        self.app.post('/create_genre', data = post_data)

        new_genre = Genre.query.filter_by(name = 'Shounen').one()
        self.assertIsNotNone(new_genre)
    
    
    # TEST PASSED
    def test_create_watchlist(self):
        """Test creating a watchlist."""
        create_user()
        login(self.app, 'test1', 'password')

        post_data = {
            'name': 'Shounen Anime',
            'photo_url': 'https://qph.fs.quoracdn.net/main-qimg-c13003a55f4efb7647d972cfcec4fadb'
        }
        self.app.post('/create_watchlist', data = post_data)

        new_watchlist = Watchlist.query.filter_by(name = 'Shounen Anime').one()
        self.assertIsNotNone(new_watchlist)