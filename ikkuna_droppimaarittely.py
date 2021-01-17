'''
Ikkuna karttojen droppien määrittelyyn.
'''

import os
import sys
import shutil
import luokat_perus as priluokat
from PIL import Image, ImageQt
from PyQt5 import Qt, QtCore, QtWidgets, QtGui

IKKUNAMITAT = (700,500)
MARGINAALIT = (10,10)

LISTALABEL      = (MARGINAALIT[0], MARGINAALIT[1], 200, 50)
TAVARALISTA     = (LISTALABEL[0], LISTALABEL[1]+LISTALABEL[3], LISTALABEL[2], 50)
TARKISTUSTAVARA = (TAVARALISTA[0], TAVARALISTA[1]+TAVARALISTA[3], 200, 200)
TARKISTUSKENTTA = (TARKISTUSTAVARA[0], TARKISTUSTAVARA[1]+TARKISTUSTAVARA[3], TARKISTUSTAVARA[2], 150)

# Tavaran värit
FILTTERILABEL  = (LISTALABEL[0]+LISTALABEL[2], LISTALABEL[1], LISTALABEL[2], LISTALABEL[3])
VARI_SINI      = (FILTTERILABEL[0], FILTTERILABEL[1]+FILTTERILABEL[3], int(FILTTERILABEL[2]/6), FILTTERILABEL[3])
VARI_PRONSSI   = (VARI_SINI[0]+VARI_SINI[2], VARI_SINI[1], VARI_SINI[2], VARI_SINI[3])
VARI_HOPEA     = (VARI_PRONSSI[0]+VARI_PRONSSI[2], VARI_PRONSSI[1], VARI_SINI[2], VARI_SINI[3])
VARI_KULTA     = (VARI_HOPEA[0]+VARI_HOPEA[2], VARI_HOPEA[1], VARI_SINI[2], VARI_SINI[3])
VARI_VIOLETTI  = (VARI_KULTA[0]+VARI_KULTA[2], VARI_KULTA[1], VARI_SINI[2], VARI_SINI[3])
VARI_PUNAINEN  = (VARI_VIOLETTI[0]+VARI_VIOLETTI[2], VARI_VIOLETTI[1], VARI_SINI[2], VARI_SINI[3])

# Tavaroiden tyypit
NAPPI_MIEKKA    = (VARI_SINI[0], VARI_SINI[1]+VARI_SINI[3], int(FILTTERILABEL[2]*0.33), 50)
NAPPI_KEIHAS    = (NAPPI_MIEKKA[0]+NAPPI_MIEKKA[2], NAPPI_MIEKKA[1], NAPPI_MIEKKA[2], NAPPI_MIEKKA[3])
NAPPI_KIRVES    = (NAPPI_KEIHAS[0]+NAPPI_KEIHAS[2], NAPPI_KEIHAS[1], NAPPI_MIEKKA[2], NAPPI_MIEKKA[3])

NAPPI_NYRKKI    = (NAPPI_MIEKKA[0], NAPPI_MIEKKA[1]+NAPPI_MIEKKA[3], NAPPI_MIEKKA[2], NAPPI_MIEKKA[3])
NAPPI_JOUSI     = (NAPPI_NYRKKI[0]+NAPPI_NYRKKI[2], NAPPI_NYRKKI[1], NAPPI_MIEKKA[2], NAPPI_MIEKKA[3])
NAPPI_SAUVA     = (NAPPI_JOUSI[0]+NAPPI_JOUSI[2], NAPPI_JOUSI[1], NAPPI_MIEKKA[2], NAPPI_MIEKKA[3])

NAPPI_KILPI     = (NAPPI_NYRKKI[0], NAPPI_NYRKKI[1]+NAPPI_NYRKKI[3], NAPPI_MIEKKA[2], NAPPI_MIEKKA[3])
NAPPI_PANSSARI  = (NAPPI_KILPI[0]+NAPPI_KILPI[2], NAPPI_KILPI[1], NAPPI_MIEKKA[2], NAPPI_MIEKKA[3])
NAPPI_HARPAKE   = (NAPPI_PANSSARI[0]+NAPPI_PANSSARI[2], NAPPI_PANSSARI[1], NAPPI_MIEKKA[2], NAPPI_MIEKKA[3])

