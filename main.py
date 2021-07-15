import json 
import requests
from secrets import user_id, access_token, refresh_token
from datetime import date
from refresh import Refresh

from requests.models import Response

class TopSongs:
    def __init__(self) -> None:
        self.user_id = user_id
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.songs = ""
        self.new_playlist_URI = ""


    def findTopSongs(self):
        print('Getting your top songs...')
        query = 'https://api.spotify.com/v1/me/top/tracks'

        response = requests.get(query, 
        params={"time_range": "short_term", "limit": 25}, 
        headers={"Content-Type": "application/json",
        "Authorization": "Bearer {}".format(self.access_token)})

        responseJSON = response.json()


        for i in responseJSON['items']:
            self.songs += (i['uri'] + ',')
            
        
        self.songs = self.songs[:-1]

        self.addToPlaylist()
            

    def createPlaylist(self):

        today = date.today()

        todayFormatted = today.strftime("%d/%m/%Y")

        print('Creating your playlist...')
        query = 'https://api.spotify.com/v1/users/{}/playlists'.format(self.user_id)

        # Developing a JSON query
        requests_body = json.dumps({
            "name": todayFormatted + " Top 25 Songs", "public": True
        })

        response = requests.post(query, data=requests_body, headers={"Content-Type": "application/json",
        "Authorization": "Bearer {}".format(self.access_token)})

        responseJSON = response.json()
        
        return responseJSON['id']


    def addToPlaylist(self):
        self.new_playlist_URI = self.createPlaylist()
        print('Adding songs to playlist...')
        query = 'https://api.spotify.com/v1/playlists/{}/tracks?uris={}'.format(self.new_playlist_URI, self.songs)

        response = requests.post(query, headers={"Content-Type": "application/json",
        "Authorization": "Bearer {}".format(self.access_token)})

        print(response.json)

    def call_refresh(self):

        print('Refreshing token...')

        refresh_caller = Refresh()
        self.access_token = refresh_caller.refresh()

        self.findTopSongs()


a = TopSongs()
a.call_refresh()
