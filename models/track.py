class Track:
    def __init__(
        self,
        artists,
        available_markets,
        disc_number,
        duration_ms,
        explicit,
        external_urls,
        href,
        id,
        is_local,
        name,
        preview_url,
        track_number,
        type,
        uri,
        album=None,
        external_ids=None,
        popularity=None,
    ) -> None:
        self.album = album
        self.artists = artists
        self.available_markets = available_markets
        self.disc_number = disc_number
        self.duration_ms = duration_ms
        self.explicit = explicit
        self.external_ids = external_ids
        self.external_urls = external_urls
        self.href = href
        self.id = id
        self.is_local = is_local
        self.name = name
        self.popularity = popularity
        self.preview_url = preview_url
        self.track_number = track_number
        self.type = type
        self.uri = uri

    def __str__(self):
        return f"{', '.join([artist.name for artist in self.artists])} - {self.name}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"
