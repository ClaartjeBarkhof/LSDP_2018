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

def time_to_string(time):
    h = time.time().hour
    m = time.time().minute
    return('%s'%h + ':%s'%m)

def find_last_today(opties):
    for index, optie in enumerate(opties):
        date1 = optie.find('GeplandeVertrekTijd').text[0:10]
        date2 = opties[index+1].find('GeplandeVertrekTijd').text[0:10]
        if date1 != date2:
            return optie
    return opties[-1]

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

        vertrektijd = time_to_string(vertrektijd)
 #       print(vertrektijd.time().hour + vertrektijd.time().minute)
        return ('the next leaving train is the ' + treinsoort +' to ' + eindbest +' at ' + vertrektijd + ' from platform ' +  spoor)


#Dit doet het als de tijd 'LAST' is. Moet nog gebeuren voor echte tijdswaarden.
class GetTrainTriple(DynamicMap):
    def __init__(self, config):
        DynamicMap.__init__(self, config)

    def map_value(self, bot, clientid, input_value):
        return self.triple_to_train(input_value)

    def triple_to_train(self, name):
        origin, time, destination, arrival = name.split(' , ')
        if (time == 'LAST'):
            time = '2018-03-13T23:50'
        ns = 'https://webservices.ns.nl/'
        global aut
        if arrival == 'true':
            time += '&Departure=false'
        r = requests.get(ns + 'ns-api-treinplanner?toStation=' + destination + '&fromStation=' + origin + '&dateTime=' + time, auth=aut)
        tree = ElementTree.fromstring(r.text)
        opties = tree.findall('ReisMogelijkheid')
        optie = find_last_today(opties)

        overstappen = optie.find('AantalOverstappen').text
        reistijd = optie.find('GeplandeReisTijd').text
        vertrektijd = optie.find('GeplandeVertrekTijd').text
        actuelevertrektijd = optie.find('ActueleVertrekTijd').text
        aankomsttijd = optie.find('GeplandeAankomstTijd').text
        actueleaankomsttijd = optie.find('ActueleAankomstTijd').text
        vertrektijd = datetime.strptime(vertrektijd, '%Y-%m-%dT%H:%M:%S%z')
        vertrektijd = time_to_string(vertrektijd)

        output='tijd: '+vertrektijd+' .'
        counter = 0
        for reisdeel in optie.findall('ReisDeel'):
            spoor = reisdeel.find('ReisStop').find('Spoor').text
            # print("SPOORTJE")
            # print(spoor)
            if counter == 0:
                # print('vertrek van ' + origin + ' op spoor: ' + spoor)
                output += 'vertrek van ' + origin + ' op spoor: ' + spoor
            if counter > 0:
                overstap = reisdeel.find('ReisStop').find('Naam').text
                # print('overstappen op ' + overstap + ' op spoor: ' + spoor)
                output += ', overstappen op ' + overstap + ' op spoor: ' + spoor
            counter += 1
        output += '.'
        return output
