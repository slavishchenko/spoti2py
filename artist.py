class Artist:
    def __init__(
        self,
        external_urls,
        href,
        id,
        name,
        type,
        uri,
        followers=None,
        genres=None,
        images=None,
        popularity=None,
    ) -> None:
        self.external_urls = external_urls
        self.href = href
        self.id = id
        self.name = name
        self.type = type
        self.uri = uri
        self.followers = followers
        self.genres = genres
        self.images = images
        self.popularity = popularity

    def __str__(self) -> str:
        return f"{self.name}"
