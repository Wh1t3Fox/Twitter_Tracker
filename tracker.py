#!/usr/bin/env python

import pygmaps
import tweepy
import json
import argparse
import threading

#Twitter Keys
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

#Initialize the map
gmap = pygmaps.maps('35.6500', '-97.4667', 5)

#Coords for drawing our lines on the map
path = []
legend = []

#Listener to received the stream
class Listener(tweepy.StreamListener):

    def __init__(self):
        self.draw_map()
    
    #Function is called on new tweet
    def on_data(self, data):
        decoded = json.loads(data)
        
        #Print the tweet
        print '@%s: %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore'))
        print ''
        
        #If there coords, add them to the map
        if decoded['coordinates']:
            #pop off the color in order to add more coords
            try:
                gmap.paths[0].pop(-1)
            except:
                pass
            path.append((decoded['coordinates']['coordinates'][1], decoded['coordinates']['coordinates'][0]))
            gmap.addpoint(decoded['coordinates']['coordinates'][1], decoded['coordinates']['coordinates'][0], '#FF0000', "@"+decoded['user']['screen_name'])
            gmap.addpath(path, "#0000FF")
        
        return True
    
    #If an error occurs
    def on_error(self, status):
        print status
        
    def draw_map(self):
        thread = threading.Timer(30, self.draw_map)
        thread.start()
        gmap.draw(legend)



if __name__ == "__main__":
    try:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
    
        parser = argparse.ArgumentParser(description="Track a User or Topic with GPS")
        parser.add_argument('-u', '--user', nargs='+', type=str, help="Twitter username")
        parser.add_argument('-t', '--topic', nargs='+', type=str, help="Hashtags to follow")
        args = vars(parser.parse_args())
        
        #If there are users to follow get their user id
        if args['user']:
            users = [str(tweepy.API(auth).get_user(x).id) for x in args['user']]
            [legend.append("@"+x) for x in args['user']]
        else:
            users = []
        if args['topic']:
            topics = [x for x in args['topic']]
            [legend.append("#"+x) for x in args['topic']]
        else:
            topics = []

        
        #Setup the stream with the arguments
        l = Listener()
        stream = tweepy.Stream(auth, l)
        stream.filter(follow=users, track=topics)
    except KeyboardInterrupt:
        thread.cancel()
        print '\nGoodbye!'
    
    
