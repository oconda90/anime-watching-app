"""Import packages and modules."""
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from songs_app.models import Song, Artist, Genre, Playlist, User
from songs_app.main.forms import SongForm, ArtistForm, GenreForm, PlaylistForm
from songs_app import bcrypt

# Import app and db from songs_app package so that we can run app
from app import app, db

main = Blueprint("main", __name__)

#___________________________________
#           Routes                       
#___________________________________

@main.route('/')
def home():
    '''Display homepage with all playlists from users'''
    all_watchlists = watchlist.query.all()
    return render_template('home.html',
        all_watchlists=all_watchlists)


@main.route('/profile/<username>')
@login_required
def profile(username):
    '''Display profile with all playlists from current_user'''
    user = User.query.filter_by(username=username).one()
    current_watchlists = user.watchlists
    return render_template('profile.html',
        current_watchlists=current_watchlists)