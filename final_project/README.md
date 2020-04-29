# SI_507_Intermediate_programming

The project has 2 major functions: 
a) Create a playlist for user’s Spotify account based on location by scraping website and accessing Spotify API; 
b) Visually present the artist/tracks result by Flask app. 

The 4 authentication information needed for using Spotify API and how to be acquired are as below:
•	GET_TOKENS: https://developer.spotify.com/console/get-artist-albums/
•	POST_TOKENS: https://developer.spotify.com/console/post-playlist-tracks/
•	USER_IDS = https://www.spotify.com/us/account/overview/
•	COUNTRYS = 'US'

It should be noticed that a) Tokens could be expired, but they can be applied for unlimited times. The program will have notification when they expired; b) By default, the search results are limited in United States. 
Packages needed: requests, Flask, sqlite3, pandas, Beautifulsoup
