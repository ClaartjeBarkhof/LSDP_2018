"""
Copyright (c) 2016-17 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from programy.dynamic.maps.map import DynamicMap

import requests
import pprint
from xml.etree import ElementTree
from datetime import datetime
from login import aut

class GetTrain(DynamicMap):

    def __init__(self, config):
        DynamicMap.__init__(self, config)



    def map_value(self, bot, clientid, input_value):
        return self.first_leaving_train(input_value)

    def first_leaving_train(self, name):
        ns = 'https://webservices.ns.nl/'
        global aut
        r = requests.get(ns + 'ns-api-avt?station=' + name, auth=aut)
        tree = ElementTree.fromstring(r.text)
        train = tree.find('VertrekkendeTrein')
        treinsoort = train.find('TreinSoort').text
        eindbest = train.find('EindBestemming').text
        spoor = train.find('VertrekSpoor').text
        vertrektijd = train.find('VertrekTijd').text
        vertrektijd = datetime.strptime(vertrektijd, '%Y-%m-%dT%H:%M:%S%z')
        
 #       print(vertrektijd.time().hour + vertrektijd.time().minute)
        h = vertrektijd.time().hour
        m = vertrektijd.time().minute
        return ('the next leaving train is the ' + treinsoort +' to ' + eindbest +' at ' + '%s'%h + ':%s'%m + ' from platform ' +  spoor)