class Image:
    def __init__(self, height, url, width):
        self.height = height
        self.url = url
        self.width = width

    def __str__(self) -> str:
        return f"{self.height} x {self.width}"
