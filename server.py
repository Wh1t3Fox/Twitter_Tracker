#!/usr/bin/env python
"""
Twitter Tracker
Author: Craig West
"""
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('templates'))
from tracker import *
from random import random
import binascii
import cherrypy
import threading
import os
import sys

CSRF = binascii.hexlify(os.urandom(32))

class Server(object):

    @cherrypy.expose
    def index(self, user=None, hashtag=None):
        global user_enabled
        global users
        global topics
        global legend

        cookie = cherrypy.response.cookie
        cookie['CSRF_token'] = CSRF
        if 'CSRF_token' not in cherrypy.session:
            cherrypy.session['CSRF_token'] = CSRF

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

        stream = tweepy.Stream(auth, Listener())
        stream.filter(follow=users, track=topics, async=True)

        tmpl = env.get_template('index.html')
        return tmpl.render(rand=random())


    @cherrypy.expose
    def request(self, data=None):
        if cherrypy.request.method != 'POST':
            raise cherrypy.HTTPRedirect('/')

        cherrypy.response.headers['Content-Type'] = 'text/plain'
        try:
            if 'CSRF_token' not in cherrypy.response.cookie:
                raise cherrypy.HTTPError(403, 'Missing CSRF Token')
            else:
                if cherrypy.response.cookie['CSRF_token'].value != data['CSRF_token']:
                    raise cherrypy.HTTPError(403)
        except Exception as e:
            print "[-] ERROR ", str(e)
            raise cherrypy.HTTPError(403)

        print "***********************************[+] POST ", data




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
        sys.exit()
