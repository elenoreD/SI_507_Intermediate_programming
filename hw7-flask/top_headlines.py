'''
Name: Shengnan Duan
Uniqname: elenore
'''

import secrets
from flask import Flask, render_template
import requests, json

app = Flask(__name__)

API_KEY = secrets.api_key

@app.route('/')
def index():
    title = 'Welcome!'
    return  f'<h1> {title} </h1>'

@app.route('/name/<nm>')
def name(nm):
    return render_template('name.html', name=nm)

@app.route('/headlines/<nm>')
def headlines(nm):
    base_url = 'https://api.nytimes.com/svc/topstories/v2/technology.json'
    params = {'api-key':API_KEY}
    results = requests.get(base_url,params).json()["results"]
    headlines = []
    for headline in results:
        headline_title = headline["title"]
        headlines.append(headline_title)
    return render_template('headline.html', name=nm, headline_list=headlines[:5])

@app.route('/links/<nm>')
def headlines_link(nm):
    base_url = 'https://api.nytimes.com/svc/topstories/v2/technology.json'
    params = {'api-key':API_KEY}
    results = requests.get(base_url,params).json()["results"]
    headlines = []
    headlinelinks = []
    for headline in results:
        headline_title = headline["title"]
        headline_link = headline['url']
        headlines.append(headline_title)
        headlinelinks.append(headline_link)
    return render_template('link.html', name=nm, headline_list=zip(headlines[:5], headlinelinks[:5]))

@app.route('/images/<nm>')
def headlines_table(nm):
    base_url = 'https://api.nytimes.com/svc/topstories/v2/technology.json'
    params = {'api-key':API_KEY}
    results = requests.get(base_url,params).json()["results"]
    headlines = []
    headlinelinks = []
    headlinepics = []
    for headline in results:
        headline_title = headline["title"]
        headline_link = headline['url']
        headline_image =headline['multimedia'][1]['url']
        headlines.append(headline_title)
        headlinelinks.append(headline_link)
        headlinepics.append(headline_image)
    return render_template('image.html', name=nm, title_list = headlines[0:5], url_list = headlinelinks[0:5], pic_list = headlinepics[0:5])




if __name__ == '__main__':   
    app.run(debug=True)
