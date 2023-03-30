import base64
import datetime
import logging
from urllib.parse import parse_qsl, urlencode

import requests

from exceptions import InvalidCredentials, NoSearchQuery
from models import (
    Album,
    Artist,
    AudioAnalysis,
    Copyright,
    Followers,
    Image,
    Recommendations,
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
    "artists": {"main": Artist, "extra": {"images": Image, "followers": Followers}},
}


class Client:
    """
    Client used to interact with the Spotify Web Api.

    :ivar client_id: Your Client ID.
    :ivar client_secret: Your Client Secret
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
        if not isinstance(client_id, str) and isinstance(client_secret, str):
            raise InvalidCredentials(
                "client_id and client_secret need to be of type 'str'."
            )
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

    @staticmethod
    def _get(endpoint: str, headers: str):
        return requests.get(endpoint, headers=headers)

    def get_resource(
        self, lookup_id: str, resource_type: str = "albums", version: str = None
    ) -> dict:
        """
        Sends a GET request to Spotify API

        :param lookup_id: Spotify ID for the desired resource.
        :param resource_type: Which resource you're trying to get. Default is: albums.
        :param version: Spotify API version. Defaults to CURRENT_API_VERSION.
        :return: Spotify JSON response
        :rtype: JSON
        """
        if not version:
            version = self.CURRENT_API_VERSION
        endpoint = f"{self.API_URL}{version}/{resource_type}/{lookup_id}"
        headers = self.get_resource_headers()
        r = self._get(endpoint, headers=headers)
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

        search_result.items = [classes["main"](**item) for item in search_result.items]
        for item in search_result.items:
            for attr_name, cls in classes["extra"].items():
                if isinstance(getattr(item, attr_name), list):
                    setattr(
                        item,
                        attr_name,
                        [cls(**artist) for artist in getattr(item, attr_name)],
                    )
                else:
                    setattr(item, attr_name, cls(**getattr(item, attr_name)))
        return search_result

    def base_search(self, query_params) -> dict:
        headers = self.get_resource_headers()
        endpoint = f"{self.API_URL}{self.CURRENT_API_VERSION}/search"
        lookup_url = f"{endpoint}?{query_params}"
        r = self._get(endpoint=lookup_url, headers=headers)
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
        """
        Get Spotify catalog information for a single album.

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

    def get_recommendations(
        self,
        limit: int = 20,
        seed_artists: list[str] = None,
        seed_genres: list[str] = None,
        seed_tracks: list[str] = None,
    ):
        """
        Recommendations are generated based on the available information or a given seed entity and matched against similar artists and tracks.
        For artists and tracks that are very new or obscure there might not be enough data to generate a list of tracks.

        :param limit: The target size of the list of recommended tracks.
                      Default: 20. Minimum: 1. Maximum: 100.
        :param seed_artists: A list of Spotify IDs for seed artists.
        :param seed_genres: A list of any genres in the set of available genre seeds.
                            available_genre_seeds is an attribute of the Client class.
        :param seed_tracks: A list of Spotify IDs fpr a seed track.
        NOTE:
            Up to 5 seed values may be provided in any combination of seed_artists, seed_tracks and seed_genres.
            At least 1 is required!

        :return: JSON object
        :rtype: JSON
        """
        if not seed_artists or seed_genres or seed_tracks:
            raise Exception("You need to provide at least 1 seed value.")

        query_params = {"limit": limit}
        if seed_artists:
            query_params["seed_artists"] = ",".join(seed_artists)
        if seed_genres:
            query_params["seed_genres"] = ",".join(seed_genres)
        if seed_tracks:
            query_params["seed_tracks"] = ",".join(seed_tracks)
        endpoint = f"{self.API_URL}{self.CURRENT_API_VERSION}/recommendations/?{urlencode(query_params)}"
        headers = self.get_resource_headers()

        r = self._get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return r.text
        return r.json()

    @property
    def available_genre_seeds(self):
        """
        A list of available genres seed parameter values for recommendations.

        :return: List of genres.
        :rtype: list[str]
        """
        endpoint = f"{self.API_URL}{self.CURRENT_API_VERSION}/recommendations/available-genre-seeds"
        headers = self.get_resource_headers()
        return self._get(endpoint=endpoint, headers=headers).json()["genres"]
