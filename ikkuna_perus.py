'''
Ikkuna tavaroiden määrittelyyn.
'''

import os
import sys
import shutil
import time
import luokat_perus as priluokat
from PIL import Image, ImageQt
from PyQt5 import Qt, QtCore, QtWidgets, QtGui

os.environ['QT_IM_MODULE'] = 'fcitx' # japski-input

IKKUNAMITAT = (1000,500)
MARGINAALIT = (10,10)

TARKISTUSTAVARA = (MARGINAALIT[0], MARGINAALIT[1], 200, 200)
TAVARALISTA     = (TARKISTUSTAVARA[0], TARKISTUSTAVARA[1]+TARKISTUSTAVARA[3], 200, 50)
TARKISTUSKENTTA = (TAVARALISTA[0], TAVARALISTA[1]+TAVARALISTA[3], TAVARALISTA[2], 200)
TAVARANAPPI     = (TAVARALISTA[0]+TAVARALISTA[2], MARGINAALIT[1], 200, 200)
# Tavaran kuvanimen syöttö
KUVAKENTTA      = (TAVARANAPPI[0], TAVARANAPPI[1]+TAVARANAPPI[3], TAVARANAPPI[2], TAVARALISTA[3])

# Syöttökentät
# Tavaran nimi
NIMILABEL       = (TAVARANAPPI[0]+TAVARANAPPI[2]+MARGINAALIT[0], TAVARANAPPI[1], 200, 20)
NIMIKENTTA      = (NIMILABEL[0], NIMILABEL[1]+NIMILABEL[3], 200, 40)
# Tavaran tyyppi
TYYPPILABEL     = (NIMIKENTTA[0], NIMIKENTTA[1]+NIMIKENTTA[3], NIMILABEL[2], NIMILABEL[3])
TYYPPIKENTTA    = (TYYPPILABEL[0], TYYPPILABEL[1]+TYYPPILABEL[3], NIMIKENTTA[2], NIMIKENTTA[3])
# Tavaran laatu
LAATULABEL      = (TYYPPIKENTTA[0], TYYPPIKENTTA[1]+TYYPPIKENTTA[3], NIMILABEL[2], NIMILABEL[3])
LAATURUKSI      = (LAATULABEL[0], LAATULABEL[1]+LAATULABEL[3], 30, 30)
LAATUTEKSI      = (LAATURUKSI[0]+LAATURUKSI[2], LAATURUKSI[1], LAATULABEL[2]-LAATURUKSI[2], LAATURUKSI[3])
# Tavaran leveli
LEVELILABEL     = (LAATULABEL[0], LAATURUKSI[1]+LAATURUKSI[3], NIMILABEL[2], NIMILABEL[3])
LEVELIKENTTA    = (LEVELILABEL[0], LEVELILABEL[1]+LEVELILABEL[3], NIMIKENTTA[2], NIMIKENTTA[3])
# Tavaran aliakset
ALIASLABEL     = (LEVELILABEL[0], LEVELIKENTTA[1]+LEVELIKENTTA[3], NIMILABEL[2], NIMILABEL[3])
ALIASKENTTA    = (ALIASLABEL[0], ALIASLABEL[1]+ALIASLABEL[3], NIMIKENTTA[2]-50, NIMIKENTTA[3])
ALIASNAPPI     = (ALIASKENTTA[0]+ALIASKENTTA[2], ALIASKENTTA[1], NIMIKENTTA[2]-ALIASKENTTA[2], NIMIKENTTA[3])
# Tavaran värit
VARILABEL      = (ALIASKENTTA[0], ALIASKENTTA[1]+ALIASKENTTA[3], NIMILABEL[2], NIMILABEL[3])
VARI_SINI      = (VARILABEL[0], VARILABEL[1]+VARILABEL[3], int(NIMIKENTTA[2]/6), NIMIKENTTA[3])
VARI_PRONSSI   = (VARI_SINI[0]+VARI_SINI[2], VARI_SINI[1], int(NIMIKENTTA[2]/6), NIMIKENTTA[3])
VARI_HOPEA     = (VARI_PRONSSI[0]+VARI_PRONSSI[2], VARI_PRONSSI[1], int(NIMIKENTTA[2]/6), NIMIKENTTA[3])
VARI_KULTA     = (VARI_HOPEA[0]+VARI_HOPEA[2], VARI_HOPEA[1], int(NIMIKENTTA[2]/6), NIMIKENTTA[3])
VARI_VIOLETTI  = (VARI_KULTA[0]+VARI_KULTA[2], VARI_KULTA[1], int(NIMIKENTTA[2]/6), NIMIKENTTA[3])
VARI_PUNAINEN  = (VARI_VIOLETTI[0]+VARI_VIOLETTI[2], VARI_VIOLETTI[1], int(NIMIKENTTA[2]/6), NIMIKENTTA[3])
# Tavaran osaset
OSASLABEL      = (VARI_SINI[0], VARI_SINI[1]+VARI_SINI[3], NIMILABEL[2], NIMILABEL[3])
OSASKENTTA     = (OSASLABEL[0], OSASLABEL[1]+OSASLABEL[3], NIMIKENTTA[2]-100, NIMIKENTTA[3])
OSASMAARA      = (OSASKENTTA[0]+OSASKENTTA[2], OSASKENTTA[1], int(0.5*(NIMIKENTTA[2]-OSASKENTTA[2])), NIMIKENTTA[3])
OSASNAPPI      = (OSASMAARA[0]+OSASMAARA[2], OSASMAARA[1], int(0.5*(NIMIKENTTA[2]-OSASKENTTA[2])), NIMIKENTTA[3])

