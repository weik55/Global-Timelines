#!/usr/bin/env python
#
# this is a modified version of the Google App Engine Tutorial
import json
import logging
import re

import wikipedia

import jinja2
import webapp2, os, urllib


def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

TEST_PAGE = 'Timeline_of_ancient_history'

def getWikiData(page):
    timeline = wikipedia.page(page)
    
    content = timeline.content.encode('utf-8').rstrip().split('\n')
    #print timeline.content.encode('utf-8')
    
    regexp = re.compile(r'^[0-9|c. ]+( BC:|:)')
    container = {}
    for line in content:
        if regexp.search(line) is not None:
            if line.startswith('c. '):
                line = line.replace('c. ', '')
            lineContents = line.split(':')
            if lineContents[0].find(' BC') != -1:
                lineContents[0] = '-' + lineContents[0]
                lineContents[0] = lineContents[0].replace(' BC', '')
            container[int(float(lineContents[0]))] = lineContents[1].decode('utf-8')
    
    sorted(container)
    logging.info(container)
    return container

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template_values={}
        template = JINJA_ENVIRONMENT.get_template('index.html')
        
        template_values['val'] = getWikiData(TEST_PAGE)
        #Modifying template here
        #vals = {}
        #vals['timeline'] = ""
        #timeline = ""
        
        #for x in range(0, 30):
        #    timeline += "<div>" + str(x) + "</div>\n"
        
        #vals['timeline'] = timeline
        self.response.write(template.render(template_values).encode( "utf-8" ))



application = webapp2.WSGIApplication([('/', MainHandler)], debug=True)