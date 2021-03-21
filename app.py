import jinja2
from flask import Flask, request, redirect, render_template, url_for
from dotenv import load_dotenv
from flask import Flask, render_template, request, send_file
from pprint import PrettyPrinter
import os
import requests
import json

app = Flask(__name__, template_folder="templates")

load_dotenv()
API_KEY = os.getenv('API_KEY')
pp = PrettyPrinter(indent=4)



@app.route('/')
def page():
    """Display the web page."""

    full_name = request.args.get('full-name')
    
    character_list = []
    

    query = '''query ($name: String) {
    Character(search: $name) {
        id
        name {
        full
        }
        image {
        large
        }
        media {
        edges {
            voiceActors {
            image{
                large
            }
            name {
                full
            }
            language
            }
            node {
            title {
                romaji
                english
                native
                userPreferred
            }
            coverImage{
                large
            }
            type
            }
        }
        }
    }
    }
    '''
    variables = {
        'name': full_name
    }

    url = 'https://graphql.anilist.co'

    result_json = requests.post(
        url, json={'query': query, 'variables': variables})
    json_response = json.loads(result_json.text)

    # pp.pprint(json_response)
    character_name = []
    for i in range(len(json_response["data"]["Character"]["media"]["edges"])):
        character_list = json_response["data"]["Character"]["media"]["edges"][i]['voiceActors']
        for i in character_list:
            character_name.append(i["name"])
    char_image = json_response["data"]["Character"]["image"]["large"]
    va_img = json_response["data"]["Character"]["media"]["edges"][0]["voiceActors"][0]["image"]["large"]
    print(char_image)           

    
    context = {
        'full_name': full_name,
        "character_list": character_name[0]["full"],
        "char_image": char_image,
        "va_img": va_img
        
       
    }
    return render_template('index.html', **context)



@app.route('/shows.html')
def shows():
    """returns a bunch of stuff"""
    return render_template('shows.html')

@app.route('/search_return.html')
def search_return():
    """returns a bunch of stuff"""
    return render_template('search_return.html')

@app.route('/profile.html')
def profile():
    """returns a bunch of stuff"""
    return render_template('profile.html')

@app.route('/developers.html')
def developers():
    """returns a bunch of stuff"""
    return render_template('developers.html')



    


if __name__ == '__main__':
    app.run(debug=True)