import requests
import pprint
from xml.etree import ElementTree
from datetime import datetime
from login import aut

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

print(first_leaving_train('amsterdam centraal', aut))
