"""Import packages and modules."""
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from app.models import Anime, Studio, Genre, Watchlist, User
from app.main.forms import AnimeForm, StudioForm, GenreForm, WatchlistForm
from app import bcrypt

# Import app and db from songs_app package so that we can run app
from app import app, db

main = Blueprint("main", __name__)

#___________________________________
#           Routes                       
#___________________________________

@main.route('/')
def home():
    '''Display homepage with all playlists from users'''
    all_watchlists = Watchlist.query.all()
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
    
@main.route('/anime_in_watchlist/<id>')
@login_required
def anime_in_watchlist(id):
    '''Display selected watchlist with all animes from that watchlist'''
    selected_watchlist = Watchlist.query.filter_by(id=id).one()
    all_animes = selected_Watchlist.songs
    return render_template('anime_in_watchlist.html',
    all_animes=all_animes)


@main.route('/create_anime', methods=['GET', 'POST'])
@login_required
def create_anime():
    '''Create a Anime Route'''
    form = AnimeForm()
    if form.validate_on_submit(): 
        new_anime = Anime(
            title=form.title.data,
            photo_url = form.photo_url.data,
            date=form.date.data,
            studio=form.studio.data,
            genres=form.genres.data,
            watchlists=form.watchlists.data
        )
        db.session.add(new_anime)
        db.session.commit()

        flash('New anime was created successfully.')
        return redirect(url_for('main.anime_detail', anime_id=new_anime.id))
    return render_template('create_anime.html', form=form)