# Tuloskenttä
LABEL_TIEDOT    = (NIMILABEL[0]+NIMILABEL[2]+MARGINAALIT[0], NIMILABEL[1], IKKUNAMITAT[0]-MARGINAALIT[0]-NIMILABEL[0]-NIMILABEL[2]-MARGINAALIT[0], 20)
TAVARATIEDOT    = (LABEL_TIEDOT[0], LABEL_TIEDOT[1]+LABEL_TIEDOT[3], LABEL_TIEDOT[2], 200)

# Lisää listaan
LISAYSLABEL     = (TAVARATIEDOT[0], TAVARATIEDOT[1]+TAVARATIEDOT[3], TAVARATIEDOT[2], NIMILABEL[3])
LISAYSNAPPI     = (LISAYSLABEL[0], LISAYSLABEL[1]+LISAYSLABEL[3], LISAYSLABEL[2], NIMIKENTTA[3])

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

class Paaikkuna(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Tavaraselain")
		self.resize(IKKUNAMITAT[0], IKKUNAMITAT[1])
		self.setMinimumSize(IKKUNAMITAT[0], IKKUNAMITAT[1])
		self.setMaximumSize(IKKUNAMITAT[0], IKKUNAMITAT[1])
		self.setStyleSheet("background-color: #31363b")

		# Määritettävä tavara
		self.tavara = priluokat.Varuste()
		print(str(self.tavara))
		# Jo määritetyt tavarat
		self.tavarat = []
		self.tavaralista = QtWidgets.QComboBox(self)
		self.tavaralista.setGeometry(QtCore.QRect(*TAVARALISTA))
		# Esikatselu jo määritelly tavaralle
		self.tarkistustavara = QtWidgets.QPushButton(self)
		self.tarkistustavara.setGeometry(QtCore.QRect(*TARKISTUSTAVARA))
		self.tarkistustavara.setIconSize(QtCore.QSize(TARKISTUSTAVARA[2],TARKISTUSTAVARA[3]))
		self.tarkistustavara.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.tarkistustavara.setFocusPolicy(QtCore.Qt.NoFocus)

		# Tavaranappi
		self.tavarakuva = ""
		self.tavaranappi = QtWidgets.QPushButton(self)
		self.tavaranappi.setGeometry(QtCore.QRect(*TAVARANAPPI))
		self.tavaranappi.setIconSize(QtCore.QSize(TAVARANAPPI[2],TAVARANAPPI[3]))
		self.tavaranappi.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.tavaranappi.setFocusPolicy(QtCore.Qt.NoFocus)

		# Tekstikentät
		# Tavaran nimi: label
		self.label_tavaran_nimi = QtWidgets.QLabel(self)
		self.label_tavaran_nimi.setGeometry(QtCore.QRect(*NIMILABEL))
		self.label_tavaran_nimi.setText("Tavaran nimi")
		# Tavaran nimi: syöttökenttä
		self.tavaran_nimi = QtWidgets.QLineEdit(self)
		self.tavaran_nimi.setGeometry(QtCore.QRect(*NIMIKENTTA))
		self.tavaran_nimi.textChanged.connect(lambda t: self.paivita_tavaran_tiedot("Nimi"))

		# Tavaran tyyppi: label
		self.label_tavaran_tyyppi = QtWidgets.QLabel(self)
		self.label_tavaran_tyyppi.setGeometry(QtCore.QRect(*TYYPPILABEL))
		self.label_tavaran_tyyppi.setText("(Tavaran tyyppi)")
		# Tavaran tyyppi: syöttökenttä
		self.tavaran_tyyppi = QtWidgets.QLineEdit(self)
		self.tavaran_tyyppi.setGeometry(QtCore.QRect(*TYYPPIKENTTA))
		self.tavaran_tyyppi.textChanged.connect(lambda t: self.paivita_tavaran_tiedot("Tyyppi"))

		# Tavaran laatu: label
		self.label_tavaran_laatu = QtWidgets.QLabel(self)
		self.label_tavaran_laatu.setGeometry(QtCore.QRect(*LAATULABEL))
		self.label_tavaran_laatu.setText("Varuste vai palanen tmv")
		# Tavaran laatu: valitsin
		self.tavaran_laatu = QtWidgets.QCheckBox(self)
		self.tavaran_laatu.setGeometry(QtCore.QRect(*LAATURUKSI))
		self.tavaran_laatu.setChecked(True)
		self.teksti_tavaran_laatu = QtWidgets.QLabel(self)
		self.teksti_tavaran_laatu.setGeometry(QtCore.QRect(*LAATUTEKSI))
		self.teksti_tavaran_laatu.setText("Tavara")
		# self.tavaran_laatu.clicked.connect(self.vaihdalaatuteksti)
		self.tavaran_laatu.clicked.connect(lambda t: self.paivita_tavaran_tiedot("Laatu"))
		self.tavara.id = self.tavara.id | 0x080 # viides bitti ykköseksi (def. tavara)

		# Tavaran leveli: label
		self.label_tavaran_leveli = QtWidgets.QLabel(self)
		self.label_tavaran_leveli.setGeometry(QtCore.QRect(*LEVELILABEL))
		self.label_tavaran_leveli.setText("Vaadittu leveli")
		# Tavaran leveli: syöttökenttä
		self.tavaran_leveli = QtWidgets.QSpinBox(self)
		self.tavaran_leveli.setGeometry(QtCore.QRect(*LEVELIKENTTA))
		self.tavaran_leveli.setMinimum(0)
		self.tavaran_leveli.setMaximum(999)
		self.tavaran_leveli.valueChanged.connect(lambda t: self.paivita_tavaran_tiedot("Leveli"))

		# Tavaran alias: label
		self.label_tavaran_alias = QtWidgets.QLabel(self)
		self.label_tavaran_alias.setGeometry(QtCore.QRect(*ALIASLABEL))
		self.label_tavaran_alias.setText("Tavaran lempinimi")
		# Tavaran alias: syöttökenttä
		self.tavaran_alias = QtWidgets.QLineEdit(self)
		self.tavaran_alias.setGeometry(QtCore.QRect(*ALIASKENTTA))
		self.tavaran_alias.textChanged.connect(self.lisaapoista_alias)
		# Tavaran alias: nappi
		self.aliasnappi = QtWidgets.QPushButton(self)
		self.aliasnappi.setGeometry(QtCore.QRect(*ALIASNAPPI))
		self.aliasnappi.setFocusPolicy(QtCore.Qt.NoFocus)
		self.aliasnappi.setText("")
		# self.aliasnappi.clicked.connect(self.saada_alias)
		self.aliasnappi.clicked.connect(lambda t: self.paivita_tavaran_tiedot("Alias"))

		# Tavaran väri: label
		self.label_tavaran_vari = QtWidgets.QLabel(self)
		self.label_tavaran_vari.setGeometry(QtCore.QRect(*VARILABEL))
		self.label_tavaran_vari.setText("Tavaran väri")
		self.varikoodi = 0
		# Tavaran väri: nappi sini
		self.varinappi_sini = QtWidgets.QPushButton(self)
		self.varinappi_sini.setGeometry(QtCore.QRect(*VARI_SINI))
		self.varinappi_sini.setFocusPolicy(QtCore.Qt.NoFocus)
		self.varinappi_sini.setText("Si")
		self.varinappi_sini.setStyleSheet("background-color: #94d2f8")
		self.varinappi_sini.clicked.connect(lambda t: self.paivita_tavaran_tiedot("Väri-sininen"))
		# Tavaran väri: nappi pronssi
		self.varinappi_pronssi = QtWidgets.QPushButton(self)
		self.varinappi_pronssi.setGeometry(QtCore.QRect(*VARI_PRONSSI))
		self.varinappi_pronssi.setFocusPolicy(QtCore.Qt.NoFocus)
		self.varinappi_pronssi.setText("Pr")
		self.varinappi_pronssi.setStyleSheet("background-color: #e58852")
		self.varinappi_pronssi.clicked.connect(lambda t: self.paivita_tavaran_tiedot("Väri-pronssi"))
		# Tavaran väri: nappi hopea
		self.varinappi_hopea = QtWidgets.QPushButton(self)
		self.varinappi_hopea.setGeometry(QtCore.QRect(*VARI_HOPEA))
		self.varinappi_hopea.setFocusPolicy(QtCore.Qt.NoFocus)
		self.varinappi_hopea.setText("Ho")
		self.varinappi_hopea.setStyleSheet("background-color: #afb7d4")
		self.varinappi_hopea.clicked.connect(lambda t: self.paivita_tavaran_tiedot("Väri-hopea"))
		# Tavaran väri: nappi kulta
		self.varinappi_kulta = QtWidgets.QPushButton(self)
		self.varinappi_kulta.setGeometry(QtCore.QRect(*VARI_KULTA))
		self.varinappi_kulta.setFocusPolicy(QtCore.Qt.NoFocus)
		self.varinappi_kulta.setText("Ku")
		self.varinappi_kulta.setStyleSheet("background-color: #f8f29d")
		self.varinappi_kulta.clicked.connect(lambda t: self.paivita_tavaran_tiedot("Väri-kulta"))
		# Tavaran väri: nappi violetti
		self.varinappi_violetti = QtWidgets.QPushButton(self)
		self.varinappi_violetti.setGeometry(QtCore.QRect(*VARI_VIOLETTI))
		self.varinappi_violetti.setFocusPolicy(QtCore.Qt.NoFocus)
		self.varinappi_violetti.setText("Vi")
		self.varinappi_violetti.setStyleSheet("background-color: #af62e5")
		self.varinappi_violetti.clicked.connect(lambda t: self.paivita_tavaran_tiedot("Väri-violetti"))
		# Tavaran väri: nappi punainen
		self.varinappi_punainen = QtWidgets.QPushButton(self)
		self.varinappi_punainen.setGeometry(QtCore.QRect(*VARI_PUNAINEN))
		self.varinappi_punainen.setFocusPolicy(QtCore.Qt.NoFocus)
		self.varinappi_punainen.setText("Pu")
		self.varinappi_punainen.setStyleSheet("background-color: #e32a45")
		self.varinappi_punainen.clicked.connect(lambda t: self.paivita_tavaran_tiedot("Väri-punainen"))

		# Tavaran osat: label
		self.label_tavaran_osat = QtWidgets.QLabel(self)
		self.label_tavaran_osat.setGeometry(QtCore.QRect(*OSASLABEL))
		self.label_tavaran_osat.setText("Tarvitsee osiksi (id)")
		# Tavaran osa: syöttökenttä
		self.tavaran_osa = QtWidgets.QSpinBox(self)
		self.tavaran_osa.setGeometry(QtCore.QRect(*OSASKENTTA))
		self.tavaran_osa.setMinimum(0)
		self.tavaran_osa.setMaximum(0xFFF)
		self.tavaran_osa.valueChanged.connect(self.nappi_lisaapoista_osa)
		# Tavaran osa: lukumäärä
		self.tavaran_osamaara = QtWidgets.QSpinBox(self)
		self.tavaran_osamaara.setMinimum(0)
		self.tavaran_osamaara.setMaximum(999)
		self.tavaran_osamaara.setGeometry(QtCore.QRect(*OSASMAARA))
		# Tavaran osa: lisää tai poista
		self.tavaran_osanappi = QtWidgets.QPushButton(self)
		self.tavaran_osanappi.setGeometry(QtCore.QRect(*OSASNAPPI))
		self.tavaran_osanappi.setFocusPolicy(QtCore.Qt.NoFocus)
		self.tavaran_osanappi.setText("")
		self.tavaran_osanappi.setStyleSheet("background-color: #31363b")
		self.tavaran_osanappi.clicked.connect(lambda t: self.paivita_tavaran_tiedot("Osa"))

		# Kuvatiedoston asettaminen
		self.tavaran_kuvakentta = QtWidgets.QLineEdit(self)
		self.tavaran_kuvakentta.setGeometry(QtCore.QRect(*KUVAKENTTA))
		self.tavaran_kuvakentta.textChanged.connect(self.paivita_kuvatiedosto)
		self.tavaran_kuvakentta.setStyleSheet("background-color: black")

		# Tavaran tiedot
		# Label
		self.label_tavaran_nimi = QtWidgets.QLabel(self)
		self.label_tavaran_nimi.setGeometry(QtCore.QRect(*LABEL_TIEDOT))
		self.label_tavaran_nimi.setText("Syötettävän tavaran tiedot")
		# Tietoikkuna
		self.tavaratiedot = QtWidgets.QTextEdit(self)
		self.tavaratiedot.setGeometry(QtCore.QRect(*TAVARATIEDOT))
		self.tavaratiedot.setText("")
		self.tavaratiedot.setReadOnly(True)
		self.tavaratiedot.setAlignment(QtCore.Qt.AlignTop)
		self.tavaratiedot.setWordWrapMode(0)
		self.tavaratiedot.setStyleSheet("background-color: #31363b")

		# Tarkistustavaran tiedot
		self.tarkistus_tavaratiedot = QtWidgets.QTextEdit(self)
		self.tarkistus_tavaratiedot.setGeometry(QtCore.QRect(*TARKISTUSKENTTA))
		self.tarkistus_tavaratiedot.setText("")
		self.tarkistus_tavaratiedot.setReadOnly(True)
		self.tarkistus_tavaratiedot.setAlignment(QtCore.Qt.AlignTop)
		self.tarkistus_tavaratiedot.setWordWrapMode(0)
		self.tarkistus_tavaratiedot.setStyleSheet("background-color: #31363b")
		self.tavaralista.currentIndexChanged.connect(self.paivita_tarkastuskentta)

		# Lisää tavara listaan: label
		self.label_lisaa_tavara = QtWidgets.QLabel(self)
		self.label_lisaa_tavara.setGeometry(QtCore.QRect(*LISAYSLABEL))
		self.label_lisaa_tavara.setText("Lisää tavara")
		# Lisää tavara listaan: nappi
		self.nappi_lisaa_tavara = QtWidgets.QPushButton(self)
		self.nappi_lisaa_tavara.setGeometry(QtCore.QRect(*LISAYSNAPPI))
		self.nappi_lisaa_tavara.setFocusPolicy(QtCore.Qt.NoFocus)
		self.nappi_lisaa_tavara.setText("Lisää tavara listaan")
		self.nappi_lisaa_tavara.setStyleSheet("background-color: #31363b")
		self.nappi_lisaa_tavara.clicked.connect(self.lisaa_listaan)

	def paivita_kuvatiedosto(self):
		# tavarakuva = f"./Kuvat/Soubi/{self.tavara.id}.png"
		tavarakuva = self.tavaran_kuvakentta.text()
		if len(tavarakuva):
			tavarakuva = "./Kuvat/Soubi/"+self.tavaran_kuvakentta.text()+"{}".format(".png"*(".png" not in tavarakuva))
			ikoni = kuva_pixmapiksi(tavarakuva, (TAVARANAPPI[2],TAVARANAPPI[3]))
			if ikoni is not None:
				self.tavaranappi.setIcon(ikoni)
			self.tavarakuva = tavarakuva

	def vaihdalaatuteksti(self):
		if self.tavaran_laatu.isChecked():
			self.teksti_tavaran_laatu.setText("Tavara")
			self.tavaran_leveli.setMinimum(0)
			self.tavaran_leveli.setMaximum(999)
			self.tavaran_leveli.setStyleSheet("background-color: #31363b")
		else:
			self.teksti_tavaran_laatu.setText("Palanen")
			self.tavaran_leveli.setValue(0)
			self.tavaran_leveli.setMinimum(0)
			self.tavaran_leveli.setMaximum(0)
			self.tavaran_leveli.setStyleSheet("background-color: black")

	def nappi_lisaapoista_osa(self):
		'''
		Vaihda aliasnapin symbolia riippuen onko alias
		listattu (poista listasta) vai ei (lisää listaan).
		'''
		osa = self.tavaran_osa.value()
		vastaava_tavara = None
		for tavara in self.tavarat:
			if tavara.id == osa:
				vastaava_tavara = tavara
				break
		if vastaava_tavara is not None:
			if vastaava_tavara in [a[0] for a in self.tavara.tarvitsee]:
				self.tavaran_osanappi.setText("-")
				self.tavaran_osanappi.setStyleSheet("background-color: #6c2c2c")
			else:
				self.tavaran_osanappi.setText("+")
				self.tavaran_osanappi.setStyleSheet("background-color: #2c6c2c")
		else:
			self.tavaran_osanappi.setText("")
			self.tavaran_osanappi.setStyleSheet("background-color: #31363b")

	def lisaapoista_alias(self):
		'''
		Vaihda aliasnapin symbolia riippuen onko alias
		listattu (poista listasta) vai ei (lisää listaan).
		'''
		alias = self.tavaran_alias.text()
		if alias in self.tavara.aliakset:
			self.aliasnappi.setText("-")
			self.aliasnappi.setStyleSheet("background-color: #6c2c2c")
		elif len(alias):
			self.aliasnappi.setText("+")
			self.aliasnappi.setStyleSheet("background-color: #2c6c2c")
		else:
			self.aliasnappi.setText("")
			self.aliasnappi.setStyleSheet("background-color: #31363b")

	def saada_alias(self):
		'''
		Vaihda aliasnapin symbolia riippuen onko alias
		listattu (poista listasta) vai ei (lisää listaan).
		'''
		alias = self.tavaran_alias.text()
		if alias in self.tavara.aliakset:
			self.tavara.aliakset.remove(alias)
			self.tavaran_alias.setText("")
		elif len(alias):
			self.tavara.aliakset.append(alias)
		self.lisaapoista_alias()

	def paivita_vari(self, vari):
		'''
		Aseta värikoodi ja korosta valittu väri.
		'''
		self.varikoodi = 0
		# Harmaat
		self.varinappi_sini.setStyleSheet("background-color: #53778c")
		self.varinappi_pronssi.setStyleSheet("background-color: #8c5332")
		self.varinappi_hopea.setStyleSheet("background-color: #73798c")
		self.varinappi_kulta.setStyleSheet("background-color: #8c8958")
		self.varinappi_violetti.setStyleSheet("background-color: #6b3c8c")
		self.varinappi_punainen.setStyleSheet("background-color: #8c1a2b")
		# Sininen kirkkaaksi
		if vari == "sininen":
			self.varikoodi = priluokat.SININEN
			self.varinappi_sini.setStyleSheet("background-color: #94d2f8")
		# Pronssi kirkkaaksi
		elif vari == "pronssi":
			self.varikoodi = priluokat.PRONSSI
			self.varinappi_pronssi.setStyleSheet("background-color: #e58852")
		# Hopea kirkkaaksi
		elif vari == "hopea":
			self.varikoodi = priluokat.HOPEA
			self.varinappi_hopea.setStyleSheet("background-color: #afb7d4")
		# Kulta kirkkaaksi
		elif vari == "kulta":
			self.varikoodi = priluokat.KULTA
			self.varinappi_kulta.setStyleSheet("background-color: #f8f29d")
		# Violetti kirkkaaksi
		elif vari == "violetti":
			self.varikoodi = priluokat.VIOLETTI
			self.varinappi_violetti.setStyleSheet("background-color: #af62e5")
		# Punainen kirkkaaksi
		elif vari == "punainen":
			self.varikoodi = priluokat.PUNAINEN
			self.varinappi_punainen.setStyleSheet("background-color: #e32a45")
		# Kaikki kirkkaalle
		else:
			self.varinappi_sini.setStyleSheet("background-color: #94d2f8")
			self.varinappi_pronssi.setStyleSheet("background-color: #e58852")
			self.varinappi_hopea.setStyleSheet("background-color: #afb7d4")
			self.varinappi_kulta.setStyleSheet("background-color: #f8f29d")
			self.varinappi_violetti.setStyleSheet("background-color: #af62e5")
			self.varinappi_punainen.setStyleSheet("background-color: #e32a45")

	def paivita_tavaran_tiedot(self, muutettu_kentta):
		'''
		Päivitä tavaran tiedot syötettyjen tietojen perusteella.
		'muutettu_kentta' kertoo mitä tietoa pitää päivittää.
		'''
		# Säädä esineen nimi
		if muutettu_kentta == "Nimi":
			self.tavara.nimi = self.tavaran_nimi.text()
		# Säädä esineen tyyppi (miekka vai keihäs vai mikä)
		elif muutettu_kentta == "Tyyppi":
			self.tavara.tyyppi = self.tavaran_tyyppi.text()
		# Säädä esineen laatu
		elif muutettu_kentta == "Laatu":
			self.vaihdalaatuteksti()
			if self.tavaran_laatu.isChecked():
				self.tavara.id = self.tavara.id | 0x080 # viides bitti ykköseksi
			else:
				self.tavara.id = self.tavara.id & 0xF7F # viides bitti nollaksi
		# Säädä tarvittava leveli
		elif muutettu_kentta == "Leveli":
			self.tavara.leveli = self.tavaran_leveli.value()
		# Lisää tai poista lempinimi
		elif muutettu_kentta == "Alias":
			self.saada_alias()
		# Säädä osan väri
		elif "Väri" in muutettu_kentta:
			vari = muutettu_kentta.split("-")[-1]
			self.paivita_vari(vari)
			self.tavara.id = (0x0FF & self.tavara.id) | (self.varikoodi << 8) # päivitä neljä ekaa bittiä värikoodiksi
		# Lisää tai poista tieto osastarpeesta
		elif muutettu_kentta == "Osa":
			osa = self.tavaran_osa.value()
			vastaava_tavara = None
			for tavara in self.tavarat:
				if tavara.id == osa:
					vastaava_tavara = tavara
					break
			# Lisää
			if self.tavaran_osanappi.text() == "+":
				lukumaara = self.tavaran_osamaara.value()
				if vastaava_tavara is not None and lukumaara > 0:
					self.tavara.tarvitsee.append((vastaava_tavara, lukumaara))
					if (None, 0) in self.tavara.tarvitsee:
						self.tavara.tarvitsee.remove((None, 0))
			# Poista
			elif self.tavaran_osanappi.text() == "-" and vastaava_tavara is not None:
				for t,tavara in enumerate(self.tavara.tarvitsee):
					if tavara[0] is vastaava_tavara:
						d = self.tavara.tarvitsee.pop(t)
						break
			self.tavaran_osa.setValue(0)
			self.tavaran_osamaara.setValue(0)
		self.tavaratiedot.setText(str(self.tavara))
		st, arvot = self.tavara.dekryptaa_id()
		print(st)

	def paivita_tarkastuskentta(self):
		'''
		Päivitä tarkastustavaran tiedot tarkastuskenttääm
		(jotta saa luntittua ID:n ymv)
		'''
		valittu = self.tavaralista.currentIndex()
		if valittu >= 0:
			self.tarkistus_tavaratiedot.setText(str(self.tavarat[valittu]))

	def lisaa_listaan(self):
		'''
		Lisää tavara listaan jos se on validi
		'''
		if len(self.tavara.nimi) and self.tavara.id & 0xF00 > 0:
			self.tavara.korjaa_id(self.tavarat)
			self.tavarat.append(self.tavara)
			self.tavaralista.addItem(self.tavara.nimi)
			# Kopsaa kuva ID:n taakse oikeaan kansioon
			print(self.tavarakuva)
			print(f"./Kuvat/Varusteet/{self.tavara.id}.png")
			if len(self.tavarakuva) and len(self.tavarakuva.split(".png")) > 1 and os.path.exists(self.tavarakuva):
				shutil.copyfile(self.tavarakuva, f"./Kuvat/Varusteet/{self.tavara.id}.png")
			self.tavara = priluokat.Varuste()
			self.tavaratiedot.setText(str(self.tavara))
			self.nollaa_kentat()
		print(self.tavarat)

	def nollaa_kentat(self):
		'''
		Nollaa syöttökentät (uusi tavara)
		'''
		self.tavaran_nimi.setText("")
		self.tavaran_tyyppi.setText("")
		self.tavaran_laatu.setChecked(True)
		self.tavara.id = self.tavara.id | 0x080 # tavarabitti ykköseksi
		self.tavaran_leveli.setValue(0)
		self.tavaran_alias.setText("")
		self.tavaran_osa.setValue(0)
		self.tavaran_osamaara.setValue(0)
		self.tavaran_osanappi.setText("")
		self.varinappi_sini.setStyleSheet("background-color: #94d2f8")
		self.varinappi_pronssi.setStyleSheet("background-color: #e58852")
		self.varinappi_hopea.setStyleSheet("background-color: #afb7d4")
		self.varinappi_kulta.setStyleSheet("background-color: #f8f29d")
		self.varinappi_violetti.setStyleSheet("background-color: #af62e5")
		self.varinappi_punainen.setStyleSheet("background-color: #e32a45")

if __name__ == "__main__":
	app = QtWidgets.QApplication([])
	ikkuna = Paaikkuna()
	ikkuna.show()

	sys.exit(app.exec_())