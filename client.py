import base64
import datetime
import logging
from urllib.parse import parse_qsl, urlencode

import requests

from exceptions import NoSearchQuery
from models import (
    Album,
    Artist,
    AudioAnalysis,
    Copyright,
    Followers,
    Image,
    Search,
    Track,
)

logging.basicConfig(
    filename="logs.log",
    level=logging.INFO,
    datefmt="%H:%M:%S",
)
OPTIONS = {
    "tracks": {"main": Track, "extra": {"artists": Artist, "album": Album}},
    "albums": {"main": Album, "extra": {"artists": Artist, "images": Image}},
}


class Client:
    """
    Client used to interact with the Spotify Web Api.

    :param client_id: Your Client ID.
    :type client_id: str
    :param client_secret: Your Client Secret
    :type client_secret: str
    """

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

    def get_resource(
        self, lookup_id: str, resource_type: str = "albums", version: str = None
    ) -> dict:
        """Sends a GET request to Spotify API"""
        if not version:
            version = self.CURRENT_API_VERSION
        endpoint = f"{self.API_URL}{version}/{resource_type}/{lookup_id}"
        headers = self.get_resource_headers()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    @staticmethod
    def _get_json_lookup_key(query_params: str):
        """Returns the key that will be used to parse json"""
        return f"{parse_qsl(query_params)[1][1]}s"

    @staticmethod
    def _parse_search_items(lookup_key: str, search_result: dict = None) -> object:
        """
        Parses JSON response
        """
        classes = OPTIONS.get(lookup_key)
        # Converts search result itmes from json object to corresponding Python class
        # E.G search_result.items will be a list of Track objects
        search_result.items = [classes["main"](**item) for item in search_result.items]
        # item is an instance of a class; E.G Track/Album
        for item in search_result.items:
            for k, v in classes["extra"].items():
                # k is a class attribute name
                # v is a class instance
                if isinstance(getattr(item, k), list):
                    setattr(item, k, [v(**artist) for artist in getattr(item, k)])
                else:
                    setattr(item, k, v(**getattr(item, k)))
        return search_result

    def base_search(self, query_params) -> dict:
        headers = self.get_resource_headers()
        endpoint = f"{self.API_URL}{self.CURRENT_API_VERSION}/search"
        lookup_url = f"{endpoint}?{query_params}"
        r = requests.get(lookup_url, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        search_type = self._get_json_lookup_key(query_params)
        search_result = Search(**r.json()[search_type])
        return self._parse_search_items(
            lookup_key=search_type, search_result=search_result
        )

    def search(
        self,
        query: str,
        operator: str = None,
        operator_query: str = None,
        search_type: str | list = None,
        limit: int = 1,
    ) -> Search:
        """
        Get Spotify catalog information about albums, artists and tracks \
        that match a keyword string.

        :param query: required - Your search query.
        :param search_type: Optional item type to search accross. Defaults to "track".
        :param limit: Maximum number of results to return. >= 0 <= 50. Default is 1.
        :raise exceptions.NoSearchQuery: If no query is provided.
        :return: :class:`~models.Search`
        :rtype: object
        """
        if query == None:
            raise NoSearchQuery("A query is required")

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

    def get_album(self, id: str) -> Album:
        """Get Spotify catalog information for a single album.

        :param id: The Spotify ID of the album. Required."
        :return: :class:`models.Album`
        :rtype: object
        """
        album = Album(**self.get_resource(id, resource_type="albums"))
        album.artists = Artist(**album.artists[0])
        album.copyrights = [Copyright(**copy) for copy in album.copyrights]
        album.images = [Image(**img) for img in album.images]
        album.tracks = [Track(**song) for song in album.tracks["items"]]
        return album

    def get_artist(self, id: str) -> Artist:
        """
        Get Spotify catalog information for a single artist identified by their unique Spotify ID.

        :param id: The Spotify ID of the artist. Required."
        :return: :class:`models.Artist`
        :rtype: object
        """
        artist = Artist(**self.get_resource(id, resource_type="artists"))
        artist.images = [Image(**img) for img in artist.images]
        artist.followers = Followers(**artist.followers)
        return artist

    def get_track(self, id: str) -> Track:
        """
        Get Spotify catalog information for a single track identified by its unique Spotify ID.

        :param id: The Spotify ID of the track. Required."
        :return: :class:`models.Track`
        :rtype: object
        """
        track = Track(**self.get_resource(id, resource_type="tracks"))
        track.album = Album(**track.album)
        track.artists = Artist(**track.artists[0])
        return track

    def get_audio_analysis(self, id: str) -> AudioAnalysis:
        """
        Get low-level audio analysis for a track in the Spotify catalog.
        The audio analysis describes the track’s structure and musical content, including rhythm, pitch, and timbre.

        :param id: The Spotify ID of the track. Required."
        :return: :class:`models.AudioAnalysis`
        :rtype: object
        """
        return AudioAnalysis(
            **self.get_resource(id, resource_type="audio-analysis")["track"]
        )
