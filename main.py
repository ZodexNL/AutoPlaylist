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

# This gets the variables from another file
from apikeys import spotify_user_id, spotify_token


class CreatePlaylist:

    # This method is called everytime an object is created from a class
    # __init__ initializes the object's attributes
    def __init__(self):

        # Set the user ID attribute
        self.user_id = spotify_user_id
        self.spotify_token = spotify_token

    # Function to log into YouTube
    def get_youtube_client(self):
        pass

    # Function to get our liked videos
    def get_liked_videos(self):
        pass

    # Function that creates a new spotify playlist
    def create_playlist(self):

        # This sets the name, description and wether or not the playlist should be public
        request_body = json.dumps({
            "name": "Alle gelikde YouTube video's",
            "description": "Alle gelikede videos's op YouTube",
            "public": "false"
        })

        # This is the call to the api and creates the playlist
        query = "https://api.spotify.com/v1/users/{}/playlists".format(self.user_id)

        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
        }
        )
        response_json = response.json()

        # the playlist id
        return response_json["id"]

    # Function that searches the song on spotify
    def get_spotify_uri(self):
        pass

    # Function to add the song to the spotify playlist
    def add_song_to_playlist(self):
        pass

