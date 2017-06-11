#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  rgb_led.py
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

print "Iniciando...\n";

# Quita warnings
#gpio.setwarnings(False);

# Modo de numeracion de los pines (BCM)
gpio.setmode(gpio.BCM);

print "Fijando modo (BCM)...\n";

# Definicion de pines para el led
pin_R = 16;
pin_G = 20;
pin_B = 26;

#led = RGBLED (pin_R, pin_G, pin_B);
gpio.setup(pin_R, gpio.OUT);
gpio.setup(pin_G, gpio.OUT);
gpio.setup(pin_B, gpio.OUT);

print "Fijando pines R-G-B...\n";

gpio.output(pin_R, False);
gpio.output(pin_G, False);
gpio.output(pin_B, False);

try:
	# Midiendo distancias infinitamente...
    while True:
		gpio.output(pin_R, True);
		gpio.output(pin_G, False);
		gpio.output(pin_B, False);
		time.sleep(2);

		gpio.output(pin_R, False);
		gpio.output(pin_G, True);
		gpio.output(pin_B, False);
		time.sleep(2);

		gpio.output(pin_R, False);
		gpio.output(pin_G, False);
		gpio.output(pin_B, True);
		time.sleep(2);

		gpio.output(pin_R, False);
		gpio.output(pin_G, False);
		gpio.output(pin_B, False);
		time.sleep(2);
		
		print "Pines R-G-B apagados...\n";
		
		#led.color = (1, 0, 0);
		#led.color = (0, 0, 1);
		#led.color = (0, 1, 0);


except KeyboardInterrupt:
    
	#led.off();
	gpio.output(pin_R, False);
	gpio.output(pin_G, False);
	gpio.output(pin_B, False);
	
	# Libera todo
	gpio.cleanup();

	print("Fin....\n");