NAPPI_HATTU     = (NAPPI_KILPI[0], NAPPI_KILPI[1]+NAPPI_KILPI[3], NAPPI_MIEKKA[2], NAPPI_MIEKKA[3])
NAPPI_JALKINE   = (NAPPI_HATTU[0]+NAPPI_HATTU[2], NAPPI_HATTU[1], NAPPI_MIEKKA[2], NAPPI_MIEKKA[3])

LABERL_KARTTA   = (FILTTERILABEL[0]+FILTTERILABEL[2], FILTTERILABEL[1], 270, 50)
KARTTAKENTTA    = (LABERL_KARTTA[0], LABERL_KARTTA[1]+LABERL_KARTTA[3], LABERL_KARTTA[2]-50, LABERL_KARTTA[3])
NAPPI_KARTTA    = (KARTTAKENTTA[0]+KARTTAKENTTA[2], KARTTAKENTTA[1], LABERL_KARTTA[2]-KARTTAKENTTA[2], KARTTAKENTTA[3])
TAVARAGRID      = (KARTTAKENTTA[0], KARTTAKENTTA[1]+KARTTAKENTTA[3], LABERL_KARTTA[2], 270)
GRIDITAVARA     = (50, 50)


def kuva_pixmapiksi(tiedostopolku, mitat):
	'''
	Muuttaa tiedostopolun takana olevan kuvan sellaiseksi että
	se on annettujen mittojen kokoinen ja sen voi laittaa qt-ikoniksi.

	Ottaa:
	tiedostopolku: str
		Kuvan sijainti.
	mitat: tuple tai lista inttejä (len 2+)
		Kuvan halutut mitat.

	Palauttaa:
	QIcon tai None
		None virheessä, onnistuessa QIcon jonka voi laittaa esim. nappiin
	'''
	if os.path.exists(tiedostopolku) and type(mitat) in [list,tuple] and all([type(a) is int for a in mitat]):
		kuva = Image.open(tiedostopolku)
		kuva = kuva.resize((mitat[0], mitat[1]))
		img = ImageQt.ImageQt(kuva)
		pixmap = QtGui.QPixmap.fromImage(img)
		icon = QtGui.QIcon(pixmap)
		return(icon)
	return(None)

def tavara_napiksi(tavara, funktio):
	'''
	Antaa tavaraa vastaavan QPushButton-olion,
	jossa tavaran kuva. Nappi kytketään annettuun
	funktioon niin, että se laittaa sisääntuloargumentiksi
	itse tavaran.
	'''
	nappi = QtWidgets.QPushButton()
	nappi.setIconSize(QtCore.QSize(GRIDITAVARA[0], GRIDITAVARA[1]))
	nappi.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
	nappi.setFocusPolicy(QtCore.Qt.NoFocus)
	ikoni = None
	if type(tavara) is priluokat.Varuste:
		#  Laita kuva
		tavaran_kuva = f"./Kuvat/Varusteet/{tavara.id}.png"
		ikoni = kuva_pixmapiksi(tavaran_kuva, (GRIDITAVARA[0], GRIDITAVARA[1]))
		nappi.setStyleSheet("QPushButton:active {border: 0px solid;}")
	if ikoni is not None:
		nappi.setIcon(ikoni)
	else:
		nappi.setIcon(QtGui.QIcon())
	nappi.clicked.connect(lambda t: funktio(tavara)) # kytketään annettuun funktioon 
	return(nappi)

