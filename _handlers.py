def exception_handler(e):
    """Parses exception object and returns exception messagge or None"""
    response = e.response
    try:
        json_response = response.json()
        error = json_response.get('error', {})
        msg = error.get('message')
    except ValueError:
        msg = response.text or None
    finally:
        return msg