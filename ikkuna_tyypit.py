'''
Ikkuna tavaroiden tyyppien määrittelyyn.
'''

import os
import sys
import shutil
import luokat_perus as priluokat
from PIL import Image, ImageQt
from PyQt5 import Qt, QtCore, QtWidgets, QtGui

IKKUNAMITAT = (1000,500)
MARGINAALIT = (10,10)

TAVARALISTA     = (MARGINAALIT[0], MARGINAALIT[0], 200, 50)
TARKISTUSTAVARA = (TAVARALISTA[0], TAVARALISTA[1]+TAVARALISTA[3], 200, 200)
TARKISTUSKENTTA = (TARKISTUSTAVARA[0], TARKISTUSTAVARA[1]+TARKISTUSTAVARA[3], TARKISTUSTAVARA[2], TARKISTUSTAVARA[3])

NAPPI_MIEKKA    = (TARKISTUSTAVARA[0]+TARKISTUSTAVARA[2], TARKISTUSTAVARA[1], 100, 50)
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

		# Tavaralista
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
			self.nappi_sauva.setText("Taikasauva")
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

		# Määritettävä tavara
		self.tavara = priluokat.Varuste()
		self.varustetietokanta = priluokat.Varustetietokanta()
		self.lataa_tietokanta()

		# Näytä tavaran tiedot pikku ruudussa
		self.tavaralista.currentIndexChanged.connect(self.paivita_tarkastuskentta)

	def lataa_tietokanta(self):
		'''
		Lataa tietokannan tietokantatiedostosta.
		'''
		self.varustetietokanta.lue_tiedostosta("varustetietokanta.json")
		varustenimet = [a.nimi for a in self.varustetietokanta.varustelista]
		print(varustenimet)
		self.tavaralista.clear()
		print("putsattu")
		for nimi in varustenimet:
			print(nimi)
			self.tavaralista.addItem(nimi)
		print("Lisätty")

	def paivita_kuvatiedosto(self):
		# tavarakuva = f"./Kuvat/Soubi/{self.tavara.id}.png"
		tavarakuva = self.tavaran_kuvakentta.text()
		if len(tavarakuva):
			# Jos tavara vedetty tekstikenttään, siinä on koko polku hassulla etujutulla. Siivoa.
			if "file://" in tavarakuva:
				tavarakuva = tavarakuva[7:]
			# Muuten varmaan pelkkä tiedostonimi, .png:llä tai ilman
			else:
				tavarakuva = "./Kuvat/Soubi/"+self.tavaran_kuvakentta.text()+"{}".format(".png"*(".png" not in tavarakuva))
			ikoni = kuva_pixmapiksi(tavarakuva, (TAVARANAPPI[2],TAVARANAPPI[3]))
			if ikoni is not None:
				self.tavaranappi.setIcon(ikoni)
			self.tavarakuva = tavarakuva

	def paivita_tarkastuskentta(self):
		'''
		Päivitä tarkastustavaran tiedot tarkastuskenttääm
		(jotta saa luntittua ID:n ymv)
		'''
		print("Päivitä tarkastuskenttä")
		valittu = self.tavaralista.currentIndex()
		if valittu >= 0:
			self.tavara = self.varustetietokanta.varustelista[valittu]
			self.tarkistus_tavaratiedot.setText(str(self.varustetietokanta.varustelista[valittu]))
			tavarakuva = "./Kuvat/Varusteet/{:d}.png".format(self.varustetietokanta.varustelista[valittu].id)
			self.paivita_napit(self.varustetietokanta.varustelista[valittu].tyyppi)
			ikoni = kuva_pixmapiksi(tavarakuva, (TARKISTUSTAVARA[2],TARKISTUSTAVARA[3]))
			if ikoni is not None:
				self.tarkistustavara.setIcon(ikoni)
			else:
				self.tarkistustavara.setIcon(QtGui.QIcon())

	def nappia_painettu(self, tyyppi):
		'''
		Muuta esineen tyyppi annetun sorttiseksi.
		'''
		if len(self.tavara.nimi):
			self.tavara.tyyppi = tyyppi
			print(f"Tavaran tyypiksi asetettu {tyyppi}")
			self.tallenna()
			self.paivita_napit(tyyppi)
		else:
			self.paivita_napit("")

	def paivita_napit(self, tyyppi):
		'''
		Päivitä nappien värit.
		'''
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
		
		if tyyppi == "Miekka":
			self.nappi_miekka.setStyleSheet("background-color: #6bff84")
		if tyyppi == "Keihäs":
			self.nappi_keihas.setStyleSheet("background-color: #6bff84")
		if tyyppi == "Kirves":
			self.nappi_kirves.setStyleSheet("background-color: #6bff84")
		if tyyppi == "Nyrkki":
			self.nappi_nyrkki.setStyleSheet("background-color: #6bff84")
		if tyyppi == "Jousi":
			self.nappi_jousi.setStyleSheet("background-color: #6bff84")
		if tyyppi == "Taikasauva":
			self.nappi_sauva.setStyleSheet("background-color: #6bff84")
		if tyyppi == "Kilpi":
			self.nappi_kilpi.setStyleSheet("background-color: #6bff84")
		if tyyppi == "Panssari":
			self.nappi_panssari.setStyleSheet("background-color: #6bff84")
		if tyyppi == "Päähine":
			self.nappi_hattu.setStyleSheet("background-color: #6bff84")
		if tyyppi == "Jalkine":
			self.nappi_jalkine.setStyleSheet("background-color: #6bff84")
		if tyyppi == "Härpäke":
			self.nappi_harpake.setStyleSheet("background-color: #6bff84")

	def tallenna(self):
		'''
		Tallenna tietokanta.
		'''
		print(f"Tallenna tietokanta")
		self.varustetietokanta.tallenna("varustetietokanta.json")
		print(f"Tallennettu")

if __name__ == "__main__":
	app = QtWidgets.QApplication([])
	ikkuna = Paaikkuna()
	ikkuna.show()

	sys.exit(app.exec_())