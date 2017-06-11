#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  temperatura.py
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

# Libreria sensor temperatura
import Adafruit_DHT;

# No mostrar warnings
# gpio.setwarnings(False);

# Modo de numeracion de los pines
###gpio.setmode(gpio.BOARD);
gpio.setmode(gpio.BCM);

# Definicion de pin para sensor temperatura
pin_temperatura = 19;
tipo_sensor		= Adafruit_DHT.DHT22; # DHT11

# Calculando temperatura y humedad
temperatura = 0;
humedad 	= 0;

print "antes de leer temp...\n";

# Lee temperatura y humedad
humedad, temperatura = Adafruit_DHT.read_retry(tipo_sensor, pin_temperatura);

print "Temp: ", str(temperatura), " grados y humedad: ", str(humedad);
print "Fin temp...\n";
