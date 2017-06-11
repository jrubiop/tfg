/*
 * led.c
 * 
 * Copyright 2017 jose <jose@PCJRUBIO>
 * 
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 * MA 02110-1301, USA.
 * 
 * 
 */
#include <stdio.h>
#include <wiringPi.h>

int main(int argc, char **argv) {
	
	printf ("inicio LED...\n");
	if (wiringPiSetup () == -1) {
		printf ("Fallo en setup de WiringPi...\n");
		return 1;
	}
	
	int pin_led1 = 1; // 1 es el correspondiente al pin 12
	int pin_led2 = 5; // 5 es el correspondiente al pin 18	
	
////wiringPiSetup(); // Initializes wiringPi using wiringPi's simlified number system.
//int pin_led1 = 1; // 1 es el correspondiente al pin 12
//int pin_led2 = 5; // 5 es el correspondiente al pin 18
	
////wiringPiSetupGpio(); // Initializes wiringPi using the Broadcom GPIO pin numbers	
//int pin_led1 = 18; // GPIO18 es el correspondiente al pin 12
//int pin_led2 = 24; // GPIO24 es el correspondiente al pin 18
	

	
	// Definir pin de salida
	pinMode (pin_led1, OUTPUT);
	pinMode (pin_led2, OUTPUT);
	
	
	int num_veces = 3;
	int i = 0;
	for (i=0; i < num_veces; i++) {

		// Activa el pin
		digitalWrite (pin_led1, 1);
		delay (2000);
		
		// Apaga el pin
		digitalWrite (pin_led1, 0);
		delay (1000);
		
		// Activa el pin
		digitalWrite (pin_led2, 1);
		delay (2000);
		
		// Apaga el pin
		digitalWrite (pin_led2, 0);
		delay (1000);		
	}

	printf ("fin LED...\n");
	return 0;
}
