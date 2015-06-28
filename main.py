import sys
import random
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.phonon import Phonon
class ventana_principal(QMainWindow):
	def __init__(self):
		super().__init__()
		self.metadata = Phonon.MediaObject(self)
		self.iniciar_gui()
		
	def iniciar_gui(self):
		#Propiedades de la ventana
		dimensiones = alto,ancho = 700,450
		posicion = x,y = 200,89
		self.icono = QIcon("graficos/icono_principal.ico")
		self.setIconSize(QSize(100,100))
		self.setWindowIcon(self.icono)
		self.setGeometry(*posicion+dimensiones)
		self.setObjectName("ventana_principal")
		self.setWindowTitle("PyShire")
		self.setMaximumSize(alto,ancho)
		self.setMinimumSize(alto,ancho)
		
		#Variable de deteccion secundaria de estado playing
		self.estado_reproduccion = False
		self.estado_medio = False
		#Inicio de formateo de ventana
		#self.setWindowFlags(Qt.FramelessWindowHint)#ANULAR BORDES
		self.setWindowFlags(Qt.WindowMinimizeButtonHint)#Dar boton cerrar/minimizar
		
		#Reproductor
		self.reproductor = Phonon.AudioOutput(Phonon.MusicCategory,self)#SE ASIGNA EL REPRODUCTOR
		self.archivo = Phonon.MediaObject(self)
		self.archivo.tick.connect(self.tiempo) #reloj de duracion
		self.archivo.stateChanged.connect(self.detector_estado)
		Phonon.createPath(self.archivo,self.reproductor)#Inicio de conexion con el objeto y reproductor
		
		#Base de datos canciones
		self.CANCIONES_MEMORIA = {}
		
		#Asignacion de estilos y activacion de elementos
		with open("tema_1.css") as estilo:self.setStyleSheet(estilo.read())
		self.lista_reproduccion_1()
		self.graficos()#Inicio de graficos
		self.botones()
		self.menus()
		
		
		#Slot de interaccion con el reproductor:  (A partir de aca se puede interactuar con la base de datos)
		
		
		self.agregar_cancion_lista("cancion.mp3") #FUNCION AGREGAR CANCION
		
		
		
		
		###################################################
		self.show() #Mostrar la ventana luego de dibujar todo / para no producir retardos.
	"""
	def mousePressEvent(self, event):
		self.offset = event.pos()
	
	def mouseMoveEvent(self, event):
		x=event.globalX()
		y=event.globalY()
		x_w = self.offset.x()
		y_w = self.offset.y()
		self.move(x-x_w, y-y_w)
	"""
	def seleccion_cancion_lista(self,y):
		if self.estado_reproduccion == True:
			self.archivo.stop()
			self.estado_reproduccion = False
			sour = Phonon.MediaSource((self.CANCIONES_MEMORIA[self.caja_1.currentIndex().row()]))
			self.archivo.setCurrentSource(sour)
			self.play_musica()
			self.estado_medio = True
		else:
			self.estado_medio = True
			sour = Phonon.MediaSource((self.CANCIONES_MEMORIA[self.caja_1.currentIndex().row()]))
			self.archivo.setCurrentSource(sour)
			self.play_animacion_pop()
			self.play_musica()
	
	def salir(self):
		mensaje = QMessageBox.question(self,"Confimación","Desea realmente salir?",QMessageBox.No|QMessageBox.Yes)
		if mensaje == QMessageBox.Yes:self.close()
		
	def graficos(self):
		#TITULO "PYSHIRE"
		self._titulo_principal = QLabel("PyShire",self)
		self._titulo_principal.move(570,0)
		self._titulo_principal.setFixedSize(140,50)
		self._titulo_principal.setObjectName("titulo_principal")
		self.ico_logo_shire = QPixmap("graficos/logo_cara.png")
		
		#LOGO DE CHESHIRE
		self.ojo_imagen = QPixmap("graficos/shire/ojo.png")
		self.cara_imagen = QPixmap("graficos/shire/cara.png")		
		self.cara = QLabel(self)
		self.cara.setPixmap(self.cara_imagen)
		self.cara.setScaledContents(True)
		self.cara.setGeometry(600,384,100,70)
		mensajes = ["jijiji","Hola","No me clickees!","Dulce musica.."]
		self.cara.setToolTip(random.choice(mensajes))
		self.ojo = QLabel(self)
		self.ojo.setScaledContents(True)
		self.ojo.setPixmap(self.ojo_imagen)
		self.ojo.setScaledContents(True)
		self.ojo2  = QLabel(self)
		self.ojo2.setPixmap(self.ojo_imagen)
		self.ojo2.setScaledContents(True)
		dim = self.ojo.size()
		self.ojo.setGeometry(646,391,30,30)
		self.ojo2.setGeometry(619,391,30,30)
		def animacion_picara():
			self.mov_ojo = Animacion(self.ojo,"geometry",200,QRect(646,391,30,30),QRect(641,394,30,30))
			self.mov_ojo2 = Animacion(self.ojo2,"geometry",200,QRect(619,391,30,30),QRect(615,394,30,30))
			self.mov_cara = Animacion(self.cara,"geometry",120,QRect(600,384,100,70),QRect(600,389,100,70),3)
			def ini():
				self.mov_ojo.play_y_retroceder()
				self.mov_ojo2.play_y_retroceder()
				self.mov_cara.play_y_retroceder()
			ini()
		def animacion_ojo_saltones():
			self.mov_ojo = Animacion(self.ojo,"geometry",200,QRect(646,391,30,30),QRect(646-32,391-29,100,100))
			self.mov_ojo2 = Animacion(self.ojo2,"geometry",200,QRect(619,391,30,30),QRect(619-32,391-29,100,100))
			self.mov_cara = Animacion(self.cara,"geometry",120,QRect(600,384,100,70),QRect(600,384,100,100))
			def ini():
				self.mov_cara.play_y_retroceder()
				self.mov_ojo.play_y_retroceder()
				self.mov_ojo2.play_y_retroceder()
				self.mov_cara.play_y_retroceder()
			ini()
		animaciones = {"picaron":animacion_picara,"saltones":animacion_ojo_saltones}
		##########################################################
		
		self.cara.mousePressEvent = lambda c:animaciones[random.choice(list(animaciones))]()
		self.cara.show()
		self.ojo2.show()
		self.ojo.show()	
	
	def lista_reproduccion_1(self):
		#Caja de lista
		self.caja_1 = QTableWidget(0,7,self)
		caracteristicas = ["Titulo","Artista","Album","Año","Track","Encoding","Localizacion"]
		self.caja_1.setSelectionMode(QAbstractItemView.SingleSelection)
		self.caja_1.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.caja_1.setHorizontalHeaderLabels(caracteristicas)
		self.geometria = (660,60,0,300)
		self.caja_1.setGeometry(*self.geometria)
		self.estado = False
		self.icono_abrir = QPixmap("graficos/abrir_lista.png")
		self.abrir_lista = QLabel(self)
		self.abrir_lista.setPixmap(self.icono_abrir)
		self.abrir_lista.setScaledContents(True)
		self.geo = (660,180,60,60)
		self.abrir_lista.setGeometry(*self.geo)
		self.abrir_lista.show()
		self.abrir_lista.setToolTip("Abrir lista de reproduccion!")
		self.animacion_caja_abierta = Animacion(self.caja_1,"geometry",100,QRect(*self.geometria),QRect(30,60,660,300))
		self.animacion_caja_cerrada = Animacion(self.caja_1,"geometry",100,QRect(10,60,680,300),QRect(*self.geometria))
		self.animacion_boton_abrir1 = Animacion(self.abrir_lista,"geometry",90,QRect(*self.geo),QRect(-8,180,60,60))
		self.animacion_boton_abrir2 = Animacion(self.abrir_lista,"geometry",90,QRect(0,180,30,60),QRect(*self.geo))
		self.animacion_boton = Animacion(self.abrir_lista,"geometry",100,QRect(*self.geo),QRect(650,180,60,60))
		def anim():
			self.animacion_boton.play_y_retroceder()
		def abrir():
			if self.estado == True:
				self.animacion_caja_cerrada.play()
				self.animacion_boton_abrir2.play()
				self.abrir_lista.setToolTip("Abrir lista de reproduccion!")
				self.estado = False
			else:
				self.animacion_caja_abierta.play()
				self.animacion_boton_abrir1.play()
				self.abrir_lista.setToolTip("Cerrar lista de reproduccion!")
				self.estado = True
		self.abrir_lista.mousePressEvent = lambda c:abrir()
		#self.abrir_lista.mouseReleaseEvent = lambda c:anim()
		self.caja_1.horizontalScrollBar().setStyleSheet("background-color:#FFFFFF")
		self.caja_1.setObjectName("lista_reproduccion")
		self.caja_1.itemDoubleClicked.connect(self.seleccion_cancion_lista)
		self.caja_1.setEditTriggers(QAbstractItemView.NoEditTriggers)
	
		self.caja_1.show()
	
	def agregar_cancion_lista(self,direccion):
		cantidad_actual = self.caja_1.rowCount()
		columna,cuenta = self.caja_1.insertRow(cantidad_actual),0
		for i in self.obtener_metadatos(direccion):
			c = QTableWidgetItem(str(i))
			self.caja_1.setItem(cantidad_actual,cuenta,c)
			cuenta += 1
		self.CANCIONES_MEMORIA[cantidad_actual] = direccion
	
	def menus(self):
		#MENU PRINCIPAL
		self.menu = self.menuBar()
		self.menu.setObjectName("menu_principal")
		
		#Menu de "Archivo"
		self.menu_archivo = self.menu.addMenu("Archivo")
		self.menu_archivo.setObjectName("item_de_menu")
		self.boton_abrir = self.menu_archivo.addAction("Abrir").setShortcut("ctrl+a")
		self.accion_salir = QAction("Salir",self)
		self.accion_salir.setShortcut("Ctrl+s")
		self.accion_salir.triggered.connect(self.salir)
		self.boton_salir = self.menu_archivo.addAction(self.accion_salir)
		
		#Menu "Buscar"
		self.menu_opciones = self.menu.addMenu("Opciones")
		self.menu_opciones.setObjectName("item_de_menu")
		self.boton_buscar_musica = self.menu_opciones.addAction("Buscar musica!")
		self.boton_buscar_musica.setObjectName("item_de_menu")
		
		#Menu "Ayuda"
		def acerca_de():
			dialogo = Acerca_de()
			dialogo.exec_()
		self.menu_ayuda = self.menu.addMenu("Ayuda")
		self.menu_ayuda.setObjectName("item_de_menu")
		self.boton_acerca_de = self.menu_ayuda.addAction("Acerca de..",acerca_de)
		self.boton_acerca_de.setObjectName("boton_menu")
			
		self.menu.show()#Inicio de menus
		self.menu.setFixedSize(390,30)
	
	def botones(self):
		#BOTONES Y PANEL DE REPRODUCCION
		self.slider = Phonon.SeekSlider(self)#SE ASIGNA EL SLIDER
		self.slider.setMediaObject(self.archivo)
		self.slider.setObjectName("barra_progreso")
		self.slider.setGeometry(170,330,390,100)
		
		#SLIDER DE VOLUMEN
		self.volumen = Phonon.VolumeSlider(self)
		self.volumen.setAudioOutput(self.reproductor)
		self.volumen.setGeometry(161,393,100,50)
		self.volumen.setObjectName("slider_volumen")
		self.volumen.setIconSize(QSize(0,0))
		self.volumen.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
		self.volumen.setToolTip("Subir/Bajar el volumen!")
		#Reloj de cancion
		self.tiempo_cancion = QLabel("00:00 / 00:00",self)
		self.tiempo_cancion.move(570,365)
		self.tiempo_cancion.setObjectName("tiempo_cancion")
		
		#################################BOTON PLAY
		self.icono_play = QPixmap("graficos/play.png")
		self.icono_pausa = QPixmap("graficos/pausa.png")
		self.icono_siguiente = QPixmap("graficos/siguiente_derecha.png")
		self.icono_anterior = QPixmap("graficos/anterior_izquierda.png")
		self.icono_stop = QPixmap("graficos/detener.png")
		self.boton_play = QLabel(self)
		self.boton_play.setToolTip("Play!")
		self.boton_play.setGeometry(340,395,46,46)
		self.boton_play.setPixmap(self.icono_play)
		self.boton_play.setScaledContents(True)
		self.animacion_play = Animacion(self.boton_play,"geometry",100,QRect(340,395,46,46),QRect(340-15,395-15,80,80))
		def evento_play():
			self.animacion_play.play_y_retroceder()
			self.play_musica()
		self.boton_play.mousePressEvent = lambda c:evento_play()
		
		#################################BOTON SIGUIENTE
		self.boton_siguiente = QLabel(self)
		self.boton_siguiente.setPixmap(self.icono_siguiente)
		self.boton_siguiente.setToolTip("Siguiente canción!")
		self.boton_siguiente.setScaledContents(True)
		self.boton_siguiente.setGeometry(386,398,40,40)
		self.animacion_siguiente = Animacion(self.boton_siguiente,"geometry",100,QRect(386,398,40,40),QRect(398,398,40,40))
		def evento_siguiente():
			self.animacion_siguiente.play_y_retroceder()
		self.boton_siguiente.mousePressEvent = lambda c:evento_siguiente()
		
		############################################BOTON ANTERIOR
		self.boton_anterior = QLabel(self)
		self.boton_anterior.setPixmap(self.icono_anterior)
		self.boton_anterior.setToolTip("Canción anterior!")
		self.boton_anterior.setScaledContents(True)
		self.boton_anterior.setGeometry(300,398,40,40)
		self.animacion_anterior = Animacion(self.boton_anterior,"geometry",100,QRect(300,398,40,40),QRect(292,398,40,40))
		def evento_anterior():
			self.animacion_anterior.play_y_retroceder()
		self.boton_anterior.mousePressEvent = lambda c:evento_anterior()
		self.boton_play.show()
		self.boton_siguiente.show()
		self.boton_anterior.show()
		self.buffer_de_deteccion1 = 0
		self.boton_play.show()
		self.tiempo_cancion.show()
	
	def obtener_metadatos(self,cancion):#EXTRACTOR DE METADATOS/METAGEN
			from mutagen.id3 import ID3
			audio = ID3(cancion)
			try:artista = audio["TPE1"]
			except:artista = "Desconocido"
			try:genero = audio["TCON"]
			except:genero = "Desconocido"
			try:	año = audio["TDRC"]
			except:año = "Desconocido"
			try:nombre = audio["TIT2"]
			except:nombre=cancion
			try:encoding = audio["TSSE"]
			except:encoding = "Desconocido"
			try:track = audio["TPOS"]
			except:track = ""
			url = cancion
			print (audio.pprint())
			return [nombre,artista,genero,año,track,encoding,url]	
	
	def detector_estado(self,estado):
		if estado == Phonon.ErrorState:
			error = QMessageBox.warning(self,"ERROR FATAL","Error de ejecucion!!")
		if estado == Phonon.PlayingState:
			print(self.archivo.metaData())
		if estado == Phonon.StoppedState:
			self.archivo.stop()
		if estado == Phonon.PausedState:
			self.estado_reproduccion = False
			self.boton_play.setPixmap(self.icono_play)
	
	def play_animacion_pop(self):
		self.animacion_play.play_y_retroceder()
	
	def pausa_musica():
		self.reproductor.pause()
	
	def detener_musica():
		self.reproductor.stop()
	
	def tiempo(self,tiempo):
		tiempo_que_queda = self.archivo.remainingTime()
		restante = QTime(0, (tiempo_que_queda / 60000) % 60, (tiempo_que_queda / 1000) % 60)
		actual = QTime(0, (tiempo / 60000) % 60, (tiempo / 1000) % 60)
		res = [str(restante.minute()),str(restante.second())]
		if res == ['0', '0']:
			if self.buffer_de_deteccion1 == 3:
				self.archivo.stop()
				self.boton_play.setPixmap(self.icono_play)
				self.play_animacion_pop()
				self.buffer_de_deteccion1 = 0
				self.estado_reproduccion = False
			self.buffer_de_deteccion1+=1
		self.tiempo_restante_actual = res
		segundos,segundo_actual =  ("0" + str(actual.second())),0
		minuto,minuto_actual =  ("0" + str(actual.minute())),0
		segundos_restante,segundo_restante = ("0"  +str(restante.second())),0
		minuto_restantes,minuto_restante  = ("0"  +str(restante.minute())),0
		if len(str(actual.second())) == 2:segundos_actual =  actual.second()
		else:segundos_actual = segundos
		if len(str(actual.minute())) == 2:minuto_actual = actual.minute()
		else:minuto_actual = minuto
		if len(str(restante.second())) ==1:segundo_restante = segundos_restante
		else:segundo_restante = restante.second()
		if len(str(restante.minute())) ==1:minuto_restante = minuto_restantes
		else:minuto_restante = restante.minute()
		
		self.tiempo_cancion.setText("%s:%s / %s:%s"%(minuto_actual,segundos_actual,minuto_restante,segundo_restante))
	
	def play_musica(self):
		if self.estado_medio == False:pass
		else:
			if self.estado_reproduccion == False:
				print("play")
				self.boton_play.setPixmap(self.icono_pausa)
				self.boton_play.setToolTip("Pausar!")
				self.estado_reproduccion = True
				self.archivo.play()
			else:
				self.estado_reproduccion = False
				self.boton_play.setToolTip("Play!")
				self.boton_play.setPixmap(self.icono_play)
				self.archivo.pause()
	
	def actualizar_lista_reproduccion(self,lista):
		for i in lista:self.caja_1.addItem(self.cancion_para_lista("icono",i,"c"))
		
	def crear_menu_emergente(self,en,menu):#Asignar un menu emergente sobre
		en.setContextMenuPolicy(Qt.CustomContextMenu)
		en.customContextMenuRequested.connect(menu)
		
	def cancion_para_lista(self,icono,nombre,direccion):
		self._cancion = QListWidgetItem(QIcon(icono),nombre)
		fuente_item = QFont("Italic",12)
		self._cancion.setFont(fuente_item)
		return self._cancion
	
	def menu1(self):
		menu = QMenu()
		menu.setObjectName("menu_emergente")
		menu.move(QCursor.pos())
		menu.show()
		with open("tema_1.css") as estilo:menu.setStyleSheet(estilo.read())
		menu.exec_()

