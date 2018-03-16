====================================

OPDRACHT 3 - REISPLANNER CHATBOT

====================================
====================================

ARIE SOETEMAN		- 	11060565
CLAARTJE BARKHOF	-	11035129
LUCAS FIJEN			- 	10813268

====================================

OVER DEZE CHATBOT

Deze bestanden vormen samen een implementatie van een chatbot die op basis van AIML en interactie met een NS API reisadvies kan geven in een conversatie.

Program Y is een python programma dat AIML 2.0. Interpreteert en zo een chatbot implementeert. We hebben voor deze interpreteerder gekozen omdat deze zeer flexibel is. Bovendien heeft AIML 2.0. functionaliteiten die eerdere, veel gebruikte, versies niet hebben. De functionaliteit waar het meeste gebruik van is gemaakt, is de dynamic map. Dit is een manier om een waarde gegeven in de conversatie toe te wijzen aan een bepaalde output. Een static map doet dit aan de hand van een tekstbestand, waarin key-value paren staan opgeslagen. Een dynamic map daarentegen doet dit aan de hand van een python object. In andere woorden: een dynamic map converteerd een waarde naar een nieuwe waarde met behulp van een (zelf geschreven) algoritme. In onze implementatie is de input die wordt gegeven aan de dynamic map de informatie voor een op te vragen reisadvies (de output). Deze informatie wordt uit de conversatie gehaald.

Om deze chatbot (‘mybot’) te gebruiken, moet het bestand console.sh worden uitgevoerd. Het is belangrijk dat de requirements voor het gebruik van Program-Y zijn geïnstalleerd. Deze zijn te installeren met behulp van requirements.txt. De bot en zijn benodigde files zijn gedefinieerd in config.yaml. De AIML die we hebben geschreven staat opgeslagen in mybot.aiml. We hebben tevens een set aangemaakt: stations.txt. Ook hebben we een dynamic map aangemaakt: train.py. Zoals eerder aangegeven gebruiken we voor onze implementatie gebruik van de NS API (www.ns.nl/reisinformatie/ns-api). In login.py staan authorisatie gegevens om deze te kunnen gebruiken. Hieronder staan alle belangrijke, benodigde en/of gewijzigde files met relatieve paden (vanaf de aangeleverde directory) aangegeven.

/mybot/console.sh
/program-y/requirements.txt
/mybot/config.yaml
/mybot/aiml/mybot.aiml
/mybot/sets/stations.txt
/program-y/src/programy/dynamic/maps/train.py
/program-y/src/programy/clients/login.py

====================================

FUNCTIONALITEITEN

De chatbot kan gebruikt worden om op een natuurlijke wijze reisinformatie (gebaseerd op echte data) uit te vragen. De chatbot antwoord op vragen over de verschillende reisopties vanaf een specifieke plek. Ook kan de chatbot worden gebruikt als reisplanner. Wanneer een gebruiker een beginpunt, een eindpunt, en een ankomsttijd of vertrektijd geeft, geeft de chatbot reisopties.  Dit blijkt uit het volgende voorbeeld:

Wanneer de chatbot informatie mist vraagt hij de gebruiker naar deze informatie.
User: 	i want to go from rotterdam to almere at 14:20

Bot:	These are your options:
		Option 1 (travel time 1:06):
		 14:11 from Rotterdam Centraal at platform 11
		 14:48 change at Schiphol Airport to platform 1-2
		 15:17 arrival at Almere Centrum

		Option 2 (travel time 1:20):
		 14:27 from Rotterdam Centraal at platform 9
		 15:47 arrival at Almere Centrum

		Option 3 (travel time 1:03):
		 14:28 from Rotterdam Centraal at platform 11
		 15:04 change at Schiphol Airport to platform 1-2
		 15:31 arrival at Almere Centrum

		Option 4 (travel time 1:06):
		 14:41 from Rotterdam Centraal at platform 11
		 15:18 change at Schiphol Airport to platform 1-2
		 15:47 arrival at Almere Centrum


Wanneer informatie mist kan de chatbot naar deze informatie vragen:

>>> i want to go to Rotterdam
Where do you want to depart from?
>>> almere
At what time do you want to leave?
>>> 14:20
These are your options:
Option 1 (travel time 1:07):
 14:12 from Almere Centrum at platform 1
 14:53 change at Schiphol Airport to platform 5-6
 15:19 arrival at Rotterdam Centraal

Option 2 (travel time 1:21):
 14:12 from Almere Centrum at platform 1
 15:33 arrival at Rotterdam Centraal

Option 3 (travel time 1:01):
 14:29 from Almere Centrum at platform 1
 15:04 change at Schiphol Airport to platform 5-6
 15:30 arrival at Rotterdam Centraal

