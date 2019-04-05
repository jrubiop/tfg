#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

################################
# Importación de librerias
################################
import RPi.GPIO as GPIO
import time

# Libreria sensor temperatura
import Adafruit_DHT as DHT;

# Libreria LCD
import Adafruit_CharLCD as LCD;
###from Adafruit_CharLCD import Adafruit_CharLCD;

import sys;
import urllib;
import requests;

# desactivamos mensajes de error
GPIO.setwarnings(False);

# indicamos el uso de la identificacion BCM para los GPIO
GPIO.setmode(GPIO.BCM);

# Para activar log de ejecucion
LOG_ACTIVO = 1;
debug = 0;

###########################
# Definicion de funciones
###########################
def escribe_log(msg):
	global LOG_ACTIVO;
	
	if LOG_ACTIVO == 1:
		print msg;


def fin_programa(msg):
	global pantalla;
	
	# Desactiva el sensor
	#GPIO.output(pin_trigger, False);
	
	#GPIO.output(pin_circuito, False);
	
	# Liberando puertos
	GPIO.cleanup();
	
	# Limpia pantalla
	#pantalla.clear();
	
	if msg != '':
		print msg;
	print "Fin ----";
	
	# Fin programa
	sys.exit(1);
	

# ---------------------------
# Funciones para Led-RGB
# ---------------------------
def led_rgb_apagado():
	GPIO.output(pin_R, False);
	GPIO.output(pin_G, False);
	GPIO.output(pin_B, False);

def led_rgb_rojo():
	GPIO.output(pin_R, True);
	GPIO.output(pin_G, False);
	GPIO.output(pin_B, False);
	
def led_rgb_verde():
	GPIO.output(pin_R, False);
	GPIO.output(pin_G, True);
	GPIO.output(pin_B, False);
	
def led_rgb_azul():
	GPIO.output(pin_R, False);
	GPIO.output(pin_G, False);
	GPIO.output(pin_B, True);
	
	
def mide_temperatura():
	# Lee temperatura y humedad
	humedad, temperatura = DHT.read_retry(tipo_sensor, pin_temperatura);
	
	# Control errores -- ****

	datos = {'t': temperatura, 'h': humedad };
	return datos;
	
	
def mide_duracion():
	print "Midiendo duracion";
	
	# Inicializacion de tiempos
	ts_inicio 	= 0;
	ts_final	= 0;		

	# Inicializacion del sensor
	GPIO.output(pin_trigger, False);

	# Para 1 segundo para el sensor
	#time.sleep(1);
	time.sleep(0.5);
	print "Esperando 0.5 seg...";
	
	# Activa el sensor - envio señal
	GPIO.output(pin_trigger, True);
	print "enviando trigger...";

	# Espera envio de señal
	ts_espera = 10; # cantidad
	time.sleep(ts_espera * 10**-6); # en microsegundos
	print "Terminado esperar 10 microseg...";

	# Desactiva el sensor - parada
	GPIO.output(pin_trigger, False);
	print "Iniciando echo...";

	# Inicio lectura del echo
	while GPIO.input(pin_echo) == GPIO.LOW:
		ts_inicio = time.time();
	print "Fin echo...";

	# Fin lectura del echo
	while GPIO.input(pin_echo) == GPIO.HIGH:
		ts_final = time.time();
	print "Fin lectura...";
		
	# Calculo de distancia, lo que tarde en ir y volver la señal
	ts_duracion = ts_final - ts_inicio;
	
	# Tiempo devuelto
	return ts_duracion;


def calcula_velocidad_sonido():
	# Calculo de la velocidad del sonido en funcion de variables
	velocidad_sonido = 343;
	
	# Velocidad calculada
	return velocidad_sonido;


def calcula_distancia():
	
	# Midiendo temperatura y humedad
	datos_medicion = mide_temperatura();
	temperatura = datos_medicion['t'];
	humedad 	= datos_medicion['h'];
		
	# Velocidad del sonido en aire
	# Se calculara dinamicamente en funcion del ambiente (aereo, acuatico) y de las condiciones (presion, temperatura)
	velocidad_sonido = calcula_velocidad_sonido();
	# print "Velocidad Sonido: ", str(velocidad_sonido);
		
	# Calculo del tiempo de propagacion del echo
	ts_duracion = mide_duracion();
	
	# Calculo de distancia (en cm), lo que tarde en ir y volver la señal
	distancia =  ( ( ts_duracion * velocidad_sonido ) / 2) * 100;
	
	# Pintando resultados
	distancia 	=  round(distancia, 2);
	temperatura =  round(temperatura, 2);
	humedad 	=  round(humedad, 2);
	
	msg =  "Distancia  ==> ", str(distancia), " cm -- T: ", str(temperatura), " grados y humedad: ", str(humedad);
	escribe_log(msg);
	
	# Encender LED dependiendo de la distancia
	if distancia < 20:
		led_rgb_rojo();
	elif 20 <= distancia < 40:
		led_rgb_azul();
	else:
		led_rgb_verde();
	
	# Registrando datos
	#registra_datos();
	
	# Muestra datos
	muestra_datos(distancia, temperatura, humedad);


def muestra_datos(d, t, h ):
	
	global pantalla;
	
	pantalla.message('');
	pantalla.clear();
	
	#msg_pantalla = "D: ", str(d), " cm. T: ", str(t), " ºC. H: ", str(h);
	msg_pantalla = str(d) + "cm - " + str(t) + "C";
	#pantalla.set_cursor(0,0);
	pantalla.message(msg_pantalla);

	# Texto - fila 2
	str_fecha = time.strftime('%b %d %H:%M:%S\n');
	pantalla.set_cursor(1,1);
	pantalla.message(str_fecha);		
	

