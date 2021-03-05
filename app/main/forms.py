# Create your forms here.
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SelectField, SubmitField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, ValidationError, URL
from app.models import Anime, Studio, Genre, Watchlist, User

#Forms: 
# AnimeFrom, StudioForm, GenreForm, WatchlistForm


class AnimeForm(FlaskForm):
    """Form to create a Anime."""
    title = StringField('Anime Title',
        validators=[DataRequired(), Length(min=10, max=85)])
    photo_url = StringField('Photo', validators=[URL()])
    date = DateField('Date Released')
    studio = QuerySelectField('Studio',
        query_factory=lambda: Studio.query, allow_blank=False)
    genres = QuerySelectMultipleField('Genres',
        query_factory=lambda: Genre.query, allow_blank=False)
    watchlists = QuerySelectMultipleField('Watchlist',
        query_factory=lambda: Watchlist.query, allow_blank=False)
    submit = SubmitField('Submit')


class StudioForm(FlaskForm):
    """Form to create an Studio"""
    name = StringField('Studio Name',
        validators=[DataRequired(), Length(min=6, max=50)])
    about = TextAreaField('Information About Studio')
    submit = SubmitField('Submit')