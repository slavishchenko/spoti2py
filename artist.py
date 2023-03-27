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

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"


class Followers:
    def __init__(self, href, total) -> None:
        self.href = href
        self.total = total

    def __str__(self) -> str:
        return f"{self.total}"
