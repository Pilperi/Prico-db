'''
Homman pyörittämiseen tarvittavat perus datatyypit (luokkina):
-Varusteet
	-Nimi
	-Yhdistelylogiikka
	-Lukumääräkirjanpito
-Hahmot
	-Nimi
	-Levutilanne
	-Rankkitilanne (missä mennään)
	-Varustelutilanne (tarvitsee/päällä)
-Rankit
	-Mitä varusteita rankkiin kuuluu
'''

import os
import math
import time
import json

# Tavaravärien numeeriset koodit, ei nollaa
SININEN  = 0x1
PRONSSI  = 0x2
HOPEA    = 0x3
KULTA    = 0x4
VIOLETTI = 0x5
PUNAINEN = 0x6
VARIKOODIT = {"sininen":  SININEN,
			  "pronssi":  PRONSSI,
			  "hopea":    HOPEA,
			  "kulta":    KULTA,
			  "violetti": VIOLETTI,
			  "punainen": PUNAINEN}

class Varuste:
	'''
	Perusluokka varusteille.
	-Nimi
	-Numeerinen ID
	-Tyyppi (kakera tmv vs. oikea varuste)
	-Jos varuste, vaadittava leveli
	-Jos rakennettavissa, mitä tarvitsee
	-Lukumäärä varastossa
	-Mistä droppaa (lista Karttoja)
	'''
	def __init__(self, nimi="",      idnum=0x000,    tyyppi=None,\
	                   leveli=0,     tarvitsee=None, varastossa=0,\
	                   droppaa=None, aliakset=None,  dikti=None):
		# Tavaran nimi
		self.nimi       = nimi
		# id rakennettu niin että
		#	Ekat neljä bittiä kertovat minkä värinen itemi on kyseessä (sininen, violetti jne)
		#	Viides bitti kertoo onko kyseessä kakera/piirustus (0) vai kokonainen itemi (1)
		#	Seitsemän bittiä juoksevaa numerointia
		self.id = idnum
		# Tyyppi ("Riipus", "Keihäs" tmv)
		self.tyyppi = ""
		if type(tyyppi) is str:
			self.tyyppi = tyyppi
		# Jos kokonainen tavara, mikä on tarvittava leveli
		self.leveli = 0
		# Mitä tarvitsee rakentamiseen ja montako kappaletta
		if type(tarvitsee) is list and all([type(a[0]) is Varuste and type(a[1]) is int for a in tarvitsee]):
			self.tarvitsee  = tarvitsee
		else:
			self.tarvitsee = [(None,0)]
		# Paljonko on varastossa
		self.varastossa = varastossa
		# Mistä droppaa
		self.droppaa    = []
		if type(droppaa) is list and all([type(a) is Kartta for a in droppaa]):
			self.droppaa = droppaa
		# Tavaran lempinimet ("joulukuusimiekka" jne)
		self.aliakset   = []
		if type(aliakset) is list and all([type(a) is str for a in aliakset]):
			self.aliakset = aliakset
		# Lue arvot diktistä
		if type(dikti) is dict:
			self.lue_diktista(dikti)

	def korjaa_id(self, lista):
		'''
		Aseta juokseva numero oikeaan arvoon,
		sen perusteella kuinka monta sellaista alkiota annetussa listassa
		on, joilla samat ensimmäiset viisi bittiä. Ei pitäisi olla montaa.
		'''
		print("{0:b}".format(self.id))
		juoksevanumero = 0
		if len(lista):
			matsaavat = [a for a in lista if (a.id & 0xF80) == (self.id & 0xF80)]
			juoksevanumero = len(matsaavat)
			if juoksevanumero > 0x7F:
				# cappaa apua
				print("Slotit täynnä ID-avaruudelle {0:b}".format(self.id & 0xF80))
				juoksevanumero = 0x7F
		self.id = (self.id & 0xF80) | juoksevanumero
		print("{0:b}".format(self.id))

	def dekryptaa_id(self):
		'''
		Palauttaa puretun version ID:stä.
		'''
		varikoodi = (self.id & 0xF00) >> 8
		tyyppi    = (self.id & 0x080) >> 7
		print(tyyppi)
		indeksi   =  self.id & 0x07F
		vari = "Määrittelemättömän värinen"
		for avain in VARIKOODIT:
			if VARIKOODIT[avain] == varikoodi:
				vari = avain
				break
		if tyyppi:
			tyyppi = "tavara"
		else:
			tyyppi = "osanen"
		st = f"{vari} {tyyppi} no. {indeksi}"
		return(st, (varikoodi, tyyppi, indeksi))

	def __str__(self):
		st =  f"Nimi:       {self.nimi}\n"
		st += f"ID:         {self.id}\n"
		st +=  "Tyyppi:     {:s}\n".format(self.tyyppi*(len(self.tyyppi)>0) + "Määrittelemätön"*(len(self.tyyppi)==0))
		st +=  "Leveli:     {:d}\n".format(self.leveli)
		st += "Tarvitsee:"
		if (None,0) not in self.tarvitsee:
			# st += f"     {self.tarvitsee[0][0].nimi} x{self.tarvitsee[0][1]}"
			for t,tavara in enumerate(self.tarvitsee):
				st += "  {}{} x{}".format("\n            "*bool(t), tavara[0].nimi, tavara[1])
		else:
			st += "  -"
		st += "\n"
		st += f"Varastossa: {self.varastossa}\n"
		st += "Droppaa:"
		for k,kartta in enumerate(self.droppaa):
				st += "  {}{}".format("\n            "*bool(k), kartta.nimi)
		st += "\n"
		st += "Lempinimet:"
		for n,nimi in enumerate(self.aliakset):
				st += "  {}{}".format("\n            "*bool(n), nimi)
		st += "\n"
		return(st)

	def jsoniksi(self):
		'''
		Antaa varustetiedot JSON-stringinä.
		'''
		print([(a[0].id, a[1]) for a in self.tarvitsee if a[0] is not None])
		dikti = {
				"Nimi":       self.nimi,
				"ID":         self.id,
				"Tyyppi":     self.tyyppi,
				"Leveli":     self.leveli,
				"Tarvitsee":  [(a[0].id, a[1]) for a in self.tarvitsee if a[0] is not None], # pelkät ID:t, koska uniikkeja
				"Varastossa": self.varastossa,
				"Droppaa":    [a.nimi for a in self.droppaa], # pelkkä kartan nimistringi
				"Aliakset":   self.aliakset
				}
		print(dikti)
		json_str = json.dumps(dikti)
		print(json_str)
		return(json_str)

	def lue_diktista(self, dikti):
		'''
		Lue arvot diktistä.
		'''
		if type(dikti.get("Nimi")) is str:
			self.nimi = dikti.get("Nimi")
		if type(dikti.get("ID")) is int:
			self.id = dikti.get("ID")
		if type(dikti.get("Tyyppi")) is str:
			self.tyyppi = dikti.get("Tyyppi")
		if type(dikti.get("Leveli")) is int:
			self.leveli = dikti.get("Leveli")
		if type(dikti.get("Tarvitsee")) is list:
			self.tarvitsee = dikti.get("Tarvitsee")
		if type(dikti.get("Varastossa")) is int:
			self.varastossa = dikti.get("Varastossa")
		if type(dikti.get("Droppaa")) is list:
			self.droppaa = dikti.get("Droppaa")
		if type(dikti.get("Aliakset")) is list:
			self.aliakset = dikti.get("Aliakset")

	def osat_pointtereiksi(self, varustetietokanta):
		'''
		Muuttaa tarvitsevuuslistan alkiot pelkistä numeerisista id-arvoista Varustepointtereiksi.
		'''
		for o,osanen in enumerate(self.tarvitsee):
			if type(osanen[0]) is int:
				varustepointteri = varustetietokanta.etsi_varusteid(osanen[0])
				# Löytyi ID:tä vastaava varuste
				if varustepointteri is not None:
					self.tarvitsee[o] = (varustepointteri, osanen[1]) # määrä sama int, laatu int -> Varuste
				else:
					print(f"Varustetta ID:llä {osanen[0]} ei ole tietokannassa???")


