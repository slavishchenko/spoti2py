.. spoty2py documentation master file, created by
   sphinx-quickstart on Tue Mar 28 10:24:55 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to spoty2py's documentation!
====================================

**spoty2py** is a simple, bare bones wrapper for the Spotify Web API.
It offers a *simple*, *intuitive* and more *pythonic* way to interact with the Spotify API.
For official docs, visit https://developer.spotify.com/documentation/web-api

.. note::

   This project is under active development.

.. currentmodule:: client

Client
======
.. autoclass:: Client

Search 
======

To perform Spotify search, you can use the ``client.Client.search()`` function:

.. automethod:: Client.search
.. autoclass:: models.Search
.. autoexception:: exceptions.NoSearchQuery


.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
