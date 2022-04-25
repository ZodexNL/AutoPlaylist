# Needed imports
import os
import requests
import youtube_dl
from googleapiclient.discovery import build

# Import this for the API keys
import apikeys

playlistIdInput = input("Playlist ID")
all_song_info = {}

youtube = build('youtube', 'v3', developerkey=apikeys.googleKey)


def get_spotify_uri(song_name, artist):
    query = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20"\
        .format(song_name, artist)
    response = requests.get(query, headers={
        "Content-Type": "application/json", "Authorization": "Bearer {}".format(apikeys.spotifySearchKey)

    })
    response_json = response.json()
    songs = response_json["tracks"]["items"]

    try:
        uri = songs[0]["uri"]
    except IndexError:
        uri = 'null'
        return uri


def youtube_initiate():
    nextPageToken = None
    while True:
        pl_request = youtube.playListItems().list(
            part='content Details', playlistId=playlistIdInput, maxResults=50, pageToken=nextPageToken
        )
        pl_response = pl_request.execute()
        nextPageToken = pl_request.get('nextPageToken')
        vid_ids = []

        for item in pl_response['items']:
            vid_ids.append(item['contentDetails']['videoId'])

        vid_request = youtube.videos().list(
            part="snippet", id=",".join(vid_ids)
        )

        vid_response = vid_request.execute()

        for item in vid_response["items"]:
            video_title = item["snippet"]["title"]
            print(video_title)
            youtube_url = "https://www.youtube.com/watch?v={}".format(item["id"])

            # Use imported youtube_dl to collect song and artist name
            video = youtube.dl.YoutubeDL({}).extract_info(youtube_url, download=False)

            try:








