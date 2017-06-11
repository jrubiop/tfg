#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  pantalla.py
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

import time;
import datetime;

# Libreria para la pantalla
from Adafruit_CharLCD import Adafruit_CharLCD;

print "Inicio pantalla...\n";


# Configuracion de la pantalla
pin_rs        = 5;
pin_en        = 6;

pin_d4        = 21;
pin_d5        = 22;
pin_d6        = 25;
pin_d7        = 27;

pin_bl        = 4;
 
# Caracteristicas de la pantalla
numero_columnas = 16;
numero_filas 	= 2;
 
# Inicializando la pantalla
pantalla = Adafruit_CharLCD(pin_rs, pin_en, pin_d4, pin_d5, pin_d6,
               pin_d7, numero_columnas, numero_filas, True);

while True:
	# Limpiando pantalla
	pantalla.clear();
	time.sleep(2);
	
	#pantalla.set_backlight( True);
	
	ts_fecha = time.time();
	# Fecha - fila 1
	str_fecha = time.strftime('%b %d %H:%M:%S\n');
	pantalla.message( str_fecha );
	
	print "Fecha..." , str_fecha, "\n";
	
	# Texto - fila 2
	pantalla.set_cursor(5,1);
	pantalla.message('Hola Jose');
	time.sleep(2);


print "Fin pantalla...\n";