class Varustetietokanta:
	'''
	Tietokanta olemassaolevista varusteista.
	'''
	def __init__(self, varustelista=None, aikaleima=None, stringi=None):
		self.varustelista = [] # lista Varusteita
		if type(varustelista) is list and all([type(a) is Varuste for a in varustelista]):
			self.varustelista = varustelista
		# Tietokannan aikaleima
		self.aikaleima = 0
		if type(aikaleima) is int:
			self.aikaleima = aikaleima
		elif type(aikaleima) is str:
			self.aikaleima = self.hanki_aikaleima(aikaleima)
		# Jos aikaleima on tässä kohtaa nolla, kelvollista ei ole annettu.
		# Käytetään nykyhetkeä.
		if not self.aikaleima:
			self.aikaleima = self.hanki_aikaleima("nyt")
		# Lue arvot JSON-stringistä
		if type(stringi) is str:
			self.lue_stringista(stringi)

	def hanki_aikaleima(self, aika="nyt"):
		'''
		Hankkii kokonaislukumuotoisen aikaleiman,
		jolla seurata kuinka tuoreesta tietokannasta on kyse.
		'''
		aikaleima = 0
		# Juuri tällä hetkellä
		if aika is "nyt":
			t = time.localtime()
			vuosi = "{:04d}".format(t.tm_year)
			kuu   = "{:02d}".format(t.tm_mon)
			paiv  = "{:02d}".format(t.tm_mday)
			tunti = "{:02d}".format(t.tm_hour)
			minu  = "{:02d}".format(t.tm_min)
			aikaleima = int(f"{vuosi}{kuu}{paiv}{tunti}{minu}")
		# str yyyy-mm-dd-mi
		else:
			splitattuaika = aika.split("-")
			if len(splitattuaika) > 4 and all([all([a.isnumeric() for a in b] for b in splitattuaika[:5])]):
				vuosi = "{:04d}".format(int(splitattuaika[0]))
				kuu   = "{:02d}".format(int(splitattuaika[1]))
				paiv  = "{:02d}".format(int(splitattuaika[2]))
				tunti = "{:02d}".format(int(splitattuaika[3]))
				minu  = "{:02d}".format(int(splitattuaika[4]))
				aikaleima = int(f"{vuosi}{kuu}{paiv}{tunti}{minu}")
		return(aikaleima)

	def lisaa(self, varuste, korvaa=False):
		'''
		Lisää varuste tietokantaan.
		Jos varuste on jo tietokannassa ja 'korvaa' on tosi,
		olemassaolevat varuste korvataan uudella.
		'''
		lisatty = False
		for v,vanhavaruste in enumerate(self.varustelista):
			if vanhavaruste.id == varuste.id and korvaa:
				print(f"Korvataan jo olemassaoleva {vanhavaruste.id} ({vanhavaruste.nimi}) uudella ({varuste.nimi})")
				self.varustelista[v] = varuste
				lisatty = True
				break
			elif vanhavaruste.id == varuste.id:
				print("Varuste on jo tietokannassa, ei lisätä.")
				lisatty = True
				break
		if not lisatty:
			self.varustelista.append(varuste)

	def poista(self, varuste):
		'''
		Poista varuste tietokannasta.
		'''
		poistettu = False
		for v,vanhavaruste in enumerate(self.varustelista):
			if vanhavaruste.id == varuste.id:
				self.varustelista.pop(v)
				print(f"Poistettiin varuste ID {varuste.id} ({varuste.nimi})")
				poistettu = True
				break
		if not poistettu:
			print(f"Varustetta {varuste.id} ei löytynyt tietokannasta.")

	def etsi_varusteid(self, id):
		'''
		Etsii varustetta sen numeerisella id:llä.
		'''
		for varuste in self.varustelista:
			if varuste.id == id:
				return(varuste)
		return(None)

	def etsi_kartan_varusteet(self, kartannimi):
		'''
		Hakee varusteet jotka droppaavat annetusta kartasta.
		'''
		hakutulokset = []
		for varuste in self.varustelista:
			if karttanimi in [a.nimi for a in varuste.droppaa]:
				hakutulokset.append(varuste)
		return(hakutulokset)

	def __str__(self):
		'''
		Antaa JSON-yhteensopivan stringin itsestä ja kaikista
		kirjatuista varusteista.
		'''
		st = f"{{\n\"Aikaleima\":{self.aikaleima},\n\"Varusteet\": ["
		print(st)
		print(self.varustelista)
		for v,varuste in enumerate(self.varustelista):
			print(v)
			st += "\n  {:s}{:s}".format(varuste.jsoniksi(), ","*(v<(len(self.varustelista)-1)))
			print(st)
		st += "\n]\n}\n"
		print(st)
		return(st)

	def lue_stringista(self, stringi):
		'''
		Lue tietokanta stringistä.
		'''
		dikti = json.loads(stringi)
		if type(dikti.get("Aikaleima")) is int:
			self.aikaleima = dikti.get("Aikaleima")
		if type(dikti.get("Varusteet")) is list:
			varusteet = []
			for varustedikti in dikti.get("Varusteet"):
				print(varustedikti)
				varuste = Varuste(dikti=varustedikti)
				varusteet.append(varuste)
			self.varustelista = varusteet
			# Varusteiden tarpeet id-inteistä pointtereiksi
			for varuste in self.varustelista:
				varuste.osat_pointtereiksi(self)

	def tallenna(self, tiedostopolku):
		'''
		Tallenna tietokanta tiedostoon.
		'''
		print("Tallennetaan varustetietokanta ({} varustetta)".format(len(self.varustelista)))
		tiedosto = open(tiedostopolku, "w+")
		tiedosto.write(str(self))
		tiedosto.close()
		print(f"Tallennettu tiedostoon {tiedostopolku}")

	def lue_tiedostosta(self, tiedostopolku):
		'''
		Lue tietokanta tiedostosta.
		'''
		print("Lue tiedostosta")
		if os.path.exists(tiedostopolku):
			print(f"Luetaan tietokanta tiedostosta {tiedostopolku}")
			tiedosto = open(tiedostopolku, "r")
			st = ""
			for rivi in tiedosto.readlines():
				st += rivi
			tiedosto.close()
			self.lue_stringista(st)
			print("Luettu {:d} varustetta.".format(len(self.varustelista)))
		else:
			print(f"Tiedostoa {tiedostopolku} ei ole olemassa...")

class Kartta:
	"""Luokka kartan dropeille"""
	def __init__(self, tyyppi="Normaali", maailma=0, kartta=0, droppaa=None):
		# Missä maailma sijaitsee
		self.tyyppi = tyyppi # Normaali, Hardi, Try hardi, muu???
		self.maailma = 0
		if type(maailma) is int and maailma > 0:
			self.maailma = maailma
		self.kartta  = 0
		if type(kartta) is int and kartta > 0:
			self.kartta = kartta
		self.nimi    = f"{self.tyyppi}-{self.maailma}-{self.kartta}"
		# Mitä kartasta droppaa
		self.droppaa = []
		if type(droppaa) is list and all([type(a) is Varuste for a in droppaa]):
			self.droppaa = droppaa

	def __add__(self, varuste):
		'''
		Lisää varuste kartan droppeihin.
		'''
		if type(varuste) is Varuste and varuste not in self.droppaa:
			self.droppaa.append(varuste)

	def __sub__(self, varuste):
		'''
		Poista varuste dropeista (hutilisäyksen korjaus)
		'''
		if varuste in self.droppaa:
			self.droppaa.remove(varuste)
