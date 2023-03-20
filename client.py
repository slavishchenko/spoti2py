import base64
import datetime
import logging
from urllib.parse import urlencode

import requests

from artist import Artist
from track import Track
from album import Album, Copyright
from image import Image
from parsers import SearchParser, AudioAnalysis


logging.basicConfig(level=logging.WARNING)


class BaseClient:
    API_URL = "https://api.spotify.com/"
    CURRENT_API_VERSION = "v1"

    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_expired = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"

    def __init__(self, client_id: str, client_secret: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self) -> str:
        """
        Returns base64 encoded string
        """
        client_id = self.client_id
        client_secret = self.client_secret
        if client_id is None or client_secret is None:
            raise Exception("You must provide client_id and client_secret")
        client_credentials = f"{client_id}:{client_secret}"
        client_credentials_b64 = base64.b64encode(client_credentials.encode())
        return client_credentials_b64.decode()

    def get_token_headers(self) -> dict:
        return {"Authorization": f"Basic {self.get_client_credentials()}"}

    def get_token_data(self) -> dict:
        return {"grant_type": "client_credentials"}

    def authenticate(self) -> bool:
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        r = requests.post(token_url, data=token_data, headers=token_headers)
        if r.status_code not in range(200, 299):
            raise Exception("Authentication failed!")
        data = r.json()
        now = datetime.datetime.now()
        access_token = data["access_token"]
        expires_in = data["expires_in"]
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_expired = expires < now
        return True

    def get_access_token(self) -> str:
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.authenticate()
            return self.get_access_token()
        elif token == None:
            self.authenticate()
            return self.get_access_token()
        return token

    def get_resource_headers(self) -> dict:
        access_token = self.get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        return headers

    def get_resource(self, lookup_id, resource_type="albums", version="v1") -> dict:
        endpoint = f"{self.API_URL}{version}/{resource_type}/{lookup_id}"
        headers = self.get_resource_headers()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    def base_search(self, query_params) -> dict:
        headers = self.get_resource_headers()
        endpoint = f"{self.API_URL}{self.CURRENT_API_VERSION}/search"
        lookup_url = f"{endpoint}?{query_params}"
        r = requests.get(lookup_url, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return SearchParser(r.json())

    def search(
        self,
        query=None,
        operator=None,
        operator_query=None,
        search_type: list = None,
        limit=1,
    ) -> dict:
        """
        Specify query you want you want to search for. e.g Metallica Master of Puppets.

        For more complex queries, specify operator (OR/NOT) and operator_query.

        search_type is a list of item types to search across.
        Search results include hits from all of the specified item types.
        >>> search_type = ['track', 'album']
        If you want to search for a specific item type,
        you can set search_type to a string. E.g. search_type = 'track'.
        Default value is track.

        limit is the maximum number of results to return in each item type.
            >= 0 <= 50
            Default value is 1.
        """
        if query == None:
            raise Exception("A query is required")

        if search_type is None:
            search_type = "track"
        if isinstance(search_type, list):
            search_type = ",".join([type.lower() for type in search_type])
        if isinstance(search_type, str):
            search_type = search_type.lower()

        if isinstance(query, dict):
            query = " ".join([f"{k}:{v}" for k, v in query.items()])
        if operator != None and operator_query != None:
            if operator.lower() == "or" or operator.lower() == "not":
                operator = operator.upper()
                if isinstance(operator_query, str):
                    query = f"{query} {operator} {operator_query}"
        query_params = urlencode({"q": query, "type": search_type, "limit": limit})

        return self.base_search(query_params)


class Client(BaseClient):
    def __init__(self, client_id: str, client_secret: str, *args, **kwargs) -> None:
        super().__init__(client_id, client_secret, *args, **kwargs)

    def get_album(self, _id):
        album = Album(**self.get_resource(_id, resource_type="albums"))
        album.artists = Artist(**album.artists[0])
        album.copyrights = [Copyright(**copy) for copy in album.copyrights]
        album.images = [Image(**img) for img in album.images]
        album.tracks = [Track(**song) for song in album.tracks["items"]]
        return album

    def get_artist(self, _id):
        return self.get_resource(_id, resource_type="artists")

    def get_track(self, _id):
        track = Track(**self.get_resource(_id, resource_type="tracks"))
        album = Album(**track.album)
        artists = Artist(**track.artists[0])
        track.album = album
        track.artists = artists
        return track

    def get_audio_analysis(self, _id):
        return AudioAnalysis(self.get_resource(_id, resource_type="audio-analysis"))
