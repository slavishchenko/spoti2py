# spoti2py

**spoti2py** is a simple, bare bones, asynchronous wrapper for the Spotify Web API.
It offers _simple_, _intuitive_ and more _pythonic_ way to interact with the [Spotify Web API](https://developer.spotify.com/documentation/web-api).

---

## Documentation
The full documentation can be viewed [here](https://spoti2py.readthedocs.io/en/latest/).

## Index

- [Installation](#installation)

- [Getting started](#getting-started)

- [Examples](#examples)


## Installation

To use **spoti2py**, clone the repository and install it with pip:

```console
(.venv) $ git clone https://github.com/slavishchenko/spoti2py spotify
        $ cd spotify
        $ pip install .
```

## Getting started

**NOTE**: To use this library, you’ll need a Spotify account (free or premium), and you’ll also need to [create an app](https://developer.spotify.com/documentation/web-api/tutorials/getting-started#create-an-app) in order to get your client credentials.

First, instantiate `spoti2py.client.Client` class with your _client_id_ and _client_secret_.

```python
from spoti2py.client import Client

client = Client(client_id="your client id", client_secret="your client secret")
```

Now you can start exploring what Spotify Web API has to offer.

## Examples

#### Search for a song and get audio analysis

```python
import asyncio
import os

from spoti2py.client import Client


client_id = "your client id"
client_secret = "your client secret"

client = Client(client_id, client_secret)

async def main():
   async with client as c:
      search = await c.search(query="master of puppets", limit=5)
      songs = search.items
      analysis = await asyncio.gather(
            *[asyncio.create_task(c.get_audio_analysis(song.id)) for song in songs]
      )
      return zip(songs, analysis)

response = client.loop.run_until_complete(main())
for song, analysis in response:
    print(f'{song.name} is played at {analysis.tempo} BPM')
```

#### Get full artist details

```python
import asyncio
import os

from spoti2py.client import Client


client_id = "your client id"
client_secret = "your client secret"
artist_id = "1vCWHaC5f2uS3yhpwWbIA6"

client = Client(client_id, client_secret)


async def get_full_artist_details():
   async with client as c:
      artist, albums, top_tracks, related_artists = await asyncio.gather(
            c.get_artist(id=artist_id),
            c.get_artists_albums(id=artist_id, limit=5),
            c.get_artists_top_tracks(id=artist_id),
            c.get_related_artists(id=artist_id),
      )
      return artist, albums, top_tracks, related_artists


artist, albums, top_tracks, related_artists = client.loop.run_until_complete(
   get_full_artist_details()
)
```
