class Search:
    def __init__(self, href, items, limit, next, offset, previous, total) -> None:
        self.href = href
        self.items = items
        self.limit = limit
        self.next = next
        self.offset = offset
        self.previous = previous
        self.total = total

    def __str__(self):
        return f'Search results for "{self.href}"'
