import json
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, CacheFileHandler, SpotifyOAuth
import boto3
from datetime import datetime

def lambda_handler(event, context):
    
    cilent_id = os.environ.get('client_id')
    client_secret = os.environ.get('client_secret')
    
    client_credentials_manager = SpotifyClientCredentials(client_id=cilent_id, client_secret=client_secret)

    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    
    playlist_link = "https://open.spotify.com/playlist/6VOedaf3eNWDOVpa9Qdlvg"
    playlist_URI = playlist_link.split("/")[-1]
    
    spotify_data = sp.playlist_tracks(playlist_URI)   
    
    #creating s3 client for s3 related operations
    cilent = boto3.client('s3')
    
    filename = "spotify_raw_" + str(datetime.now()) + ".json"

    
    cilent.put_object(
        Bucket="spotify-etl-project-madhav123",
        Key="raw_data/to_process/" + filename,
        Body=json.dumps(spotify_data)
        )