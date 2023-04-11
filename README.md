# spoti2py

**spoti2py** is a simple, bare bones, asynchronous wrapper for the Spotify Web API.
It offers _simple_, _intuitive_ and more _pythonic_ way to interact with the [Spotify Web API](https://developer.spotify.com/documentation/web-api).

---

## Index

- [Installation](#installation)

- [Getting started](#getting-started)

- [Examples](#examples)

- [API Refrence](#api-reference)

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

##### Search for a song and get audio analysis

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

##### Get full artist details

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

## API reference

#### _async_ Client.search()

Get Spotify catalog information about albums, artists and tracks
that match a keyword string.

- **Parameters**

  - **query** – required - Your search query.

  - **search_type** – Optional item type to search accross. Defaults to “track”.

  - **limit** – Maximum number of results to return. >= 0 <= 50. Default is 1.

- **Raises**

  **exceptions.NoSearchQuery** – If no query is provided.

- **Returns**

  `Search`

- **Return type**

  object

#### _async_ Client.get_album()

Get Spotify catalog information for a single album.

- **Parameters**

  **id** – The Spotify ID of the album. Required.

- **Returns**

  `Album`

- **Return type**

  object

#### _async_ Client.get_album_tracks()

Get Spotify catalog information about an album’s tracks.
Optional parameters can be used to limit the number of tracks returned.

- **Parameters**

  - **id** – The Spotify ID of the album. Required.

  - **market** – An ISO 3166-1 alpha-2 country code.
    If a country code is specified, only content that is available in that market will be returned.
    If a valid user access token is specified in the request header,
    the country associated with the user account will take priority over this parameter.
    Default: us.

  - **limit** – The maximum number of items to return. Default: 20. Min: 1. Max: 50.

- **Returns**

  list[`Track`]

- **Return type**

  list

#### _async_ Client.get_new_releases()

Get a list of new album releases featured in Spotify

- **Parameters**

  - **country** – A country: an ISO 3166-1 alpha-2 country code.
    Provide this parameter if you want the list of returned items to be relevant to a particular country.
    If omitted, the returned items will be relevant to all countries.

  - **limit** – The maximum number of items to return. Default: 20. Min: 1. Max: 50.

- **Returns**

  list[`Album`]

#### _async_ Client.get_artist()

Get Spotify catalog information for a single artist identified by their unique Spotify ID.

- **Parameters**

  **id** – The Spotify ID of the artist. Required.”

- **Returns**

  `Artist`

- **Return type**

  object

#### _async_ Client.get_artists_albums()

Get Spotify catalog information about an artist’s albums.

- **Parameters**

  - **id** – The Spotify ID of the artist.

  - **include_groups** – A list of keywords that will be used to filter the response.
    If not supplied, all album types will be returned.
    Valid values: album, single, appears_on, compilation.

  - **limit** – The maximum number of items to return. Default: 20. Min: 1. Max. 50.

- **Returns**

  List[`Album`]

- **Return type**

  List[object]

#### _async_ Client.get_artists_top_tracks()

Get Spotify catalog information about an artist’s top tracks by country.

- **Parameters**

  - **id** – The Spotify ID of the artist.

  - **market** – An ISO 3166-1 alpha-2 country code.
    If a country code is specified, only content that is available in that market will be returned.
    If a valid user access token is specified in the request header,
    the country associated with the user account will take priority over this parameter.
    Default: us.

- **Returns**

  list[`Track`]

- **Return type**

  list[object]

#### _async_ Client.get_related_artists()

Get Spotify catalog information about artists similar to a given artist.

- **Parameters**

  **id** – The Spotify ID of the artist.

- **Returns**

  list[`Artist`]

- **Type**

  list

#### _async_ Client.get_track()

Get Spotify catalog information for a single track identified by its unique Spotify ID.

- **Parameters**

  **id** – The Spotify ID of the track. Required.”

- **Returns**

  `Track`

- **Return type**

  object

#### _async_ Client.get_audio_analysis()

Get low-level audio analysis for a track in the Spotify catalog.
The audio analysis describes the track’s structure and musical content, including rhythm, pitch, and timbre.

- **Parameters**

  **id** – The Spotify ID of the track. Required.”

- **Returns**

  `AudioAnalysis`

- **Return type**

  object

#### _async_ Client.get_recommendations()

Recommendations are generated based on the available information or a given seed entity and matched against similar artists and tracks.
For artists and tracks that are very new or obscure there might not be enough data to generate a list of tracks.

- **Parameters**

  - **limit** – The target size of the list of recommended tracks.
    Default: 20. Minimum: 1. Maximum: 100.

  - **seed_artists** – A list of Spotify IDs for seed artists.

  - **seed_genres** – A list of any genres in the set of available genre seeds.
    available_genre_seeds is an attribute of the Client class.

  - **seed_tracks** – A list of Spotify IDs fpr a seed track.

Up to 5 seed values may be provided in any combination of seed_artists, seed_tracks and seed_genres.
At least 1 is required!

- **Returns**

  `Recommendations`

- **Return type**

  object
