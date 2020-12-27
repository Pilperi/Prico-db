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

import math
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
	def __init__(self, nimi="", idnum=0x000, tyyppi=None, leveli=0, tarvitsee=None, varastossa=0, droppaa=None, aliakset=None):
		# Tavaran nimi
		self.nimi       = nimi
		# id rakennettu niin että
		#	Ekat neljä bittiä kertovat minkä värinen itemi on kyseessä (sininen, violetti jne)
		#	Viides bitti kertoo onko kyseessä kakera/piirustus (0) vai kokonainen itemi (1)
		#	Seitsemän bittiä juoksevaa numerointia
		self.id         = idnum
		# Tyyppi ("Riipus", "Keihäs" tmv)
		self.tyyppi = ""
		if type(tyyppi) is str:
			self.tyyppi = tyyppi
		# Jos kokonainen tavara, mikä on tarvittava leveli
		self.leveli     = 0
		if self.id & (0x400):
			self.leveli = leveli
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

	def korjaa_id(self, lista):
		'''
		Aseta juokseva numero oikeaan arvoon,
		sen perusteella kuinka monta sellaista alkiota annetussa listassa
		on, joilla samat ensimmäiset viisi bittiä. Ei pitäisi olla montaa.
		'''
		print("{0:b}".format(self.id))
		juoksevanumero = 0
		if len(lista):
			matsaavat = [a for a in lista if ((a.id & self.id) & 0xF80)]
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
		tyyppi    = (self.id & 0x080) > 0
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

	def __add__(self, other):
		'''
		Summausoperaatio: jos int niin kasvatetaan varastotilannetta int verran.
		Jos Varuste niin luodaan uusi varuste joka on yhdistelmä tästä ja toisesta.
		'''
		if type(other) is int:
			self.varastossa += other
			return(self)
		elif type(other) is Varuste:
			uusivaruste = Varuste(nimi=f"{self.nimi}+{other.nimi}", tyyppi=1, leveli=max(self.leveli, other.leveli), tarvitsee=[(self, 1), (other, 1)], varastossa=0)
			return(uusivaruste)
		else:
			return(other)

	def json(self):
		'''
		Antaa varustetiedot JSON-stringinä.
		'''
		dikti = {
				"Nimi":       self.nimi,
				"ID":         self.id,
				"Tyyppi":     self.tyyppi,
				"Leveli":     self.leveli,
				"Tarvitsee":  [a.id for a in self.tarvitsee], # pelkät ID:t, koska uniikkeja
				"Varastossa": self.varastossa,
				"Droppaa":    [a.nimi for a in self.droppaa],
				"Aliakset":   self.aliakset
				}
		json_str = json.dumps(dikti)
		return(json_str)

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
