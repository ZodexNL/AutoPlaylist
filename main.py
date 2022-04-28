import YouTube
from spotify import create_playlist, get_playlist_id, add_song_to_playlist
from youtube3 import YoutubeClient youtube = YoutubeClient()


def main():
    all_song_info = YouTube.youtube_initiate()
    playlist = create_playlist(name="Test Auto", public=False)
    playlist_id = get_playlist_id(playlist)
    add_song_to_playlist(playlist_id, all_song_info)
    YoutubeClient.

    if __name__ == '__main__':
        main()
