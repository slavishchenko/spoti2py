class Artist:
    def __init__(self, external_urls, href, id, name, type, uri) -> None:
        self.external_urls = external_urls
        self.href = href
        self.id = id
        self.name = name
        self.type = type
        self.uri = uri

    def __str__(self) -> str:
        return f"{self.name}"
