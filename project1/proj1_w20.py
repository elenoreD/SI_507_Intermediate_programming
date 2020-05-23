#########################################
##### Name:          ShengnanDuan  ######
##### Uniqname:            elenore ######
#########################################
import json
import requests
import webbrowser
# Part 1

class Media:

    '''Any media type in iTunes
    Attributes
    ----------
    title : string
        Media's title
    author : string
        Media's author
    release_year: string
        Media's release_year
    url: string
        Media's preview url
    json: json file
        API's search results

    '''

    def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL", json=None):
        if json:
            try:
                self.title = json["collectionName"]
            except:
                self.title = json["trackName"]
            self.author = json["artistName"]
            self.release_year = json["releaseDate"].split('-')[0]
            try:
                self.url=json["collectionViewUrl"]
            except:
                self.url = json["trackViewUrl"]
            
        else:
            self.title = title
            self.author = author
            self.release_year = release_year
            self.url=url
    
    def info(self):
        '''Get the info of media, including title, author and release_year.

        Parameters
        ----------
        none

        Returns
        -------
        str
            The the info of media, including title, author and release_year
        '''
        return f"{self.title} by {self.author} ({self.release_year})"

    def length(self):
        '''Get the length of media.

        Parameters
        ----------
        none

        Returns
        -------
        int
            0
        '''
        return 0

class Song(Media):

    '''subclass of Media, specifically for song type of media in iTunes
    Attributes
    ----------
    title : string
        Song's title
    author : string
        Song's author
    release_year: string
        Song's release_year
    url: string
        Song's preview url
    album:
        Song's album info
    genre:
        Song's genre info
    track_length:
        Song's preview url
    json: json file
        API's search results

    '''
    def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL", album = "No Album", genre = "No Genre", track_length = 0, json=None):
        super().__init__(title , author, release_year, url, json)
        if json:
            self.title = json["trackName"]
            self.album = json["collectionName"]
            self.genre = json["primaryGenreName"]
            self.track_length = json["trackTimeMillis"]
            try:
                self.url=json["collectionViewUrl"]
            except:
                self.url = json["trackViewUrl"]
           

        else:
            self.album = album
            self.genre = genre
            self.track_length = track_length

    def info(self):

        '''Get the info of song, including title, author, release_year and genre

        Parameters
        ----------
        none

        Returns
        -------
        str
            The the info of song, including title, author, release_year and genre
        '''
        
        return f"{self.title} by {self.author} ({self.release_year}) [{self.genre}]"

    def length(self):

        '''Get the length of song.

        Parameters
        ----------
        none

        Returns
        -------
        int
            song's track_length
        '''
        return round(self.track_length * 0.001)

class Movie(Media):

    '''subclass of Media, specifically for movie type of media in iTunes
    Attributes
    ----------
    title : string
        Movie's title
    author : string
        Movie's author
    release_year: string
        Movie's release_year
    url: string
        Movie's preview url
    rating:
        Movie's album info
    movie_length:
        Movie's preview url
    json: json file
        API's search results

    '''

    def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL", rating = "No Rating", movie_length = 0, json=None):
        super().__init__(title, author, release_year, url, json)
        if json:
            self.title = json["trackName"]
            self.rating = json["contentAdvisoryRating"]
            self.movie_length = json["trackTimeMillis"]
            try:
                self.url=json["collectionViewUrl"]
            except:
                self.url = json["trackViewUrl"]
            

        else:
            self.rating = rating 
            self.movie_length = movie_length

    def info(self):

        '''Get the info of movie, including title, author, release_year and rating.

        Parameters
        ----------
        none

        Returns
        -------
        str
            The the info of movie, including title, author, release_year and genre
        '''
        return f"{self.title} by {self.author} ({self.release_year}) [{self.rating}]"

    def length(self):

        '''Get the length of movie.

        Parameters
        ----------
        none

        Returns
        -------
        int
            movie's movie_length
        '''
        return round(self.movie_length * 1.6667e-5)

# Part 2
# Done

# Part 3
def call_API(param):
    '''return a list from API that python can parse.

    call iTunes API and return the search result.

    Parameters
    ----------
    user1stinput: str
        user's input, usually a name of any media type

    Returns
    -------
    list
        a list of dictionaries 

    '''
    #https://itunes.apple.com/search?term=Beatles
    baseurl = 'https://itunes.apple.com/search'
    params_dict = {'term':param}
    response = requests.get(baseurl, params_dict)
    api_file = json.loads(response.text)['results']
    return api_file


# Other classes, functions, etc. should go here
def get_itunes_response (user1stinput):

    '''print the query results, and return a list of url objects for further processing.

    By calling the previous call_API function, creating objects for Song, Media and other media type. The function can print the media's infomation and parse media's url by using those objects.

    Parameters
    ----------
    user1stinput: str
        user's input, usually a name of any media type

    Returns
    -------
    list
        a list of urls. 

    '''

    song_list = []
    movie_list = []
    other_media_list = []
    for result in call_API(user1stinput):
        if 'kind' in result:
            if result['kind'] == 'song':
                song_result=Song(json=result)
                song_list.append(song_result)
                    
            elif result['kind'] =='feature-movie':
                movie_result=Movie(json=result)
                movie_list.append(movie_result)

        else:
            other_media_result=Media(json=result)
            other_media_list.append(other_media_result)

    count = 0
    url_list=[]
    print ('SONGS')
    for song in song_list:
        count += 1
        url_list.append(song.url)
        print (str(count)+ ' ' + song.info())

    print ('MOVIES')
    for movie in movie_list:
        count += 1
        url_list.append(movie.url)
        print (str(count)+ ' ' + movie.info())

    print ('OTHER MEDIA')
    for other in other_media_list:
        count += 1
        url_list.append(other.url)
        print (str(count)+ ' ' + other.info())

   
    return url_list



if __name__ == "__main__":
    # your control code for Part 4 (interactive search) should go here
    user1stinput = input ('Enter a search term, or "exit" to quit: ')

    if user1stinput == 'exit':
        print('Have a nice day :)')
        exit()

    else:
        all_url = get_itunes_response (user1stinput) # user's first input, should be a string
        
        while True:
            user2ndinput = input ('Enter the number to see corresponding detailed page, start a new search or exit to quit: ') # after first input, the second function triggered. user can keep checking preview page, start a new search or exit
            if user2ndinput.isnumeric() and int(user2ndinput) < len(all_url): # go to preview page
                direct_to_url = all_url [int(user2ndinput)-1]
                print('Directing to', direct_to_url)
                webbrowser.open(direct_to_url)
                break

            elif user2ndinput.isnumeric() and int(user2ndinput) >= len(all_url):
                print('Please search for number index within the results list')

            elif user2ndinput == 'exit': # exit
                print('Thanks for searching, Have a nice day :)')
                exit()

            else:
                get_itunes_response (user2ndinput) # start a new search

            

