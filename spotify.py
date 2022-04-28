import requests
import json
import apikeys


def create_playlist(name, public):
    response = requests.post(apikeys.spotify_url, headers={
        "Authorization": f"Bearer{apikeys.spotifyAddPlaylistKey}"}, json={"name": name, "public": public
    })
    json_resp = response.json()
    return json_resp


def get_playlist_id(resp):
    return resp["id"]


def add_song_to_playlist(playlist_id, all_song_info):
    uris = [info["spotify_uri"] for song, info in all_song_info.items()]
    request_body=json.dumps({
        "uris": uris
    })

    request_data = json.dumps(uris)
    query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
        playlist_id)
    response = requests.post(query, data=request_data, headers= {
        "Content-Type": "application/json", "Authorization": "Bearer {}".format(apikeys.spotifyAddItemKey)
    })
    print(response.status_code)
    response_json = response.json()
    return response_json
