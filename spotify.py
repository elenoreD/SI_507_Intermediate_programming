import requests
import json
import string
from bs4 import BeautifulSoup
import sqlite3
import pandas as pd
import secrets
from flask import Flask, render_template, request
import plotly.graph_objects as go 
import urllib

####################################################################################################
# Project Overview 
####################################################################################################

# thinking logic
# input locations --> location/artist website --> list of artist names --> call spotify api -->
# post create a playlist --> get the playlist id --> search for artist and their top tracks --> post add tracks to my playlist

# part1:
# 2 post functions for playlists, 3 get functions for data retrieving 

# part2:
# cache data in json file to avoid token expire issue

# part3:
# create database, load info from different source to tables

# part4:
# Flask visualization 

# part5:
# lastly: user interaction main function

####################################################################################################
# part 1: data retrival 
####################################################################################################

GET_TOKEN = secrets.GET_TOKENS
POST_TOKEN = secrets.POST_TOKENS
USER_ID = secrets.USER_IDS
COUNTRY = secrets.COUNTRYS

def create_playlist(location, headers):

	''' Create an empty playlist for the user's spotify account
    
    Parameters
    ----------
    location: String
		A formatted string from user inputs

	headers: dictionary
		A dictionary of authentication information pairs
    
    Returns
    -------
    String:
		The id string of the empty playlist 
    '''

	new_playlist = "https://api.spotify.com/v1/users/{}/playlists".format(USER_ID)
	body = {
		"name": f'playlist for {location}',
		"description": "I'm a test playlist"
	}
	new_playlist = requests.post(new_playlist, headers = headers, data = json.dumps(body))
	if new_playlist.status_code != 201:
		print("token expired")
		exit(1)
	new_playlist = json.loads(new_playlist.text)
	return new_playlist["id"]


def get_artist_name_from_web(location):

	''' Scraping artist information from a webpage
    
    Parameters
    ----------
    location: String
		A formatted string from user inputs
    
    Returns
    -------
    list:
		A list of dictionaries of artist information for certian location.
		Each dictionary has 5 keys: name, local rank, picture image url of the artist, description and location
		By default, the function only get information of the top 5 artists
    '''

	artist_dic = {}
	name_list = []
	rank_list = []
	pic_list = []
	desc_list = []

	url = "https://www.ranker.com/list/{}-bands-and-musical-artists-from-here/reference".format(location)
	response = make_request_with_cache(url,error_message='web problem')

	soup = BeautifulSoup(response, 'html.parser')
	look_for_name = soup.find_all(class_='listItem__title')
	look_for_rank = soup.find_all('strong', class_='listItem__rank block center instapaper_ignore')
	look_for_pic = soup.find_all('img', class_='listItem__image lozad')
	look_for_description = soup.find_all(class_='listItem__wiki block default grey')

	for names in look_for_name:
		name = names.text.strip()
		name_list.append(name)

	for rank in look_for_rank:
		rank = rank.text.strip()
		rank_list.append(rank)
		
	for pic in look_for_pic:
		pic = pic['data-src']
		pic_list.append(pic)
	
	for desc in look_for_description:
		desc = desc.text.strip()
		desc_list.append(desc)

	artist_dic['name'] = name_list[:5]
	artist_dic['rank'] = rank_list[:5]
	artist_dic['picture'] = pic_list[:5]
	artist_dic['description'] = desc_list[:5]
	artist_dic['location'] = location[:5]
	
	return artist_dic

def get_artist_id(artist, headers):

	''' Get artist information through spotify API
    
    Parameters
    ----------
    artist: list
		A list of strings (artist names)

	headers: dictionary
		A dictionary of authentication information pairs
    
    Returns
    -------
    list:
		A list of dictionaries of artist information.
		Each dictionary has 4 keys: name, spotify artist id, number followers, and genres
    '''

	artistIDInfo_list = []
	
	for people in artist:
		artistIDInfo_dict = {}
		artist_search = "https://api.spotify.com/v1/search?q={}&type=artist&limit=1".format(people)
		artist_info = make_request_with_cache(artist_search, headers = headers)
		artist_info = json.loads(artist_info)['artists']['items'][0]

		artistIDInfo_dict['name'] = people
		artistIDInfo_dict['id'] = artist_info['id']
		artistIDInfo_dict['followers'] = artist_info['followers']['total']
		artistIDInfo_dict['genres'] = ' '.join(artist_info['genres'])
		artistIDInfo_list.append(artistIDInfo_dict)

	return artistIDInfo_list


def get_top_track_uris(artist_id, headers):

	''' Get top tracks information through spotify API
    
    Parameters
    ----------
    artist_id: string
		A string of artist spotify id

	headers: dictionary
		A dictionary of authentication information pairs
    
    Returns
    -------
    list:
		A list of dictionaries of top tracks information.
		Each dictionary has 6 keys: track uri information in spotify, album name, spotify artist id, track name, track length and picture image url of the track. 
		By default, the function only get information of the top 5 tracks of each artist
    '''

	top_tracks = "https://api.spotify.com/v1/artists/{}/top-tracks?country={}".format(artist_id, COUNTRY)
	top_tracks = make_request_with_cache(top_tracks, headers = headers)
	
	top_tracks = json.loads(top_tracks)["tracks"]
	top_tracks = top_tracks[:5]
	track_list = []
	for track in top_tracks:
		trackInfo_dict = {}
		trackInfo_dict['trackIDuri'] = track['uri']
		trackInfo_dict['albumName'] = track['album']['name']
		trackInfo_dict['artistID'] = track['artists'][0]['id']
		trackInfo_dict['trackName'] = track['name']
		trackInfo_dict['duration'] = track['duration_ms']*1.6667e-5
		trackInfo_dict['albumPic'] = track['album']['images'][1]['url']
		track_list.append(trackInfo_dict)

	return track_list



def add_tracks_to_playlist(headers, playlist_id, tracks):

	'''Add tracks to the empty list that created before.
    
    Parameters
    ----------
    headers: dictionary
		A dictionary of authentication information pairs
	
	playlist_id: string
		A string that identify a unique playlist
	
	tracks: list
		A list of track spotify urls
    
    Returns
    -------
    None
    '''

	new_track = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)
	body = {
		"uris": tracks
	}
	new_track = requests.post(new_track, headers = headers, data = json.dumps(body))

####################################################################################################
# part 2: cache 
####################################################################################################

CACHE_FILENAME = "spotify_cache.json"
CACHE_DICT = {}

def open_cache():

	''' Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary
    
    Parameters
    ----------
    None
    
    Returns
    -------
    The opened cache: dict
    '''

	try:
		cache_file = open(CACHE_FILENAME, 'r')
		cache_contents = cache_file.read()
		cache_dict = json.loads(cache_contents)
		cache_file.close()
	except:
		cache_dict = {}

	return cache_dict


def save_cache(cache_dict):

	''' Saves the current state of the cache to disk
    
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    
    Returns
    -------
    None
    '''

	dumped_json_cache = json.dumps(cache_dict)
	fw = open(CACHE_FILENAME,"w")
	fw.write(dumped_json_cache)
	fw.close() 


def make_request(baseurl, headers={}, error_message="token expired"):

	'''Make a request to the Web API using the baseurl and headers
    
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    headers: dictionary
        A dictionary of authentication information pairs
    
    Returns
    -------
    dict
        the data returned from making the request in the form of text
    '''

	response = requests.get(baseurl,headers=headers)
	if response.status_code != 200:
		print(error_message)
		exit(1)
	return response.text

CACHE_DICT = open_cache()

def make_request_with_cache(baseurl, headers={}, error_message="token expired"):

	'''Check the cache for a saved result for this baseurl. 
	If the result is found, return it. 
	Otherwise send a new request, save it, then return it.
    
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    headers: dictionary
        A dictionary of authentication information pairs
    error_message: string
        A string to validate the error information, by default it's 'token expired'. 
    
    Returns
    -------
    dict
        the results of the query as a dictionary loaded from cache
        JSON
    '''

	if baseurl in CACHE_DICT:
		# print('using caching')
		return CACHE_DICT[baseurl]
	else: 
		# print('feching')
		api_return = make_request(baseurl, headers, error_message)
		CACHE_DICT[baseurl] = api_return
		save_cache(CACHE_DICT)
		return CACHE_DICT[baseurl]



####################################################################################################
# part 3: database
####################################################################################################


