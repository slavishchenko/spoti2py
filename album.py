class BaseAlbum:
    def __init__(
        self,
        album_group,
        album_type,
        artists,
        available_markets,
        external_urls,
        href,
        id,
        images,
        name,
        release_date,
        release_date_precision,
        total_tracks,
        type,
        uri,
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

    def __str__(self):
        return f"{self.name}"


class Album(BaseAlbum):
    def __init__(
        self,
        album_group,
        album_type,
        artists,
        available_markets,
        external_urls,
        href,
        id,
        images,
        name,
        release_date,
        release_date_precision,
        total_tracks,
        type,
        uri,
        external_ids,
        copyrights,
        genres,
        label,
        popularity,
        tracks,
    ) -> None:
        super().__init__(
            album_group,
            album_type,
            artists,
            available_markets,
            external_urls,
            href,
            id,
            images,
            name,
            release_date,
            release_date_precision,
            total_tracks,
            type,
            uri,
        )
        self.external_ids = external_ids
        self.copyrights = copyrights
        self.genres = genres
        self.label = label
        self.populariy = popularity
        self.tracks = tracks


class Copyright:
    def __init__(self, text, type) -> None:
        self.text = text
        self.type = type

    def __str__(self) -> str:
        return f"{self.text}"


class Image:
    def __init__(self, height, url, width):
        self.height = height
        self.url = url
        self.width = width

    def __str__(self) -> str:
        return f"{self.height} x {self.width}"
