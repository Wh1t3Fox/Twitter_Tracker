#!/usr/bin/env python
"""
Twitter Tracker
Author: Craig West
"""
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('templates'))
from tracker import *
from pygmaps import maps
from random import random
import cherrypy
import os


class Server(object):

    @cherrypy.expose
    def index(self, user=None, hashtag=None):
        global user_enabled
        global users
        global topics
        global legend
        if user:
            user_enabled = True
            users = [str(tweepy.API(auth).get_user(x).id) for x in args['user']]
            [legend.append("@"+x) for x in args['user']]
        else:
            users = []
        if hashtag:
            topics = [x for x in args['topic']]
            [legend.append("#"+x) for x in args['topic']]
        else:
            topics = []

        #l = Listener()
        #stream = tweepy.Stream(auth, l)
        #stream.filter(follow=users, track=topics)
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
    cherrypy.quickstart(Server(), '/', conf)
