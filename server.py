#!/usr/bin/env python
"""
Twitter Tracker
Author: Craig West
"""
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('templates'))
from tracker import *
from random import random
import cherrypy
import threading
import os
import sys

l = None

class Server(object):

    @cherrypy.expose
    def index(self, user=None, hashtag=None):
        global user_enabled
        global users
        global topics
        global legend

        if user:
            user_enabled = True
            users = [str(tweepy.API(auth).get_user(x).id) for x in user.split(',')]
            [legend.append("@"+x) for x in user.split(',')]
        else:
            users = []
        if hashtag:
            topics = [x for x in hashtag.split(',')]
            [legend.append("#"+x) for x in hashtag.split(',')]
        else:
            topics = []


        l = Listener()
        stream = tweepy.Stream(auth, l)
        stream.filter(follow=users, track=topics, async=True)

        tmpl = env.get_template('index.html')
        return tmpl.render(rand=random())


if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }
    try:
        cherrypy.quickstart(Server(), '/', conf)
    except KeyboardInterrupt:
        l.thread.cancel()
        sys.exit()