def create_database():

	'''Create 3 empty tables for spotify.sqlite database.
	The information of 3 tables will be retrieved from previous functions
    
    Parameters
    ----------
   	None
    
    Returns
    -------
    None
    '''

	conn = sqlite3.connect('spotify.sqlite')
	cur = conn.cursor()
	
	create_RankArtist_sql = '''
		CREATE TABLE IF NOT EXISTS "Artist" (
			"Name" TEXT NOT NULL,
			"Rank" INTEGER NOT NULL, 
			"Picture" TEXT NOT NULL,
			"Description" TEXT,
			"Location" TEXT NOT NULL
		)
	'''
	create_ArtistInfo_sql = '''
		CREATE TABLE IF NOT EXISTS 'ArtistIDInfo'(
			'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
			'ArtistID' TEXT NOT NULL,
			'ArtistName' TEXT NOT NULL,
			'Genre' TEXT NOT NULL,
			'Followers' INTEGER
		)
	'''

	create_TrackInfo_sql = '''
			CREATE TABLE IF NOT EXISTS 'TrackInfo'(
			'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
			'ArtistID' TEXT NOT NULL,
			'TrackID' TEXT NOT NULL,
			'TrackName' TEXT NOT NULL,
			'AlbumName' TEXT NOT NULL,
			'Duration' TEXT NOT NULL,
			'AlbumPicture' TEXT NOT NULL
		)
	'''

	cur.execute(create_RankArtist_sql)
	cur.execute(create_ArtistInfo_sql)
	cur.execute(create_TrackInfo_sql)
	conn.commit()
	conn.close()

def load_Artist(artist_dict, db_name = 'spotify.sqlite', tbl_name = 'Artist'):

	'''Load infromation scraped from webpage to the table Artist
    
    Parameters
    ----------
    artist_dict: dictionary
        A dictionary of artist information

	db_name: string
        The database file name
	
	tbl_name: string
        The table name 
    
    Returns
    -------
    None
    '''

	conn=sqlite3.connect(db_name)
	cur = conn.cursor()                                 
	
	dataframe = pd.DataFrame(artist_dict)

	wildcards = ','.join(['?'] * len(dataframe.columns))              
	data = [tuple(x) for x in dataframe.values]
	
	# cur.execute("drop table if exists %s" % tbl_name)
	
	col_str = '"' + '","'.join(dataframe.columns) + '"'
	# cur.execute("create table %s (%s)" % (tbl_name, col_str))
	
	cur.executemany("insert into %s values(%s)" % (tbl_name, wildcards), data)
	
	conn.commit()
	conn.close()


def load_ArtistIDInfo(artist_names, headers):

	'''Load infromation retrieved from Spotify API to the table ArtistIDInfo
    
    Parameters
    ----------
    artist_names: list
        A list of strings

	headers: dictionary
		A dictionary of authentication information pairs
    
    Returns
    -------
    None
    '''

	response = get_artist_id(artist_names, headers)

	insert_AritistID_sql = '''
		INSERT INTO ArtistIDInfo
		VALUES (NULL, ?, ?, ?, ?)
	'''

	conn = sqlite3.connect('spotify.sqlite')
	cur = conn.cursor()

	for c in response:
		cur.execute(insert_AritistID_sql,
			[
				str(c['id']),
				str(c['name']), 
				str(c['genres']),
				int(c['followers'])
			]
		)
	
	conn.commit()
	conn.close()
	
def load_TrackInfo(artist_id_info_list, headers):

	'''Load infromation retrieved from Spotify API to the table TrackInfo
    
    Parameters
    ----------
    artist_id_info_list: list
        A list of dictionaries that with aritst information from Spotify API

	headers: dictionary
		A dictionary of authentication information pairs
    
    Returns
    -------
    None
    '''

	conn = sqlite3.connect('spotify.sqlite')
	cur = conn.cursor()

	insert_TrackID_sql = '''
		INSERT INTO TrackInfo
		VALUES (NULL, ?, ?, ?, ?, ?, ?)
	'''

	for element in artist_id_info_list:
		response = get_top_track_uris(element['id'], headers)

		for c in response:
			cur.execute(insert_TrackID_sql,
				[
					str(c['artistID']),
					str(c['trackIDuri']), 
					str(c['trackName']),
					str(c['albumName']),
					str(c['duration']),
					str(c['albumPic'])
				]
			)
	
	conn.commit()
	conn.close()



####################################################################################################
# part 4: visualization
####################################################################################################
app = Flask(__name__)

@app.route('/')
def index():

	'''Create a homepage for data collection.
    
    Parameters
    ----------
    None
    
    Returns
    -------
	render to the view template index.html
    '''

	return render_template('index.html')

