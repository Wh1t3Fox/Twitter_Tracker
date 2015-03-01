#!/usr/bin/env python

from tweepy import OAuthHandler
from ConfigParser import SafeConfigParser
from server import CSRF
import tweepy
import pygmaps
import json
import argparse
import threading
import requests


parser = SafeConfigParser()
parser.read('config.ini')
auth= OAuthHandler(parser.get('twitter', 'CONSUMER_KEY'), parser.get('twitter', 'CONSUMER_SECRET'))
auth.set_access_token(parser.get('twitter', 'ACCESS_KEY'),parser.get('twitter', 'ACCESS_SECRET'))

#Initialize the map
gmap = pygmaps.maps()

#Coords for drawing our lines on the map
user_enabled = False
path = []
legend = []
colors = []

#Listener to received the stream
class Listener(tweepy.StreamListener):

    def __init__(self):
        self.draw_map()

    #Function is called on new tweet
    def on_data(self, data):
        decoded = json.loads(data)

        #If there coords, add them to the map
        if decoded['coordinates']:

            #Print the tweet
            #print('@{}: {}'.format(decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore')))
            #print('')
            payload = {}
            payload['data'] = {}
            payload['data']['CSRF_token'] = CSRF
            payload['data']['user'] = "@"+decoded['user']['screen_name']
            r = requests.post('http://localhost:8080/request', params=payload)
            '''
            title = "@"+decoded['user']['screen_name']
            gmap.addpoint(decoded['coordinates']['coordinates'][1], decoded['coordinates']['coordinates'][0], '#FF0000', title)
            if user_enabled:
                #pop off the color in order to add more coords
                try:
                    gmap.paths[0].pop(-1)
                except:
                    pass
                path.append((decoded['coordinates']['coordinates'][1], decoded['coordinates']['coordinates'][0]))
                gmap.addpath(path, "#0000FF")
            '''
        return True

    #If an error occurs
    def on_error(self, status):
        pass
        #print("[-] ERROR {0}".format(status))

    def draw_map(self):
        self.thread = threading.Timer(30, self.draw_map)
        self.thread.start()
        gmap.draw(legend)
