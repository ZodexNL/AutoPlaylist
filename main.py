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
import os
import youtube_dl

# still not working

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from exceptions import ResponseException

# This gets the variables from another file
from apikeys import spotify_user_id, spotify_token
print("test1")

class CreatePlaylist:

    # This method is called everytime an object is created from a class
    # __init__ initializes the object's attributes
    def __init__(self):

        # Set the user ID attribute
        self.user_id = spotify_user_id
        self.spotify_token = spotify_token
        self.youtube_client = self.get_youtube_client()
        self.all_song_info = {}
        print("test1")

    # Function to log into YouTube
    def get_youtube_client(self):
        print("hello")
        """ Log Into Youtube, Copied from Youtube Data API """
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secret2.json"

        # Get credentials and create an API client
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()

        # from the Youtube DATA API
        youtube_client = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)
        print("test1")
        return youtube_client

    # Function to get our liked videos and create a dictionary of important song info
    def get_liked_videos(self):
        """Grab Our Liked Videos & Create A Dictionary Of Important Song Information"""
        request = self.youtube_client.videos().list(
            part="snippet,contentDetails,statistics",
            myRating="like"
        )
        response = request.execute()

        # collect each video and get important information
        for item in response["items"]:
            video_title = item["snippet"]["title"]
            youtube_url = "https://www.youtube.com/watch?v={}".format(
                item["id"])

            # use youtube_dl to collect the song name & artist name
            video = youtube_dl.YoutubeDL({}).extract_info(
                youtube_url, download=False)
            song_name = video["track"]
            artist = video["artist"]
            print("test1")

            if song_name is not None and artist is not None:
                # save all important info and skip any missing song and artist
                self.all_song_info[video_title] = {
                    "youtube_url": youtube_url,
                    "song_name": song_name,
                    "artist": artist,

                    # add the uri, easy to get song to put into playlist
                    "spotify_uri": self.get_spotify_uri(song_name, artist)

                }

    # Function that creates a new spotify playlist
    def create_playlist(self):

        # This sets the name, description and wether or not the playlist should be public
        request_body = json.dumps({
            "name": "Alle gelikde YouTube video's",
            "description": "Alle gelikede videos's op YouTube",
            "public": "false"
        })
        print("test1")
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
    def get_spotify_uri(self, song_name, artist):

        # THis formats the api call

        query = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(
            song_name,
            artist
        )
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        # get the response in a json
        response_json = response.json()
        songs = response_json["tracks"]["items"]

        # this makes sure it only uses the first song
        uri = songs[0]["uri"]
        print("test1")
        return uri

    # Function to add the song to the spotify playlist
    def add_song_to_playlist(self):
        """Add all liked songs into a new Spotify playlist"""
        # populate dictionary with our liked songs
        self.get_liked_videos()

        # collect all of uri
        uris = [info["spotify_uri"]
                for song, info in self.all_song_info.items()]

        # create a new playlist
        playlist_id = self.create_playlist()

        # add all songs into new playlist
        request_data = json.dumps(uris)

        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            playlist_id)

        response = requests.post(
            query,
            data=request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        print("test1")
        # check for valid response status
        if response.status_code != 200:
            raise ResponseException(response.status_code)

        response_json = response.json()
        return response_json


if __name__ == '__main__':
    cp = CreatePlaylist()
    cp.add_song_to_playlist()
