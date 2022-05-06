# imports
import requests
import json

from apikeys import spotify_user_id, spotify_token


def create_playlist(name, public):
    response = requests.post(
        spotify_user_id,
        headers={
            "Authorization": f"Bearer {spotify_token}"
        },
        json={
            "name": name,
            "public": public
        }
    )
    json_resp = response.json()

    return json_resp


def main():
    playlist = create_playlist(
        name="Mijn Playlist",
        public=False
    )

    print(f"Playlist: {playlist}")

    # pretty = json.dumps(playlist, indent=4)
    # print(pretty)

    ding = playlist["id"]
    print(ding)


if __name__ == '__main__':
    main()