class Tavaragridi(QtWidgets.QWidget):
	'''
	Tavarat gridinä.
	'''
	def __init__(self, parent, sijainti, tavarat, funktio):
		'''
		Gridi läimäistään pääikkunaan "parent" sijainnille "sijainti",
		siihen laitetaan tavarapainikkeet kuvaamaan tavaroita "tavarat"
		ja kukin nappi kytketään funktioon "funktio" niin että
		se syöttää siihen kyseisen Varuste-olion.
		'''
		super().__init__(parent=parent)
		self.grid = Qt.QGridLayout()
		# self.grid.setHorizontalSpacing(5)
		# self.grid.setVerticalSpacing(5)
		self.grid.setSpacing(5)
		varusteindeksi = 0
		for i in range(5):
			for j in range(5):
				if varusteindeksi < len(tavarat):
					# print(f"{varusteindeksi}/{len(tavarat)}: kuva")
					nappi = tavara_napiksi(tavarat[varusteindeksi], funktio)
				else:
					# print(f"{varusteindeksi}/{len(tavarat)}: tyhjä")
					nappi = tavara_napiksi(None, funktio)
				if varusteindeksi == len(tavarat):
					# print(f"{varusteindeksi}/{len(tavarat)}: plussa")
					nappi.setText("+")
				self.grid.addWidget(nappi, i, j)
				varusteindeksi += 1
		self.setGeometry(QtCore.QRect(*sijainti))
		self.setLayout(self.grid)
		self.show()