Option 4 (travel time 1:19):
 14:29 from Almere Centrum at platform 1
 15:15 change at Leiden Centraal to platform 8b
 15:48 arrival at Rotterdam Centraal
>>> 

De chatbot controleert of de gebruiker correcte informatie geeft (bestaande stations en tijden) en vraagt wanneer nodig naar herformulering.
====================================
EXTRA EIGENSCHAP: PROSODISCHE INFORMATIE

In het hypothetische geval dat de chatbot ook gesproken tekst zou kunnen verwerken, zou er prosodische informatie opgeslagen kunnen worden. Deze prosodische informatie kan helpen zinnen van de gebruiker te disambigueren. Dit kan op verschillende manieren. Het kan bijvoorbeeld gaan om een verschil in het ontleden (parsen) van een zin. Een ander voorbeeld is het helpen herkennen van een verschil in nuance of doel van de tekst van de gebruiker. We zullen van allebei deze twee manieren om een zin te disambigueren met behulp van prosodie een voorbeeld geven.

Hoe een zin door de bot ontleed wordt maakt uit voor een goede interpretatie van een zin. Omdat een station uit meerdere woorden (tokens) kan bestaan (‘Amsterdam Centraal’), kan de bot niet zeker zijn van wanneer de woorden bij elkaar horen en samen de naam van een station vormen of wanneer de woorden los zijn en het tweede woord bijvoorbeeld een tijdsaanduiding is. Onderstaande zinnen illustreren dit. 

I want to travel to [Amsterdam Centraal]p
I want to travel to [Muiderpoort]p [tomorrow]t
I want to travel to [Amsterdam Centraal]p [tomorrow]t

Wanneer er een overgang is van plaats- naar een tijdsbepaling kan er een bepaalde mate van pauze worden herkend (zin 2). Deze pauze is meer aanwezig dan wanneer meerdere woorden bijvoorbeeld samen tot een plaatsbepaling horen (zin 1). Wanneer deze pauze opgeslagen (‘—’) is als informatie vanuit spraak, kan de zin op de goede manier worden ontleed: 

I want to travel to Muiderpoort — tomorrow 
I want to travel to Amsterdam Centraal — tomorrow

Met de informatie die in bovenstaande zinnen is toegevoegd kan ‘Muiderpoort tomorrow’ nooit als een plaatsbepaling worden ontleed, of ‘Centraal tomorrow’ nooit als tijdsbepaling. We hebben dit in de chatbot geïmplementeerd alsof de input tekst van de gebruiker al van spraak naar tekst is geconverteerd met toevoeging van tekens om prosodische informatie aan te duiden.

Het tweede genoemde voorbeeld van prosodische informatie die een zin kan helpen disambigueren is het verschil maken tussen verschillende doelen van een bepaalde tekst input van een gebruiker. Onderstaande delen van conversaties illustreren dit mogelijke verschil in doel van de zin. In onderstaande voorbeelden is het doel van de eerste input van de gebruiker reisinformatie opvragen en het tweede doel rectificatie (verbeteren van de chatbot). In het eerste voorbeeld wordt dit niet door de chatbot herkend. In het tweede voorbeeld wordt dit wel herkend.

1.	User:	I want to go from Rotterdam to Amersfoort.
			→ Doel = reisinformatie opvragen
	Bot:	There is a train from Rotterdam to Almere at 11:36 at track 2. 
			→ Begrepen doel = reisinformatie opvragen
	User:	I want to go to Amersfoort.
			→ Doel = verbetering
	Bot:	There is a train from Rotterdam to Amstersfoort at 12:05 at track 9.
			→ Begrepen doel = reisinformatie opvragen

2.	User: 	I want to go from Rotterdam to Amersfoort.
			→ Doel = reisinformatie opvragen
	Bot:	There is a train from Rotterdam to Almere at 11:36 at track 2. 
			→ Begrepen doel = reisinformatie opvragen
	User:	I want to go to Amersfoort.
			→ Doel = rectificatie
	Bot:	Sorry, I must have misunderstood what you said. There is a train from Rotterdam
			to Amersfoort at 12:05 at track 9.
			→ Begrepen doel = reisinformatie opvragen

Wanneer er sprake is van rectificatie als doen van de zin, wordt er vaak meer nadruk gelegd op het gedeelte dat gerectificeerd moet worden. In het bovenstaande voorbeeld is het de plaatsaanduiding voor de bestemming, die aangepast moet worden. Wanneer deze extra nadruk wordt opgeslagen in de tekst met een ‘--’ markering. Het gesprek zal dan als voorbeeld 2 verlopen. 

====================================

VOORBEELD CONVERSATIES

====================================

Hey there! I can assist you in planning your journey.

>>> Hello 
Well, Hello!

>>> I am in Rotterdam
I understand that you are at Rotterdam

>>> I want to go to Amsterdam Centraal
At what time do you want to leave?

