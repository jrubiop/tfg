#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  led.py
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

# No mostrar warnings
# gpio.setwarnings(False);

# Modo de numeracion de los pines
gpio.setmode(gpio.BOARD);
pin_led1 = 12;
pin_led2 = 18;

# gpio.setmode(gpio.BCM);
#pin_led1 = 18;
#pin_led2 = 24;


# for  x in range ( 0, 10):

gpio.setup(pin_led1, gpio.OUT);
gpio.setup(pin_led2, gpio.OUT);

gpio.output(pin_led1, True);
time.sleep(2);

gpio.output(pin_led1, False);
time.sleep(2);

gpio.output(pin_led2, True);
time.sleep(2);

gpio.output(pin_led2, False);
time.sleep(2);



# Liberar todo
gpio.cleanup();
