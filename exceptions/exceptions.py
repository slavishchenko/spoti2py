class NoSearchQuery(Exception):
    """Raised if no search query is provided"""

    pass


class InvalidCredentials(Exception):
    """Raised if invalid credentials are passed into client class"""

    pass


class InvalidItemType(Exception):
    """Raise if invalid item_type is provided to parse_json function"""

    pass
