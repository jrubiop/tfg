#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  distancia.py
#  
#  Copyright 2017 jose <jose@PCJRUBIO>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#

import RPi.GPIO as gpio;
import time;

#from gpiozero import RGBLED;

# Libreria sensor temperatura
#import Adafruit_DHT;

print "Iniciando...\n";

# Quita warnings
gpio.setwarnings(False);

# Modo de numeracion de los pines (BCM)
gpio.setmode(gpio.BCM);

print "Fijando modo (BCM)...\n";

# Definicion de pines a utilizar (BCM)
pin_echo 	= 6;
pin_trigger = 12;

# Activacion de pines
# Para activar el sensor (pin trigger)
gpio.setup(pin_trigger, gpio.OUT);

print "Fijando pin trigger...\n";

# Para leer del sensor (pin echo)
gpio.setup(pin_echo, gpio.IN);

print "Fijando pin echo...\n";

# Definicion de pines para el led
pin_R = 16;
pin_G = 20;
pin_B = 26;

#led = RGBLED (pin_R, pin_G, pin_B);
gpio.setup(pin_R, gpio.OUT);
gpio.setup(pin_G, gpio.OUT);
gpio.setup(pin_B, gpio.OUT);

print "Fijando pines R-G-B...\n";

# Definicion de pin para sensor temperatura
pin_temperatura = 19;
#tipo_sensor		= Adafruit_DHT.DHT11; # DHT11

gpio.output(pin_R, False);
gpio.output(pin_G, False);
gpio.output(pin_B, False);

print "Pines R-G-B apagados...\n";

try:
	# Midiendo distancias infinitamente...
    while True:
		ts_inicio 	= 0;
		ts_final	= 0;		

		# Velocidad del sonido en aire
		# Se calculara dinamicamente en funcion del ambiente (aereo, acuatico) y de las condiciones (presion, temperatura)
		velocidad_sonido = 343;

		# Inicializa el sensor
		gpio.output(pin_trigger, False);

		# Para 1 segundo para el sensor
		time.sleep(1);
	
		print "Esperando 1 seg...\n";
		
		# Calculando temperatura y humedad
		temperatura = 0;
		humedad 	= 0;
		
		#print "antes de leer temp...\n";
		
		# Lee temperatura y humedad
		#humedad, temperatura = Adafruit_DHT.read_retry(tipo_sensor, pin_temperatura);
		
		#print "despues de leer temp...\n";

		# Activa el sensor - envio señal
		gpio.output(pin_trigger, True);
		
		print "enviando trigger...\n";

		# Espera envio de señal
		ts_espera = 10; # segundos
		time.sleep(ts_espera * 10**-6); # en microsegundos
		
		print "Terminado esperar 10 seg...\n";

		# Desactiva el sensor - parada
		gpio.output(pin_trigger, False);

		print "Iniciando echo..\n";

		# Inicio lectura del echo
		#while gpio.input(pin_echo) == gpio.LOW:
		#	ts_inicio = time.time();
			
		print "Fin echo..\n";

		# Fin lectura del echo
		#while gpio.input(pin_echo) == gpio.HIGH:
		#	ts_final = time.time();
			
		print "Fin lectura..\n";
			
		# Calculo de distancia, lo que tarde en ir y volver la señal
		ts_duracion = ts_final - ts_inicio;
		distancia =  ( ( ts_duracion * velocidad_sonido ) / 2) * 100;
		
		# Pintando resultados
		distancia =  round(distancia, 2);
		temperatura =  round(temperatura, 2);
		print "Distancia  ==> ", str(distancia), " cm -- ", str(temperatura), " grados y humedad: ", str(humedad);
		
		# Encender led dependiendo de la distancia
		if distancia > 20:
			gpio.output(pin_R, True);
			gpio.output(pin_G, False);
			gpio.output(pin_B, False);
			#led.color = (1, 0, 0);
		elif 20 <= distancia < 40:
			gpio.output(pin_R, False);
			gpio.output(pin_G, False);
			gpio.output(pin_B, True);
			#led.color = (0, 0, 1);
		else:
			gpio.output(pin_R, False);
			gpio.output(pin_G, True);
			gpio.output(pin_B, False);
			#led.color = (0, 1, 0);


except KeyboardInterrupt:
    
	# Desactiva el sensor
	gpio.output(pin_trigger, False);
	
	#led.off();
	gpio.output(pin_R, False);
	gpio.output(pin_G, False);
	gpio.output(pin_B, False);
	
	# Libera todo
	gpio.cleanup();

	print("Fin....\n");
