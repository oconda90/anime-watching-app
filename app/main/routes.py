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
    selected_Watchlist = Watchlist.query.filter_by(id=id).one()
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

@main.route('/create_studio', methods=['GET', 'POST'])
@login_required
def create_studio():
    '''Create a Studio Route'''
    form = StudioForm()
    if form.validate_on_submit():
        new_studio = Studio(
            name=form.name.data,
            about=form.about.data
        )
        db.session.add(new_studio)
        db.session.commit()

        flash('New studio created successfully.')
        return redirect(url_for('main.home'))
    
    # if form was not valid, or was not submitted yet
    return render_template('create_studio.html', form=form)


@main.route('/create_genre', methods=['GET', 'POST'])
@login_required
def create_genre():
    '''Create a Genre Route'''
    form = GenreForm()
    if form.validate_on_submit():
        new_genre = Genre(
            name=form.name.data
        )
        db.session.add(new_genre)
        db.session.commit()

        flash('New genre created successfully.')
        return redirect(url_for('main.home'))
    
    # if form was not valid, or was not submitted yet
    return render_template('create_genre.html', form=form)

@main.route('/create_watchlist', methods=['GET', 'POST'])
@login_required
def create_watchlist():
    '''Create a Watchlist Route'''
    form = WatchlistForm()
    if form.validate_on_submit():
        new_watchlist = Watchlist(
            name=form.name.data,
            photo_url = form.photo_url.data,
            user = current_user
        )
        db.session.add(new_watchlist)
        db.session.commit()

        flash('New watchlist created successfully.')
        return redirect(url_for('main.home'))
    
    # if form was not valid, or was not submitted yet
    return render_template('create_watchlist.html', form=form)


@main.route('/anime/<anime_id>', methods=['GET', 'POST'])
@login_required
def anime_detail(anime_id):
    '''Shows Details of Anime'''
    anime = Anime.query.filter_by(id=anime_id).one()
    form = AnimeForm(obj=anime)
    
    # if form was submitted and contained no errors
    if form.validate_on_submit():
        anime.title = form.title.data
        anime.photo_url = form.photo_url.data
        anime.date = form.date.data
        anime.artist = form.studio.data
        anime.genres = form.genres.data
        anime.playlists = form.watchlists.data

        db.session.commit()

        flash('Anime was updated successfully.')
        return redirect(url_for('main.anime_detail', anime_id=anime_id))

    return render_template('anime_detail.html', anime=anime, form=form)



