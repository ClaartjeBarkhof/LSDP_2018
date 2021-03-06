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
import datetime
import re
import pprint
from xml.etree import ElementTree
from datetime import datetime, timedelta
from login import aut
from programy.utils.text.dateformat import DateFormatter
import pdb

'''
Converts time object to time in type string
'''
def time_to_string(time):
    h = time.time().hour
    m = time.time().minute
    return('%s'%h + ':%s'%m)

'''
Finds the last travel advice from a list of
options for this day.
'''
def find_last_today(opties):
    for index, optie in enumerate(opties):
        date1 = optie.find('GeplandeVertrekTijd').text[0:10]
        date2 = opties[index+1].find('GeplandeVertrekTijd').text[0:10]
        if date1 != date2:
            return optie
    return opties[-1]

'''
Returns an appropriate date time string,
based on a given time and date (which can be set to
tomorrow or unknown). If Date is set to unknown, we'll
assume the user wishes to travel today.
'''
def convert_time(time, date, middag_avond):
    if (date == 'TOMORROW'):
        date = date = '2018-' + DateFormatter().date_representation()[0:2] + '-' + DateFormatter().date_representation()[3:5]
        day = int(date[8:10])
        tomorrow = day + 1
        date = date = '2018-' + DateFormatter().date_representation()[0:2] + '-' + str(tomorrow)
    else:
        date = '2018-' + DateFormatter().date_representation()[0:2] + '-' + DateFormatter().date_representation()[3:5]
    if (len(time) == 1) and ('MIDDAG' in middag_avond):
            time = int(time) + 12
            time = 'T' + str(time) + ':00'
            time = date + time
    if (len(time) == 1):
        time = 'T0' + time + ':00'
        time = date + time
    if (len(time) == 2):
        time = 'T' + time + ':00'
        time = date + time
    elif ":" in time:
        if len(time) == 5:
            time = date + 'T' + time
        if len(time) == 4:
            time = 'T0' + time
            time = date + time
    return time

'''
This class implements the GetTrain dynamic map. This works
with a station as input.
'''
class GetTrain(DynamicMap):

    def __init__(self, config):
        DynamicMap.__init__(self, config)

    def map_value(self, bot, clientid, input_value):
        return self.first_leaving_train(input_value)

    '''
    Takes a station as input and outputs the first
    leaving train.
    '''
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
        return ('the next leaving train is the ' + treinsoort +' to ' + eindbest +' at ' + vertrektijd + ' from platform ' +  spoor)


'''
This class implements the GetTrainTriple dynamic map. This works
with a destination, origin and time as a minimal input.
'''
class GetTrainTriple(DynamicMap):
    def __init__(self, config):
        DynamicMap.__init__(self, config)

    def map_value(self, bot, clientid, input_value):
        return self.triple_to_train(input_value)

    def triple_to_train(self, name):
        '''
        Origin (departure station), time (time of departure or arrival),
        destination (destination station), arrival (true if an arrival time is given),
        last (true if the last train is requested), date (can be set to tomorrow) 
        '''
        origin, time, destination, arrival, last, date, middag_avond = name.split(' , ')

        if (last == 'TRUE'):
            date = '2018-' + DateFormatter().date_representation()[0:2] + '-' + DateFormatter().date_representation()[3:5]
            time = date + 'T23:50'
        elif any(char.isdigit() for char in time) == False:
            return "Please enter a valid sentence."
        else:
            time = convert_time(time, date, middag_avond)

        ns = 'https://webservices.ns.nl/'
        global aut
        arrivaltext = ''
        if arrival == 'TRUE':
            arrivaltext += '&Departure=false'
        r = requests.get(ns + 'ns-api-treinplanner?toStation=' + destination + '&fromStation=' + origin + '&dateTime=' + time + arrivaltext, auth=aut)
        tree = ElementTree.fromstring(r.text)
        opties = tree.findall('ReisMogelijkheid')
        output = ''
        if date == 'TOMORROW':
            output += 'For tomorrow, t'
        else:
            output += 'T'

        if last == 'TRUE':
            opties = [find_last_today(opties)]
            output += 'he last option is:\n'
        else:
            output += 'hese are your options:\n'


        # filter out the options that are more than 10 minutes before the given time
        timeobj = datetime.strptime(time + ':00+0100', '%Y-%m-%dT%H:%M:%S%z')
        newoptions = []
        for optie in opties:
            if arrival == 'TRUE':
                newtime = datetime.strptime(optie.find('ActueleAankomstTijd').text, '%Y-%m-%dT%H:%M:%S%z')
                if ((timeobj <= newtime) and abs(timeobj - newtime) <= timedelta(minutes=40)) or ((timeobj >= newtime) and abs(newtime - timeobj) <= timedelta(minutes=30)):
                    newoptions.append(optie)
            else:
                newtime = datetime.strptime(optie.find('ActueleVertrekTijd').text, '%Y-%m-%dT%H:%M:%S%z')
                if (timeobj <= newtime) or abs(timeobj - newtime) <= timedelta(minutes=10):
                    newoptions.append(optie)
        opties = newoptions
        if len(opties) == 0:
            return("Oh no! There are no connections from " + origin + " to " + destination + " around " + time[-5:] +\
                   "... I do hope you have some proper shoes for the walk!")

        # sums up the top 4 options
        for index, optie in enumerate(opties):
            if index < 4:
                index += 1
                overstappen = optie.find('AantalOverstappen').text
                reistijd = optie.find('GeplandeReisTijd').text
                vertrektijd = optie.find('GeplandeVertrekTijd').text
                actuelevertrektijd = optie.find('ActueleVertrekTijd').text
                aankomsttijd = optie.find('GeplandeAankomstTijd').text
                actueleaankomsttijd = optie.find('ActueleAankomstTijd').text
                vertrektijd = datetime.strptime(vertrektijd, '%Y-%m-%dT%H:%M:%S%z')
                vertrektijd = time_to_string(vertrektijd)

                if last != 'TRUE':
                    output += 'Option ' + str(index) + ' (travel time ' + reistijd + '):\n'
                counter = 0
                for reisdeel in optie.findall('ReisDeel'):
                    stops = reisdeel.findall('ReisStop')
                    spoor = stops[0].find('Spoor').text
                    tijd = stops[0].find('Tijd').text[11:16]
                    naam = stops[0].find('Naam').text

                    if counter == 0:
                        output += ' ' + tijd + ' from ' + naam + ' at platform ' + spoor + '\n'
                    if counter > 0:
                        output += ' ' + tijd +' change at ' + naam + ' to platform ' + spoor + '\n'
                    counter += 1

                output += ' ' + stops[-1].find('Tijd').text[11:16] + ' arrival at ' + stops[-1].find('Naam').text + '\n\n'
        return output