class Animacion(QWidget):#Asignar una animacion geometryca Basica
	def __init__(self,objeto,tipo,duracion,inicio,fin,veces=1):
		self.objeto,self.tipo,self.duracion,self.inicio,self.fin,self.veces = objeto,tipo,duracion,inicio,fin,veces
	def iniciar(self,objeto,tipo,duracion,inicio,fin,veces):
		self.animacion = QPropertyAnimation(objeto,tipo)
		self.animacion.setLoopCount(veces)
		self.animacion.setDuration(duracion)
		self.animacion.setStartValue(inicio)
		self.animacion.setEndValue(fin)	
	def play(self):
		self.iniciar(self.objeto,self.tipo,self.duracion,self.inicio,self.fin,self.veces)
		self.animacion.start()
		self.animacion.finished.connect(self.play_y_retroceder)
	def play_y_retroceder(self):
		self.iniciar(self.objeto,self.tipo,self.duracion,self.inicio,self.fin,self.veces)
		self.animacion.start()
		self.animacion.finished.connect(lambda : self.retroceder())
	def retroceder(self):
		self.iniciar(self.objeto,self.tipo,self.duracion,self.fin,self.inicio,self.veces)
		self.animacion.start()
		self.animacion.finished.connect(lambda :self.animacion.stop())

class Acerca_de(QDialog):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Acerca de PyShire")
		self.dialogo()
	def dialogo(self):
		self.setWindowIcon(QIcon("graficos/icono_principal.ico"))
		self.setStyleSheet("background-color:#000000;border-radius:3px")
		self.logo = QLabel(self)
		cajah = QHBoxLayout(self)
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.logo.setPixmap(QPixmap("graficos/acerca.jpg"))
		self.logo.setScaledContents(True)
		self.logo.setGeometry(0,0,450,300)
		self.logo.setMaximumHeight(300)
		self.logo.setMaximumWidth(480)
		cajah.addWidget(self.logo)
	
		self.mousePressEvent = lambda c:self.close()
		self.logo.show()
		
		self.show()

if __name__ == "__main__":
	inicio = QApplication(sys.argv)#Inicio de aplicacion
	ventana_main = ventana_principal()
	sys.exit(inicio.exec_())
