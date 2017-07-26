'''
Created on Dec 11, 2014

@author: Wei
'''

import json
import re

import wikipedia


def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

timeline = wikipedia.page("Timeline_of_ancient_history")

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
        container[int(float(lineContents[0]))] = lineContents[1]

sorted(container)
print pretty(container)
