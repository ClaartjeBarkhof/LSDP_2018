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

from programy.dynamic.variables.variable import DynamicVariable

from programy.utils.text.dateformat import DateFormatter

import requests
import pprint
from xml.etree import ElementTree
from datetime import datetime
from login import aut

class GetTrain(DynamicVariable):

    def __init__(self, config):
        DynamicVariable.__init__(self, config)

    def get_value(self, bot, clientid, value=None):
        print("TEST",value)
        global aut
        if value != None:
        	return self.first_leaving_train(value, aut)

    def first_leaving_train(name, aut):
	    ns = 'https://webservices.ns.nl/'
	    r = requests.get(ns + 'ns-api-avt?station=' + name, auth=aut)
	#     print(r.text)
	    tree = ElementTree.fromstring(r.text)
	    train = tree.find('VertrekkendeTrein')
	    treinsoort = train.find('TreinSoort').text
	    eindbest = train.find('EindBestemming').text
	    spoor = train.find('VertrekSpoor').text
	    vertrektijd = train.find('VertrekTijd').text
	    vertrektijd = datetime.strptime(vertrektijd, '%Y-%m-%dT%H:%M:%S%z')
	    return 'The next leaving train is the ' + treinsoort + \
	          ' to ' + eindbest + \
	          ' at ' + vertrektijd.time().isoformat(timespec='minutes') + \
	          ' from platform ' +  spoor