# -----------------------------------
# Funciones para registro de datos
# -----------------------------------
def registra_datos():
	#url_registra_datos = 'http://google.es';
	url_registra_datos = 'http://localhost/medidas.php';
	parametros = {'key1': 'value1', 'key2': 'value2'};
	datos = {'key1': 'value1', 'key2': 'value2'};
	
	try:
		#cabeceras = {'user-agent': 'my-app/0.0.1'}
		#headers=cabeceras
		
		# sesion = requests.Session()
		# sesion.get(...)
		
		#respuesta = requests.get(url_registra_datos, params=parametros)	
		respuesta = requests.post(url_registra_datos, data=datos);
		
		# respuesta.text
		# respuesta.content
		print 'STATUS:' , respuesta.status_code, ' -- HEADERS: ', respuesta.headers;
		
	except requests.exceptions.RequestException:
		print 'ERROR:----';


def comprueba_conexion(url):
	try:
		#url = "https://www.google.com";
		urllib.urlopen(url);
		status = 1;
	except:
		# Error de conexion
		status = 0;
	return status;





#######################
# Definicion de pines
#######################

# Definicion de pines para activacion de sistema
pin_led_on_off 	= 14;
pin_boton 		= 15;
pin_circuito 	= 18;

# Definicion de pin para sensor temperatura
pin_temperatura = 19;
tipo_sensor		= DHT.DHT22; # DHT11

# Definicion de pines para la pantalla
pin_bl = 4;
pin_rs = 5;
pin_en = 6;

pin_d4 = 21;
pin_d5 = 22;
pin_d6 = 25;
pin_d7 = 27;

# Definicion de pines para LED-RGB
pin_R = 16;
pin_G = 20;
pin_B = 26;

# Definicion de pines para sensor ultrasonidos
pin_echo 	= 23;
pin_trigger = 24;



###################################
# Configuracion de puertos/pines
###################################
GPIO.setup(pin_led_on_off,	GPIO.OUT);
GPIO.setup(pin_circuito,	GPIO.OUT);
GPIO.setup(pin_boton,		GPIO.IN, pull_up_down=GPIO.PUD_UP);

# RGB-LED
GPIO.setup(pin_R, GPIO.OUT);
GPIO.setup(pin_G, GPIO.OUT);
GPIO.setup(pin_B, GPIO.OUT);

# HC-SR04
GPIO.setup(pin_trigger, GPIO.OUT);
GPIO.setup(pin_echo, 	GPIO.IN);



###################################
# Inicializacion de variables
###################################

# Inicializacion de estados del sistema
estado_boton 	 = True;
sistema_activado = False;

# Inicializacion temperatura y humedad
temperatura = 0;
humedad 	= 0;

# Definicion de caracteristicas de la pantalla
numero_columnas = 16;
numero_filas 	= 2;

# Apagando LEDs
GPIO.output(pin_circuito, 	False);
GPIO.output(pin_led_on_off, False);
led_rgb_apagado();


# Inicializacion de la pantalla
try:
	pantalla = LCD.Adafruit_CharLCD(pin_rs, pin_en, pin_d4, pin_d5, pin_d6, pin_d7, numero_columnas, numero_filas, True);
	pantalla.clear();
	
	pantalla.message('Iniciando sensor...');
	pantalla.set_backlight(0);
	
	# Texto - fila 2
	pantalla.set_cursor(5,1);
	pantalla.message('TFG');	
	
	#time.sleep(2);
	#pantalla.set_backlight(1);

except Exception as err:
	msg = "Error al inicializar la pantalla. ", err;
	fin_programa(msg);
	
	
msg = "Activada pantalla...";
escribe_log(msg);


###################################
# Inicio programa
###################################
try:
	
	# Activar LED estado del sistema
	GPIO.output(pin_circuito, True);

	i = 0;
	while(True):
		
		# Obtener estado del boton de activacion
		estado_boton = GPIO.input(pin_boton);
		time.sleep(0.2);
		
		# Comprobar si se pulsa el boton
		if estado_boton==False:
			# BOTON PULSADO
			escribe_log('Boton pulsado');
		
			# Comprobar estado del sistema
			if sistema_activado == True:
				# Sistema esta activado. Se desactiva
				sistema_activado = False;
				msg_activacion = 'Desactivado';
				GPIO.output(pin_led_on_off, False);
			else:
				# Sistema esta desactivado. Se activa
				sistema_activado = True;
				msg_activacion = 'Activado';
				GPIO.output(pin_led_on_off, True);
	
			# Pintando estado en la pantalla
			pantalla.clear();
			pantalla.message(msg_activacion);
				
		# Fin comprobar estado boton
		
		# Comprobar estado del sistema para su funcionamiento
		if sistema_activado == True:
			# Sistema ACTIVO
			escribe_log('Activado...' + str(i) );
			
			# Calcula distancias
			calcula_distancia();
		else:
			# Sistema DESACTIVADO
			escribe_log('Desactivado...' + str(i) );
		# Fin comprobar estado del sistema
			
		# Para debug
		i = i + 1;
	
		
	 
except KeyboardInterrupt:
	msg = "Terminando programa...";
	fin_programa(msg);


###################################
# Fin programa
###################################