class Paaikkuna(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Lisää tavaroita karttoihin")
		self.resize(IKKUNAMITAT[0], IKKUNAMITAT[1])
		self.setMinimumSize(IKKUNAMITAT[0], IKKUNAMITAT[1])
		self.setMaximumSize(IKKUNAMITAT[0], IKKUNAMITAT[1])
		self.setStyleSheet("background-color: #31363b")

		# Tavaralista
		# Listalaabeli
		self.label_tavaralista = QtWidgets.QLabel(self)
		self.label_tavaralista.setGeometry(QtCore.QRect(*LISTALABEL))
		self.label_tavaralista.setText("Lista tavaroista")
		# Itse lista
		self.tavaralista = QtWidgets.QComboBox(self)
		self.tavaralista.setGeometry(QtCore.QRect(*TAVARALISTA))
		# Esikatselu jo määritelly tavaralle
		self.tarkistustavara = QtWidgets.QPushButton(self)
		self.tarkistustavara.setGeometry(QtCore.QRect(*TARKISTUSTAVARA))
		self.tarkistustavara.setIconSize(QtCore.QSize(TARKISTUSTAVARA[2],TARKISTUSTAVARA[3]))
		self.tarkistustavara.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.tarkistustavara.setFocusPolicy(QtCore.Qt.NoFocus)

		# Tavaran tiedot
		self.tarkistus_tavaratiedot = QtWidgets.QTextEdit(self)
		self.tarkistus_tavaratiedot.setGeometry(QtCore.QRect(*TARKISTUSKENTTA))
		self.tarkistus_tavaratiedot.setText("")
		self.tarkistus_tavaratiedot.setReadOnly(True)
		self.tarkistus_tavaratiedot.setAlignment(QtCore.Qt.AlignTop)
		self.tarkistus_tavaratiedot.setWordWrapMode(0)
		self.tarkistus_tavaratiedot.setStyleSheet("background-color: #31363b")

		# Filtteröintiosiot
		self.filtterit = {"Väri": None, "Tyyppi": None, "Vaindropit": True}
		# Filtteröi värin perusteella
		self.varistatukset = {"Sininen": True,
		                      "Pronssi": True,
		                      "Hopea":   True,
		                      "Kulta":   True,
		                      "Violetti":True,
		                      "Punainen":True}
		# Tavaroiden värit
		if True:
			# Tavaran väri: label
			self.label_filtteri = QtWidgets.QLabel(self)
			self.label_filtteri.setGeometry(QtCore.QRect(*FILTTERILABEL))
			self.label_filtteri.setText("Filtteröi tavaralista")
			# Tavaran väri: nappi sini
			self.varinappi_sini = QtWidgets.QPushButton(self)
			self.varinappi_sini.setGeometry(QtCore.QRect(*VARI_SINI))
			self.varinappi_sini.setFocusPolicy(QtCore.Qt.NoFocus)
			self.varinappi_sini.setText("Si")
			self.varinappi_sini.setStyleSheet("background-color: #94d2f8")
			self.varinappi_sini.clicked.connect(lambda t: self.paivita_varinapit("Sininen"))
			# Tavaran väri: nappi pronssi
			self.varinappi_pronssi = QtWidgets.QPushButton(self)
			self.varinappi_pronssi.setGeometry(QtCore.QRect(*VARI_PRONSSI))
			self.varinappi_pronssi.setFocusPolicy(QtCore.Qt.NoFocus)
			self.varinappi_pronssi.setText("Pr")
			self.varinappi_pronssi.setStyleSheet("background-color: #e58852")
			self.varinappi_pronssi.clicked.connect(lambda t: self.paivita_varinapit("Pronssi"))
			# Tavaran väri: nappi hopea
			self.varinappi_hopea = QtWidgets.QPushButton(self)
			self.varinappi_hopea.setGeometry(QtCore.QRect(*VARI_HOPEA))
			self.varinappi_hopea.setFocusPolicy(QtCore.Qt.NoFocus)
			self.varinappi_hopea.setText("Ho")
			self.varinappi_hopea.setStyleSheet("background-color: #afb7d4")
			self.varinappi_hopea.clicked.connect(lambda t: self.paivita_varinapit("Hopea"))
			# Tavaran väri: nappi kulta
			self.varinappi_kulta = QtWidgets.QPushButton(self)
			self.varinappi_kulta.setGeometry(QtCore.QRect(*VARI_KULTA))
			self.varinappi_kulta.setFocusPolicy(QtCore.Qt.NoFocus)
			self.varinappi_kulta.setText("Ku")
			self.varinappi_kulta.setStyleSheet("background-color: #f8f29d")
			self.varinappi_kulta.clicked.connect(lambda t: self.paivita_varinapit("Kulta"))
			# Tavaran väri: nappi violetti
			self.varinappi_violetti = QtWidgets.QPushButton(self)
			self.varinappi_violetti.setGeometry(QtCore.QRect(*VARI_VIOLETTI))
			self.varinappi_violetti.setFocusPolicy(QtCore.Qt.NoFocus)
			self.varinappi_violetti.setText("Vi")
			self.varinappi_violetti.setStyleSheet("background-color: #af62e5")
			self.varinappi_violetti.clicked.connect(lambda t: self.paivita_varinapit("Violetti"))
			# Tavaran väri: nappi punainen
			self.varinappi_punainen = QtWidgets.QPushButton(self)
			self.varinappi_punainen.setGeometry(QtCore.QRect(*VARI_PUNAINEN))
			self.varinappi_punainen.setFocusPolicy(QtCore.Qt.NoFocus)
			self.varinappi_punainen.setText("Pu")
			self.varinappi_punainen.setStyleSheet("background-color: #e32a45")
			self.varinappi_punainen.clicked.connect(lambda t: self.paivita_varinapit("Punainen"))

		# Tavaran tyyppinapit
		if True:
			# Miekka
			self.nappi_miekka = QtWidgets.QPushButton(self)
			self.nappi_miekka.setGeometry(QtCore.QRect(*NAPPI_MIEKKA))
			self.nappi_miekka.setFocusPolicy(QtCore.Qt.NoFocus)
			self.nappi_miekka.setText("Miekka")
			self.nappi_miekka.clicked.connect(lambda t: self.nappia_painettu("Miekka"))
			# Keihäs
			self.nappi_keihas = QtWidgets.QPushButton(self)
			self.nappi_keihas.setGeometry(QtCore.QRect(*NAPPI_KEIHAS))
			self.nappi_keihas.setFocusPolicy(QtCore.Qt.NoFocus)
			self.nappi_keihas.setText("Keihäs")
			self.nappi_keihas.clicked.connect(lambda t: self.nappia_painettu("Keihäs"))
			# Kirves
			self.nappi_kirves = QtWidgets.QPushButton(self)
			self.nappi_kirves.setGeometry(QtCore.QRect(*NAPPI_KIRVES))
			self.nappi_kirves.setFocusPolicy(QtCore.Qt.NoFocus)
			self.nappi_kirves.setText("Kirves")
			self.nappi_kirves.clicked.connect(lambda t: self.nappia_painettu("Kirves"))
			# --------------------------------------------------------
			# Nyrkki
			self.nappi_nyrkki = QtWidgets.QPushButton(self)
			self.nappi_nyrkki.setGeometry(QtCore.QRect(*NAPPI_NYRKKI))
			self.nappi_nyrkki.setFocusPolicy(QtCore.Qt.NoFocus)
			self.nappi_nyrkki.setText("Nyrkki")
			self.nappi_nyrkki.clicked.connect(lambda t: self.nappia_painettu("Nyrkki"))
			# Jousi
			self.nappi_jousi = QtWidgets.QPushButton(self)
			self.nappi_jousi.setGeometry(QtCore.QRect(*NAPPI_JOUSI))
			self.nappi_jousi.setFocusPolicy(QtCore.Qt.NoFocus)
			self.nappi_jousi.setText("Jousi")
			self.nappi_jousi.clicked.connect(lambda t: self.nappia_painettu("Jousi"))
			# Taikasauva
			self.nappi_sauva = QtWidgets.QPushButton(self)
			self.nappi_sauva.setGeometry(QtCore.QRect(*NAPPI_SAUVA))
			self.nappi_sauva.setFocusPolicy(QtCore.Qt.NoFocus)
			self.nappi_sauva.setText("Taikas.")
			self.nappi_sauva.clicked.connect(lambda t: self.nappia_painettu("Taikasauva"))
			# --------------------------------------------------------
			# Kilpi
			self.nappi_kilpi = QtWidgets.QPushButton(self)
			self.nappi_kilpi.setGeometry(QtCore.QRect(*NAPPI_KILPI))
			self.nappi_kilpi.setFocusPolicy(QtCore.Qt.NoFocus)
			self.nappi_kilpi.setText("Kilpi")
			self.nappi_kilpi.clicked.connect(lambda t: self.nappia_painettu("Kilpi"))
			# Panssari
			self.nappi_panssari = QtWidgets.QPushButton(self)
			self.nappi_panssari.setGeometry(QtCore.QRect(*NAPPI_PANSSARI))
			self.nappi_panssari.setFocusPolicy(QtCore.Qt.NoFocus)
			self.nappi_panssari.setText("Panssari")
			self.nappi_panssari.clicked.connect(lambda t: self.nappia_painettu("Panssari"))
			# Päähine
			self.nappi_hattu = QtWidgets.QPushButton(self)
			self.nappi_hattu.setGeometry(QtCore.QRect(*NAPPI_HATTU))
			self.nappi_hattu.setFocusPolicy(QtCore.Qt.NoFocus)
			self.nappi_hattu.setText("Päähine")
			self.nappi_hattu.clicked.connect(lambda t: self.nappia_painettu("Päähine"))
			# --------------------------------------------------------
			# Höpläimet
			self.nappi_jalkine = QtWidgets.QPushButton(self)
			self.nappi_jalkine.setGeometry(QtCore.QRect(*NAPPI_JALKINE))
			self.nappi_jalkine.setFocusPolicy(QtCore.Qt.NoFocus)
			self.nappi_jalkine.setText("Jalkine")
			self.nappi_jalkine.clicked.connect(lambda t: self.nappia_painettu("Jalkine"))
			# Härpäke
			self.nappi_harpake = QtWidgets.QPushButton(self)
			self.nappi_harpake.setGeometry(QtCore.QRect(*NAPPI_HARPAKE))
			self.nappi_harpake.setFocusPolicy(QtCore.Qt.NoFocus)
			self.nappi_harpake.setText("Härpäke")
			self.nappi_harpake.clicked.connect(lambda t: self.nappia_painettu("Härpäke"))

		# Esikatseltava tavara
		self.tavara = priluokat.Varuste()
		self.varustetietokanta = priluokat.Varustetietokanta()
		self.varustetietokanta.lue_tiedostosta("varustetietokanta.json")
		self.filtteroidyt_tavarat = self.varustetietokanta.varustelista
		self.paivita_varustelista()
		self.paivita_tarkastuskentta()
		self.tavaragridi = Tavaragridi(self, TAVARAGRID, [], self.tiedot_kartan_varusteesta)
		# Näytä tavaran tiedot pikku ruudussa
		self.tavaralista.currentIndexChanged.connect(self.paivita_tarkastuskentta)

		# Kartat
		self.karttatietokanta = priluokat.Karttatietokanta()
		self.karttatietokanta.lue_tiedostosta("karttatietokanta.json", self.varustetietokanta)
		self.kartta = priluokat.Kartta()

		# Karttamuokkauksen laabeli
		self.label_tavaralista = QtWidgets.QLabel(self)
		self.label_tavaralista.setGeometry(QtCore.QRect(*LABERL_KARTTA))
		self.label_tavaralista.setText("Kartan nimi (esim. 18-3)")
		# Kartan syöttökenttä
		self.karttakentta = QtWidgets.QLineEdit(self)
		self.karttakentta.setGeometry(QtCore.QRect(*KARTTAKENTTA))
		self.karttakentta.textChanged.connect(self.etsi_kartan_tiedot)
		# Nappi lisääpoista kartta
		self.nappi_kartta = QtWidgets.QPushButton(self)
		self.nappi_kartta.setGeometry(QtCore.QRect(*NAPPI_KARTTA))
		self.nappi_kartta.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.nappi_kartta.setFocusPolicy(QtCore.Qt.NoFocus)
		self.nappi_kartta.clicked.connect(self.lisaapoista_kartta)

	def etsi_kartan_tiedot(self):
		'''
		Etsi kartta karttatietokannasta ja päivitä
		tiedot relevantteihin kenttiin.
		'''
		self.kartta = priluokat.Kartta()
		self.karttakentta.setStyleSheet("background-color: salmon; color: black")
		kartan_nimi = "Normaali-"+self.karttakentta.text()
		print(f"Etsi kartta {kartan_nimi}")
		# Etsi nimeä vastaava kartta karttatietokannasta
		kartta = None
		# print([k.nimi for k in self.karttatietokanta.karttalista])
		for karttaehdokas in self.karttatietokanta.karttalista:
			if karttaehdokas.nimi == kartan_nimi:
				print(f"Mätsi")
				self.nappi_kartta.setText("-")
				self.nappi_kartta.setStyleSheet("background-color: salmon; color: black")
				kartta = karttaehdokas
				break
		# Kartta löytyi
		if kartta is not None:
			print("Löytyi")
			self.kartta = kartta
			self.karttakentta.setStyleSheet("background-color: #6bff84; color: black")
		else:
			print("Ei löytynyt")
			self.nappi_kartta.setText("+")
			self.nappi_kartta.setStyleSheet("background-color: #6bff84; color: black")
		self.tavaragridi.hide()
		self.tavaragridi = Tavaragridi(self, TAVARAGRID, self.kartta.droppaa, self.tiedot_kartan_varusteesta)

	def lisaapoista_kartta(self):
		'''
		Lisää kartta tietokantaan tai poista kartta tietokannasta.
		'''
		# Käy tietokanta läpi ja yritä poistaa kartta sieltä
		if self.nappi_kartta.text() == "-":
			for k,kartta in enumerate(self.karttatietokanta.karttalista):
				if kartta.nimi == self.kartta.nimi:
					print(f"Poista {kartta.nimi} karttatietokannasta")
					self.karttatietokanta.karttalista.pop(k)
					self.karttakentta.setStyleSheet("background-color: salmon; color: black")
					self.nappi_kartta.setStyleSheet("background-color: #6bff84; color: black")
					self.nappi_kartta.setText("+")
					self.kartta = priluokat.Kartta()
					self.tavaragridi.hide()
					self.tavaragridi = Tavaragridi(self, TAVARAGRID, self.kartta.droppaa, self.tiedot_kartan_varusteesta)
					break
		# Jos karttaa ei poistettu, se varmaan pitää lisätä uutena tietokantaanm
		else:
			print(f"Lisää karttatietokantaan")
			kartan_osat = self.karttakentta.text().split("-")
			if len(kartan_osat) == 2:
				try:
					maailma = int(kartan_osat[0])
					kartta  = int(kartan_osat[1])
					self.kartta = priluokat.Kartta(maailma=maailma, kartta=kartta)
					print(f"Lisää {self.kartta.nimi} tietokantaan")
					self.karttatietokanta.karttalista.append(self.kartta)
					self.karttakentta.setStyleSheet("background-color: #6bff84; color: black")
					self.nappi_kartta.setStyleSheet("background-color: salmon; color: black")
					self.nappi_kartta.setText("-")
				except ValueError:
					print("Kartan nimi on huono")
			else:
				print("Kartan nimi on huono")

	def filtteroi_tietokanta(self):
		'''
		Filtteröi tietokanta annettujen hakukriteereiden perusteella.
		'''
		self.filtteroidyt_tavarat = self.varustetietokanta.filtteroi(self.filtterit)
		self.paivita_varustelista()

	def paivita_varustelista(self):
		varustenimet = [a.nimi for a in self.filtteroidyt_tavarat]
		self.tavaralista.clear()
		print("putsattu")
		for nimi in varustenimet:
			# print(nimi)
			self.tavaralista.addItem(nimi)
		print("Lisätty")

	def paivita_tarkastuskentta(self):
		'''
		Päivitä tarkastustavaran tiedot tarkastuskenttääm
		(jotta saa luntittua ID:n ymv)
		'''
		print("Päivitä tarkastuskenttä")
		valittu = self.tavaralista.currentIndex()
		if valittu >= 0:
			self.tavara = self.filtteroidyt_tavarat[valittu]
			self.tarkistus_tavaratiedot.setText(str(self.filtteroidyt_tavarat[valittu]))
			tavarakuva = "./Kuvat/Varusteet/{:d}.png".format(self.filtteroidyt_tavarat[valittu].id)
			ikoni = kuva_pixmapiksi(tavarakuva, (TARKISTUSTAVARA[2],TARKISTUSTAVARA[3]))
			if ikoni is not None:
				self.tarkistustavara.setIcon(ikoni)
			else:
				self.tarkistustavara.setIcon(QtGui.QIcon())

	def paivita_varinapit(self, vari):
		'''
		Päivitä värinappien statukset ja filtteröintikriteerit.
		'''
		# Flippaa väri
		print(f"Päivitä värinapit")
		print(f"{vari} {self.varistatukset[vari]}")
		self.varistatukset[vari] = not(self.varistatukset[vari])
		print(f"-> {vari} {self.varistatukset[vari]}")
		# Resetoi värifiltterivalikoima
		self.filtterit["Väri"] = []
		# Kaikki napit harmaaksi
		self.varinappi_sini.setStyleSheet("background-color: #53778c")
		self.varinappi_pronssi.setStyleSheet("background-color: #8c5332")
		self.varinappi_hopea.setStyleSheet("background-color: #73798c")
		self.varinappi_kulta.setStyleSheet("background-color: #8c8958")
		self.varinappi_violetti.setStyleSheet("background-color: #6b3c8c")
		self.varinappi_punainen.setStyleSheet("background-color: #8c1a2b")
		# Sininen kirkkaaksi
		if self.varistatukset["Sininen"]:
			self.filtterit["Väri"].append(priluokat.SININEN)
			self.varinappi_sini.setStyleSheet("background-color: #94d2f8")
		# Pronssi kirkkaaksi
		if self.varistatukset["Pronssi"]:
			self.filtterit["Väri"].append(priluokat.PRONSSI)
			self.varinappi_pronssi.setStyleSheet("background-color: #e58852")
		# Hopea kirkkaaksi
		if self.varistatukset["Hopea"]:
			self.filtterit["Väri"].append(priluokat.HOPEA)
			self.varinappi_hopea.setStyleSheet("background-color: #afb7d4")
		# Kulta kirkkaaksi
		if self.varistatukset["Kulta"]:
			self.filtterit["Väri"].append(priluokat.KULTA)
			self.varinappi_kulta.setStyleSheet("background-color: #f8f29d")
		# Violetti kirkkaaksi
		if self.varistatukset["Violetti"]:
			self.filtterit["Väri"].append(priluokat.VIOLETTI)
			self.varinappi_violetti.setStyleSheet("background-color: #af62e5")
		# Punainen kirkkaaksi
		if self.varistatukset["Punainen"]:
			self.filtterit["Väri"].append(priluokat.PUNAINEN)
			self.varinappi_punainen.setStyleSheet("background-color: #e32a45")
		# Filtteröi tavarat
		self.filtteroi_tietokanta()

	def nappia_painettu(self, tyyppi):
		'''
		Tavaran tyyppikriteeriä päivitetty.
		'''
		# Lisää/poista tyyppi sallittujen listasta
		if self.filtterit["Tyyppi"] is None:
			self.filtterit["Tyyppi"] = []
		if tyyppi not in self.filtterit["Tyyppi"]:
			self.filtterit["Tyyppi"].append(tyyppi)
		else:
			self.filtterit["Tyyppi"].remove(tyyppi)
		# Päivitä nappien värit
				# Kaikki napit harmaiksi
		self.nappi_miekka.setStyleSheet("background-color: #31363b")
		self.nappi_keihas.setStyleSheet("background-color: #31363b")
		self.nappi_kirves.setStyleSheet("background-color: #31363b")
		# ----------------------------------------------------------
		self.nappi_nyrkki.setStyleSheet("background-color: #31363b")
		self.nappi_jousi.setStyleSheet("background-color: #31363b")
		self.nappi_sauva.setStyleSheet("background-color: #31363b")
		# ----------------------------------------------------------
		self.nappi_kilpi.setStyleSheet("background-color: #31363b")
		self.nappi_panssari.setStyleSheet("background-color: #31363b")
		self.nappi_hattu.setStyleSheet("background-color: #31363b")
		# ----------------------------------------------------------
		self.nappi_jalkine.setStyleSheet("background-color: #31363b")
		self.nappi_harpake.setStyleSheet("background-color: #31363b")
		
		if "Miekka" in self.filtterit["Tyyppi"]:
			self.nappi_miekka.setStyleSheet("background-color: #6bff84; color: black")
		if "Keihäs" in self.filtterit["Tyyppi"]:
			self.nappi_keihas.setStyleSheet("background-color: #6bff84; color: black")
		if "Kirves" in self.filtterit["Tyyppi"]:
			self.nappi_kirves.setStyleSheet("background-color: #6bff84; color: black")
		if "Nyrkki" in self.filtterit["Tyyppi"]:
			self.nappi_nyrkki.setStyleSheet("background-color: #6bff84; color: black")
		if "Jousi" in self.filtterit["Tyyppi"]:
			self.nappi_jousi.setStyleSheet("background-color: #6bff84; color: black")
		if "Taikasauva" in self.filtterit["Tyyppi"]:
			self.nappi_sauva.setStyleSheet("background-color: #6bff84; color: black")
		if "Kilpi" in self.filtterit["Tyyppi"]:
			self.nappi_kilpi.setStyleSheet("background-color: #6bff84; color: black")
		if "Panssari" in self.filtterit["Tyyppi"]:
			self.nappi_panssari.setStyleSheet("background-color: #6bff84; color: black")
		if "Päähine" in self.filtterit["Tyyppi"]:
			self.nappi_hattu.setStyleSheet("background-color: #6bff84; color: black")
		if "Jalkine" in self.filtterit["Tyyppi"]:
			self.nappi_jalkine.setStyleSheet("background-color: #6bff84; color: black")
		if "Härpäke" in self.filtterit["Tyyppi"]:
			self.nappi_harpake.setStyleSheet("background-color: #6bff84; color: black")
		# Filtteröi tavarat
		self.filtteroi_tietokanta()

	def tiedot_kartan_varusteesta(self, varuste):
		if type(varuste) is priluokat.Varuste and varuste in self.kartta.droppaa:
			print(f"Poista {varuste.nimi} kartan {self.kartta.nimi} dropeista")
			self.kartta.droppaa.remove(varuste)
		else:
			print(f"Lisää {self.tavara.nimi} kartan {self.kartta.nimi} droppeihin")
			if self.tavara not in self.kartta.droppaa:
				self.kartta.droppaa.append(self.tavara)
				self.tavara.droppaa.append(self.kartta)
		self.etsi_kartan_tiedot()
		self.karttatietokanta.tallenna("karttatietokanta.json")
		self.varustetietokanta.tallenna("varustetietokanta.json")

if __name__ == "__main__":
	app = QtWidgets.QApplication([])
	ikkuna = Paaikkuna()
	ikkuna.show()

	sys.exit(app.exec_())