"""

First we have to make sure we are logged into YouTube
Then we have to somehow grab our video's (maybe via playlist)(or via the songs that I liked on YouTube
The next step is to create a new playlist in spotify
And then we need to make sure that we search the song on Spotify
Lastly we need to add this song into our new Spotify playlist

"""

# imports
import json
import requests
from apikeys import spotify_user_id


class CreatePlaylist:

    # This method is called everytime an object is created from a class
    # __init__ initializes the object's attributes
    def __init__(self):

        # Set the user ID attribute
        self.user_id = spotify_user_id

    # Function to log into YouTube
    def get_youtube_client(self):
        pass

    # Function to get our liked videos
    def get_liked_videos(self):
        pass

    # Function that creates a new spotify playlist
    def create_playlist(self):

        # This is for the spotify playlist api
        request_body = json.dumps({
            "name": "Alle gelikde YouTube video's",
            "description": "Alle gelikede videos's op YouTube",
            "public": "True"
        })

        query = "https://api.spotify.com/v1/users/{}/playlists".format(self.user_id)

    # Function that searches the song on spotify
    def get_spotify_uri(self):
        pass

    # Function to add the song to the spotify playlist
    def add_song_to_playlist(self):
        pass

