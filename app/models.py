# Create your models here.
"""Create database models to represent tables."""
from app import db
from sqlalchemy_utils import URLType
from sqlalchemy.orm import backref
from flask_login import UserMixin
import enum

# Models & Tables: 
# Watchlist, Anime, Watchlist_Anime_table
# Studio, Genre, Anime_genre_table
# User, user_Watchlist_table

class Anime(db.Model):
    """Anime model."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    photo_url = db.Column(URLType)
    date = db.Column(db.Date)

    # The Studio who animated the anime
    Studio_id = db.Column(db.Integer, db.ForeignKey('Studio.id'), nullable=False)
    Studio = db.relationship('Studio', back_populates='Anime')

    # The genres of a Anime can be
    genres = db.relationship(
        'Genre', secondary='anime_genre', back_populates='Anime')
    
    # What watchlist does this Anime belong to?
    playlists = db.relationship(
        'Watchlist', secondary='Anime_in_Watchlist', back_populates='Anime')

    def __str__(self):
        return f'Anime: {self.title}'
    
class Studio(db.Model):
    """Studio model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    about = db.Column(db.String(350))
    
    # The Anime animated by the Studio
    animes = db.relationship('Anime', back_populates='Studio')

    def __str__(self):
        return f'{self.name}'
    

class Genre(db.Model):
    """Genre model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)

    # The genre a anime belongs to
    songs = db.relationship(
        'Anime', secondary='anime_genre', back_populates='genres')

    def __str__(self):
        return f'{self.name}'

anime_genre_table = db.Table('anime_genre',
    db.Column('anime_id', db.Integer, db.ForeignKey('anime.id')),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'))
)