def get_results(sort_by, sort_order, genre, location):

	'''Create queries based on the conditions (from parameters) and return the results
    
    Parameters
    ----------
    sort_by: string
        A string of column name of certain table 
    
	sort_order: string
        A string of column name of certain table 
	
	genre: string
        A string of column name of certain table 
	
	location: string
        A string of column name of certain table 

    Returns
    -------
    A SQL query result
    '''

	conn = sqlite3.connect('spotify.sqlite')
	cur = conn.cursor()
	
	if sort_by == 'Artist_Followers':
		sort_column = 'i.Followers'
	else:
		sort_column = 't.Duration'

	newlocation = location.lower()
	where_clause_location = f''' WHERE a.Location= "{newlocation}" '''

	if genre != 'All':
		newgenre = genre.lower()
		where_clause = f'''{where_clause_location} AND i.Genre like '%{newgenre}%' '''
	else:
		where_clause = where_clause_location

	q = f'''
		SELECT DISTINCT t.TrackName, a.Name, a.Location, a.Description, a.Picture, i.Followers, i.Genre, t.AlbumName, t.Duration, t.AlbumPicture
		FROM Artist a 
		JOIN ArtistIDInfo i
			ON a.Name=i.ArtistName
		JOIN TrackInfo t
			ON i.ArtistID=t.ArtistID
		{where_clause}
		ORDER BY {sort_column} {sort_order}
	'''

 
	results = cur.execute(q).fetchall()
	conn.close()
	return results


@app.route('/results', methods=['POST'])
def plot():

	'''Create the plot page for search result.
    
    Parameters
    ----------
    None
    
    Returns
    -------
	render to the view documents plot.html or results.html
    '''

	############
	# bar    ###
	############
	sort_by = request.form['sort']
	sort_order = request.form['dir']
	source_region = request.form['genre']
	location = request.form['location']
	results = get_results(sort_by, sort_order, source_region, location)

	plot_results = request.form.get('plot', False)
	if (plot_results):
		x_vals = [r[1] for r in results]
		y_vals = [r[5] for r in results]
		bars_data = go.Bar(
			x=x_vals,
			y=y_vals
		)
		fig = go.Figure(data=bars_data)
		div = fig.to_html(full_html=False)
		return render_template("plot.html", plot_div=div)
	else:
		return render_template('results.html', 
			sort=sort_by, results=results,
			region=source_region)


	# ############
	# # point   ##
	# ############
	# import plotly.express as px
	# sort_by = request.form['sort']
	# sort_order = request.form['dir']
	# source_region = request.form['genre']
	# location = request.form['location']
	# results = get_results(sort_by, sort_order, source_region, location)

	# plot_results = request.form.get('plot', False)
	# if (plot_results):
	# 	x_vals = [r[1] for r in results]
	# 	y_vals = [r[5] for r in results]
	# 	bars_data = go.Bar(
	# 		x=x_vals,
	# 		y=y_vals
	# 	)
	# 	fig = px.scatter(bars_data, x=y_vals, y=x_vals) 
				 
	# 	fig.update_layout(
	# 			   yaxis_title="Artist", 
	# 			 xaxis_title='number of followers on spotify')

	# 	div = fig.to_html(full_html=False)
	# 	return render_template("plot.html", plot_div=div)
	
	


####################################################################################################
# part 5: main function
####################################################################################################

def main():

	'''Main function that takes user input.
    
    Parameters
    ----------
    None 
    
    Returns
    -------
    None
    '''
	
	get_headers = {
		"Authorization": "Bearer {}".format(GET_TOKEN)
	}
	post_headers = {
		"Accept": "application/json",
		"Content-Type": "application/json",
		"Authorization": "Bearer {}".format(POST_TOKEN)
	}
	
	user_input = input('input location ')
	user_input = user_input.split()
	user_input = '-'.join(user_input)


	artist_name_infos = get_artist_name_from_web(user_input)
	artist_ID_infos = get_artist_id(artist_name_infos['name'], get_headers)

	total_track_info = []
	for infos in artist_ID_infos:
		track_info = get_top_track_uris(infos['id'], get_headers)
		total_track_info.extend(track_info)


	track_uri_list = []
	for element in total_track_info:
		track_uri_list.append(element['trackIDuri'])
	

	playlist_id = create_playlist(user_input, post_headers)
	add_tracks_to_playlist(post_headers, playlist_id, track_uri_list)

	
	# load_Artist(artist_name_infos)
	# load_ArtistIDInfo(artist_name_infos['name'], get_headers)
	# load_TrackInfo(artist_ID_infos, get_headers)
	

if __name__ == '__main__':
	main()
	app.run(debug=True)
	


	
	
