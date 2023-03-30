from .artist import Artist
from .image import Image


class Album:
    """
    Spotify Album model.

    :param album_group: The field is present when getting an artist's albums.
                        This field represents relationship between the artist and the album.
                        Example values: "compilation"
                        Allowed values: "album", "single", "compilation", "appears_on".
    :param album_type: The type of the album.
    :param artists: The artists of the album (simplified).
                    Each artist object includes a link in href to more detailed information about the artist.
    :param available_markets: The markets in which the album is available.
    :param external_urls: Known external URLs for this album.
    :param href: A link to the Web API endpoint providing full details of the album.
    :param id: Spotify id of the Album.
    :param images: The cover art for the album in various sizes, widest first.
    :param name: The name of the album.
    :param release_date: The date the album was first released.
    :param release_date_precision: The precision with which release_date value is known.
    :param total_tracks: The number of tracks in the album.
    :param type: The object type. Allowed values: "album".
    :param uri: The Spotify URI for the album.
    :param external_ids: Known external IDs for the album or None.
    :param copyrights: The copyright statements of the album.
    :param genres: A list of genres the album is associated with. If not yet classified, the list is empty.
    :param label: The label associated with the album.
    :param popularity: The popularity of the album. The values will be between 0 and 100.
    :param tracks: The tracks of the album. None for simplified version of the Album.
    :param is_playable: True, False or None.
    """

    def __init__(
        self,
        album_group: str,
        album_type: str,
        artists: list[Artist],
        available_markets: list[str],
        external_urls: dict,
        href: str,
        id: str,
        images: list[Image],
        name: str,
        release_date: str,
        release_date_precision: str,
        total_tracks: int,
        type: str,
        uri: str,
        external_ids=None | dict,
        copyrights=None | list["Copyright"],
        genres=None | list[str],
        label=None | str,
        popularity=None | int,
        tracks=None,
        is_playable=None | bool,
    ) -> None:
        self.album_group = album_group
        self.album_type = album_type
        self.artists = artists
        self.available_markets = available_markets
        self.external_urls = external_urls
        self.href = href
        self.id = id
        self.images = images
        self.name = name
        self.release_date = release_date
        self.release_date_precision = release_date_precision
        self.total_tracks = total_tracks
        self.type = type
        self.uri = uri
        self.external_ids = external_ids
        self.copyrights = copyrights
        self.genres = genres
        self.label = label
        self.populariy = popularity
        self.tracks = tracks
        self.is_playble = is_playable

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"


class Copyright:
    """
    Copyright model.

    :param text: The copytight text for this content.
    :param type: The type of copyright: C = the copyright, P = performance copyright.
    """

    def __init__(self, text: str, type: str) -> None:
        self.text = text
        self.type = type

    def __str__(self) -> str:
        return f"{self.text}"
