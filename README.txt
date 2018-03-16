OPDRACHT 3 - REISPLANNER CHATBOT

ARIE SOETEMAN		- 	11060565
CLAARTJE BARKHOF	-	11035129
LUCAS FIJEN			- 	10813268

====================================

OVER DEZE CHATBOT

Deze bestanden vormen samen een implementatie van een chatbot die op basis van AIML en interactie met een NS API reisadvies kan geven in een conversatie.

Program Y is een python programma dat AIML 2.0. Interpreteert en zo een chatbot implementeert. We hebben voor deze interpreteerder gekozen omdat deze zeer flexibel is. Bovendien heeft AIML 2.0. functionaliteiten die eerdere, veel gebruikte, versies niet hebben. De functionaliteit waar het meeste gebruik van is gemaakt, is de dynamic map. Dit is een manier om een waarde gegeven in de conversatie toe te wijzen aan een bepaalde output. Een static map doet dit aan de hand van een tekstbestand, waarin key-value paren staan opgeslagen. Een dynamic map daarentegen doet dit aan de hand van een python object. In andere woorden: een dynamic map converteerd een waarde naar een nieuwe waarde met behulp van een (zelf geschreven) algoritme. In onze implementatie is de input die wordt gegeven aan de dynamic map de informatie voor een op te vragen reisadvies (de output). Deze informatie wordt uit de conversatie gehaald.

Om deze chatbot (‘mybot’) te gebruiken, moet het bestand console.sh worden uitgevoerd. Het is belangrijk dat de requirements voor het gebruik van Program-Y zijn geïnstalleerd. Deze zijn te installeren met behulp van requirements.txt. De AIML die we hebben geschreven staat opgeslagen in mybot.aiml. We hebben tevens een set aangemaakt: stations.txt. Ook hebben we een dynamic map aangemaakt: train.py. Zoals eerder aangegeven gebruiken we voor onze implementatie gebruik van de NS API (www.ns.nl/reisinformatie/ns-api). In login.py staan authorisatie gegevens om deze te kunnen gebruiken. Hieronder staan alle belangrijke, benodigde en/of gewijzigde files met relatieve paden (vanaf de aangeleverde directory) aangegeven.

/mybot/console.sh
/program-y/requirements.txt
/mybot/config.yaml
/mybot/aiml/mybot.aiml
/mybot/sets/stations.txt
/program-y/src/programy/dynamic/maps/train.py
/program-y/src/programy/clients/login.py

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
