from .track import Track


class Recommendations:
    """
    Models Spotify's recommendations response

    :ivar tracks: A list of simplified Track objects
    :ivar seeds: A list of recommendation seed JSON objects.
    """

    def __init__(self, tracks: list[Track], seeds: list[dict]) -> None:
        self.tracks = tracks
        self.seeds = seeds

    def __repr__(self):
        return f"{self.__class__.__name__}({self.tracks})"
