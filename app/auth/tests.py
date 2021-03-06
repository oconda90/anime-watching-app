import os
from unittest import TestCase

from datetime import date
 
from app import app, db, bcrypt
from app.models import Anime, Studio, Genre, Watchlist, User
"""
Run these tests with the command:
python -m unittest app.auth.tests
"""

#_______________________________________________
# Setup
#_______________________________________________

def create_anime():
    a1 = Studio(name='Mappa')
    g1 = Genre(name= 'Shounen')
    p1 = Watchlist(name= 'Shounens')
    s1 = Anime(
        title='Jujutsu Kaisen',
        photo_url="https://static.wikia.nocookie.net/jujutsu-kaisen/images/8/88/Anime_Key_Visual_2.png/revision/latest?cb=20201212034001",
        date=date(2020, 9, 19),
        studio=a1,
        genres=g1,
        watchlists=p1
    )
    db.session.add(s1)

    a2 = Studio(name='Bones')
    s2 = Anime(title='My Hero Academia', studio=a2)
    db.session.add(s2)
    db.session.commit()

def create_user():
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='test1', name='Test1', password=password_hash)
    db.session.add(user)
    db.session.commit()

#________________________________________________
# Tests
#________________________________________________

class AuthTests(TestCase):
    """Tests for authentication (login & signup)."""
 
    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    
    
    def test_signup(self):
        """Test signup route."""
        post_data = {
            'username': 'my-test@gmail.com',
            'name': 'my-test',
            'password': 'test12345'
        }
        self.app.post('/signup', data = post_data)

        new_user = User.query.filter_by(username = 'me-test@gmail.com')
        self.assertIsNotNone(new_user)

    def test_signup_existing_user(self):
        """Test to see if user already exists."""
        post_data = {
            'username': 'test@gmail.com',
            'name': 'Test',
            'password': 'test12345'
        }
        self.app.post('/signup', data = post_data)

        response = self.app.post('/signup', data=post_data)
        response_text = response.get_data(as_text=True)
        self.assertIn('That username is taken. Please choose a different one.', response_text)
    
    
    
    def test_login_correct_password(self):
        """Test with correct login passowrd."""
        create_user()

        post_data = {
            'username': 'test1',
            'name': 'Test1',
            'password': 'password1234'
        }
        self.app.post('/login', data = post_data)

        response = self.app.get('/', follow_redirects = True)
        response_text = response.get_data(as_text = True)
    
    def test_login_nonexistent_user(self):
        """Test with a non-existent user"""
        post_data = {
            'username': 'notreal',
            'name': 'Notreal',
            'password': 'notreal2345'
        }
        response = self.app.post('/login', data = post_data)
       
        response_text = response.get_data(as_text=True)
        self.assertIn('No user with that username. Please try again.', response_text)
    
    
    
    def test_login_incorrect_password(self):
        """Test with incorrect password."""
        create_user()

        post_data = {
            'username': 'test1',
            'name': 'Test1',
            'password': 'wrong1234'
        }
        response = self.app.post('/login', data = post_data)

        response_text = response.get_data(as_text=True)
        self.assertIn("Password doesn&#39;t match. Please try again.", response_text)