Twitter Tracker |build-status|
==============================

A program to capture GPS coordinates from tweets and plot them on a map.

A Javascript file will be generated for the map using Google Maps API.

Usage

    python server.py

* You can specify either scren names, or hashtags(without the #) to watch
  http://localhost:8080/?hashtag=TheDress

Dependencies
============
* python 2.7
* tweepy
* jinja2
* Users tweeting with location enabled


Screenshot
==========
![alt text](sampleImage.png "Sample Image")



.. |build-status| image:: https://travis-ci.org/cawest1221/Twitter_Tracker.svg?branch=master
   :target: https://travis-ci.org/cawest1221/Twitter_Tracker
   :alt: Build status
