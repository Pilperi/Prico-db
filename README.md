# Princess Connect tietokantaprojekti
Graafinen ohjelma, jolla pitää kirjaa tavaroista ja leveleistä ja sen sellaisesta.
Yksi päämotivaattori on se, että kartoista droppaa monen moista tavaraa sen lisäksi mitä karttaruudussa seisoo.
Eihän sitä ihmismielin voi muistaa mitä saladroppeja missäkin tarkalleen ottaen on, niin olisi kiva pitää niistä kirjaa.
Tämä ohjelma on sitä varten, ja sitten myöhemmin jos voisi ihmetellä tyttöjen ränkkijuttuja ja sen sellaista visualisointia. Kahtoo mitä keksii.

Tähän mennessä tehty:

	[x] Tavarat määritelty (nimi+kuva+väri)
	[x] Tavaroiden riippuvuussuhdanteet määritelty (tavara koostuu 5xtätä + 1xtuota)
	[x] Tavaroiden tyypit määritelty (sini, pronssi jne)
	[/] Karttojen normidropit määritelty (se mitä peli kertoo suoraan että droppaa)
	[/] Karttojen piilodropit määritelty (se mitä kartan tiedoista ei näy)

Pitäisi vielä tehdä:

	[ ] Fiksut hakutoiminnot (näytä listana kartat joista droppaa X, ja karttaa klikatessa mitä muuta sieltä tulee)
	[ ] Lempinimien helppo lisääminen (jotta hakeminen olisi helpompaa)
	[ ] Eri tietokantojen yhdistäminen yhdeksi tietokannaksi (pitäisi olla ez)
	[ ] Jostain syystä ainakin meitillä jotkut kuvat bugaa, lähinnä pari violettiä killutinta (id 1393 & 1394)

Joskus hamassa tulevaisuudessa:
	
	[ ] Henkkoht varustetilannetietokanta
	[ ] Tytyjen tavarat the tietokanta


Jos haluaa osallistua niin saa pistää täyttäen. Täällä gitin tietokannassa on mitä minä olen jaksanut täyttää/ottanut vastaan, pusken uudet versiot yleensä aika heti kun olen saanut jotain tehtyä.
Osallistuminen käy niin että lataa Python-tulkin (3.X) jos sellaista ei vielä ole, ja mielellään niin että mukana on tarvittavat paketit. Mitään kovin eksoottisia moduuleita en tässä käytä:

	-JSON
	-Qt
	-PIL

Tavaroiden lisääminen käy niin että kutsuu pythonilla ``ikkuna_droppimaarittely.py`` ja siitä pitäisi tulla kankea GUI esiin. Siinä on vasemmalla pudotuslista tavaroista sekä valitun tavaran tietojen näyttöruudut. Keskellä on filtterinamiskat, joilla saa karsittua listaa sen pituiseksi että sieltä jopa löytää jotain. Oikeassa reunassa on varsinainen kartan määrittämisosio, joka toimii niin että:

	1) Laita tekstikenttään kartan nimi, esim. 15-5
	2) Jos karttaa ei ole määritelty, tekstiruutu on punainen ja vieressä vihreä nappi jossa +
	3) Paina sitä plussaa niin annetun niminen kartta otetaan määriteltäväksi (vähän kömpelö)
	4) Siin alapuolella on 5x5 ruudukko bokseja. Kun painaa plussaa, kartan droppilistaan lisätään vasemmalla näkyvä tavara
	5) Tavaran kuvan pitäisi näkyä pienenä boksina ruudukossa. Jos sitä painaa, tavara poistetaan droppilistasta
	6) Kartta- ja varustetiedot tallennetaan joka lisäys- ja poisto-operaation jälkeen .json-tiedostoihin. Saattaa joskus crashata ja viedä tiedoston mennessään, niin kantsii ottaa backuppeja ":D"

Luodut JSON-tiedostot voi sitten lähettää meitille discordissa ja ihmettelen miten yhdistän ne omaan vastaavaan ja pusken sitten gittiin.
