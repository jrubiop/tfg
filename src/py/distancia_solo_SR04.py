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

# Quita warnings
gpio.setwarnings(False);

# Modo de numeracion de los pines
gpio.setmode(gpio.BCM);

# Definicion de pines a utilizar (BCM)
pin_echo 	= 6;
pin_trigger = 12;

# Activacion de pines

# Para activar el sensor (pin trigger)
gpio.setup(pin_trigger, gpio.OUT);

# Para leer del sensor (pin echo)
gpio.setup(pin_echo, gpio.IN);


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

		# Activa el sensor - envio señal
		gpio.output(pin_trigger, True);

		# Espera envio de señal
		ts_espera = 10; # segundos
		time.sleep(ts_espera * 10**-6); # en microsegundos

		# Desactiva el sensor - parada
		gpio.output(pin_trigger, False);

		# Inicio lectura del echo
		while gpio.input(pin_echo) == gpio.LOW:
			ts_inicio = time.time();

		# Fin lectura del echo
		while gpio.input(pin_echo) == gpio.HIGH:
			ts_final = time.time();

		# Calculo de distancia, lo que tarde en ir y volver la señal
		ts_duracion = ts_final - ts_inicio;
		distancia =  ( ( ts_duracion * velocidad_sonido ) / 2) * 100;
		distancia =  round(distancia, 2);
		print "Distancia  ==> ", str(distancia), " en cm";

        
except KeyboardInterrupt:
    
	# Desactiva el sensor
	gpio.output(pin_trigger, False);

	# Libera todo
	gpio.cleanup();

	print("Fin....\n");