>>> 22
These are your options:
Option 1 (travel time 0:40):
 21:57 from Rotterdam Centraal at platform 12
 22:37 arrival at Amsterdam Centraal

Option 2 (travel time 1:04):
 22:02 from Rotterdam Centraal at platform 9
 23:06 arrival at Amsterdam Centraal

Option 3 (travel time 0:38):
 22:04 from Rotterdam Centraal at platform 12
 22:42 arrival at Amsterdam Centraal

Option 4 (travel time 1:15):
 22:05 from Rotterdam Centraal at platform 14
 22:53 change at Utrecht Centraal to platform 7
 23:20 arrival at Amsterdam Centraal

====================================

Hey there! I can assist you in planning your journey.

>>> Hello
Hello!

>>> I am in Baarn
I understand that you are at Baarn

>>> I want to go to Baarn
Surprise! You are already at Baarn . Please ask me something else.

>>> I want to go to Haarlem
At what time do you want to leave?

>>> 22:00
These are your options:
Option 1 (travel time 1:07):
 22:08 from Baarn at platform 2
 22:56 change at Amsterdam Centraal to platform 1
 23:15 arrival at Haarlem

Option 2 (travel time 1:06):
 22:38 from Baarn at platform 2
 23:26 change at Amsterdam Centraal to platform 1
 23:44 arrival at Haarlem

Option 3 (travel time 1:07):
 23:08 from Baarn at platform 2
 23:56 change at Amsterdam Centraal to platform 1
 00:15 arrival at Haarlem

Option 4 (travel time 1:06):
 23:38 from Baarn at platform 2
 00:26 change at Amsterdam Centraal to platform 1
 00:44 arrival at Haarlem

====================================

Hey there! I can assist you in planning your journey.

>>> Hello
Well, Hello!

>>> What time is it?
I am not a watch! Just check your computer

>>> Are you a human?
Offcourse I am! Are you human?

>>> What is the last train to Muiderpoort
Where do you want to depart from?

>>> Amsterdam Centraal
The last option is:
 23:53 from Amsterdam Centraal at platform 10b
 23:58 arrival at Amsterdam Muiderpoort

====================================

Hey there! I can assist you in planning your journey.

>>> Hello
Hello!

>>> I want to go to Muiderpoort - tomorrow      
Where do you want to depart from?

>>> Baarn
At what time do you want to leave?

>>> 11:00
For tomorrow, these are your options:
Option 1 (travel time 0:36):
 11:08 from Baarn at platform 2
 11:44 arrival at Amsterdam Muiderpoort

Option 2 (travel time 0:36):
 11:38 from Baarn at platform 2
 12:14 arrival at Amsterdam Muiderpoort

Option 3 (travel time 0:36):
 12:08 from Baarn at platform 2
 12:44 arrival at Amsterdam Muiderpoort

Option 4 (travel time 0:36):
 12:38 from Baarn at platform 2
 13:14 arrival at Amsterdam Muiderpoort

====================================

Hey there! I can assist you in planning your journey.

>>> Hello
Hoi hoi!

>>> I want to go from Rotterdam to Amersfoort 
At what time do you want to leave?

>>> I want to go to -- Almere
Sorry, I must have misunderstood what you said. At what time do you want to leave?

>>> 12:00
These are your options:
Option 1 (travel time 1:56):
 12:01 from Goor at platform 1
 12:34 change at Zutphen to platform 3
 13:17 change at Zwolle to platform 3a
 13:57 arrival at Almere Centrum

Option 2 (travel time 1:56):
 12:31 from Goor at platform 1
 13:04 change at Zutphen to platform 3
 13:47 change at Zwolle to platform 3a
 14:27 arrival at Almere Centrum

Option 3 (travel time 1:56):
 13:01 from Goor at platform 1
 13:34 change at Zutphen to platform 3
 14:17 change at Zwolle to platform 3a
 14:57 arrival at Almere Centrum

Option 4 (travel time 1:56):
 13:31 from Goor at platform 1
 14:04 change at Zutphen to platform 3
 14:47 change at Zwolle to platform 3a
 15:27 arrival at Almere Centrum

====================================

Hey there! I can assist you in planning your journey.

>>> Hello
Hoi hoi!

>>> I want to arrive at Niemandsland
I am sorry but Niemandsland is not a station that I know of.

====================================

Hey there! I can assist you in planning your journey.

>>> Hello
Hello!

>>> I want to arrive at Rotterdam at 22
Where do you want to depart from?

>>> Leeuwarden
These are your options:
Option 1 (travel time 2:39):
 19:16 from Leeuwarden at platform 4
 20:20 change at Zwolle to platform 5a
 21:55 arrival at Rotterdam Centraal

Option 2 (travel time 2:39):
 19:46 from Leeuwarden at platform 3
 22:25 arrival at Rotterdam Centraal




