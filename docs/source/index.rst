.. spoti2py documentation master file, created by
   sphinx-quickstart on Tue Apr 11 15:51:52 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to spoti2py's documentation!
====================================

**spoti2py** is a simple, bare bones, asynchronous wrapper for the Spotify Web API.
It offers *simple*, *intuitive* and more *pythonic* way to interact with the `Spotify Web API`_.

.. _Spotify Web API: https://developer.spotify.com/documentation/web-api


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Installation
------------

To use **spoti2py**, clone the repository and install it with pip:

.. code-block:: console

   (.venv) $ git clone https://github.com/slavishchenko/spoti2py spotify
           $ cd spotify
           $ pip install .


Getting started
---------------

.. note:: 
   To use this library, you'll need a Spotify account (free or premium), and you'll also need to `create an app`_ in order to get your client credentials.

.. _create an app: https://developer.spotify.com/documentation/web-api/tutorials/getting-started#create-an-app

First, instantiate ``spoti2py.client.Client`` class with your *client_id* and *client_secret*.

.. code-block:: python

   from spoti2py.client import Client

   client = Client(client_id="your client id", client_secret="your client secret")

Now you can start exploring what Spotify Web API has to offer.

Examples 
========

Search for a song and get audio analysis
----------------------------------------
.. code-block:: python

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

   songs, analysis = client.loop.run_until_complete(main())
   print(songs, analysis)

Get full artist details
-----------------------
.. code-block:: python

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


API reference
=============

Methods
-------

.. automethod:: spoti2py.client.Client.search()
.. automethod:: spoti2py.client.Client.get_album()
.. automethod:: spoti2py.client.Client.get_album_tracks()
.. automethod:: spoti2py.client.Client.get_new_releases()
.. automethod:: spoti2py.client.Client.get_artist()
.. automethod:: spoti2py.client.Client.get_artists_albums()
.. automethod:: spoti2py.client.Client.get_artists_top_tracks()
.. automethod:: spoti2py.client.Client.get_related_artists()
.. automethod:: spoti2py.client.Client.get_track()
.. automethod:: spoti2py.client.Client.get_audio_analysis()
.. automethod:: spoti2py.client.Client.get_recommendations()


Models
------

.. automodule:: spoti2py.models
.. autoclass:: Search
.. autoclass:: Album
.. autoclass:: Track
.. autoclass:: Artist
.. autoclass:: AudioAnalysis
.. autoclass:: Recommendations


Exceptions
----------

.. automodule:: spoti2py.exceptions
.. autoexception:: NoSearchQuery
.. autoexception:: InvalidCredentials
.. autoexception:: InvalidItemType
.. autoexception:: SpotifyException

.. toctree::
   :maxdepth: 2
   :caption: Contents:



