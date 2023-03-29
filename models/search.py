class Search:
    """
    Spotify search response.

    :param href: A link to the Web API endpoint returning the full result of the request.
    :param items: List of objects
    :param limit: The maximum number of items in the response (as set in the query or by default).
    :param next: URL to the next page of items or None.
    :param offset: The offset of the items returned (as set in the query or by default).
    :param previous: URL to the previous page of items or None.
    :param total: The total number of items available to return.
    """

    def __init__(
        self,
        href: str,
        items: list[object],
        limit: int,
        next: str | None,
        offset: int,
        previous: str | None,
        total: int,
    ) -> None:
        self.href = href
        self.items = items
        self.limit = limit
        self.next = next
        self.offset = offset
        self.previous = previous
        self.total = total

    def __str__(self):
        return f"{self.items}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.items})"
