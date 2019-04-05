
/*
 * sensor_TFG.c
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
#include <string.h>
#include <stdlib.h>
#include <time.h>

#include <stdlib.h>
#include <stdint.h>
#include <sys/types.h>
#include <unistd.h>

#include <wiringPi.h>
#include <lcd.h>
//#include <SimpleDHT.h>

// Para activar log de ejecucion
#define LOG_ACTIVO	0

/* ******************** */
/* Definicion de pines  */
/* ******************** */
#define PIN_LED_ON_OFF 	14
#define PIN_BOTON 		15
#define PIN_CIRCUITO 	18

#define PIN_TEMPERATURA 19

#define PIN_BL 	4
#define PIN_RS 	5
#define PIN_EN 	6
#define PIN_D4 	21
#define PIN_D5 	22
#define PIN_D6	25
#define PIN_D7 	27
 
#define PIN_R 	16
#define PIN_G 	20
#define PIN_B 	26

#define PIN_ECHO 	23
#define PIN_TRIG 	24


#define MAXTIMINGS 85
static int DHTPIN = PIN_TEMPERATURA;
static int dht22_dat[5] = {0,0,0,0,0};

static uint8_t sizecvt(const int read)
{
  /* digitalRead() and friends from wiringpi are defined as returning a value
  < 256. However, they are returned as int() types. This is a safety function */

  if (read > 255 || read < 0)
  {
    printf("Invalid data from wiringPi library\n");
    exit(EXIT_FAILURE);
  }
  return (uint8_t)read;
}


/* Para almacenar los datos obtenidos */
struct datosMedidos {
     float temperatura;
     float humedad;
     float distancia;
     float velocidad_sonido;
};


// Pantalla para mostrar la informacion
int pantalla;

/* *********************** */
/* Definicion de funciones */
/* *********************** */
void escribe_log(char* msg) {
	printf("%s \n", msg);
}

void escribe_debug(char* msg) {
	if (LOG_ACTIVO == 1) {
		printf("%s \n", msg);
	}
}

void fin_programa(char* msg) {
	//global pantalla;
	
	//# Desactiva el sensor
	//#GPIO.output(pin_trigger, False);
	
	//#GPIO.output(pin_circuito, False);
	
	//# Liberando puertos
	//GPIO.cleanup();
	
	//# Limpia pantalla
	//#pantalla.clear();
	
	if ( strcmp(msg, "") != FALSE ) {
		printf("%s \n", msg);
	}
	
	// Fin programa
	exit(1);
}
	

// ---------------------------
// Funciones para Led-RGB
// ---------------------------
void led_rgb_apagado(void) {
	digitalWrite(PIN_R, LOW);
	digitalWrite(PIN_G, LOW);
	digitalWrite(PIN_B, LOW);
}

void led_rgb_rojo(void) {
	digitalWrite(PIN_R, HIGH);
	digitalWrite(PIN_G, LOW);
	digitalWrite(PIN_B, LOW);
}
	
void led_rgb_verde(void) {
	digitalWrite(PIN_R, LOW);
	digitalWrite(PIN_G, HIGH);
	digitalWrite(PIN_B, LOW);	
}
	
void led_rgb_azul(void) {
	digitalWrite(PIN_R, LOW);
	digitalWrite(PIN_G, LOW);
	digitalWrite(PIN_B, HIGH);
}
	
// ---------------------------
// Funciones script
// ---------------------------
int inicializar_dispositivos() {
	
	if (wiringPiSetupGpio() == -1) {
	//if (wiringPiSetup() == -1) {
		return FALSE;
	}

	// Configuracion de puertos
	pinMode(PIN_LED_ON_OFF, OUTPUT);
	pinMode(PIN_CIRCUITO, 	OUTPUT);

	pullUpDnControl(PIN_BOTON, PUD_UP);

	pinMode(PIN_R, OUTPUT);
	pinMode(PIN_G, OUTPUT);
	pinMode(PIN_B, OUTPUT);
	
	pinMode(PIN_TRIG, OUTPUT);
	pinMode(PIN_ECHO, INPUT);

	// Inicializando el sensor ultrasonidos
	digitalWrite(PIN_TRIG, LOW);
	delay(30);
	
	// Todo correcto
	return TRUE;
}


void registra_datos(float distancia, float temperatura, float humedad) {
	
}


void muestra_datos(float distancia, float temperatura, float humedad) {

	// Encender LED dependiendo de la distancia
	if (distancia < 20) {
		led_rgb_rojo();
	}
	else {
		if ( (distancia >= 20) && (distancia < 40) ) {
			led_rgb_azul();
		}
		else {
			led_rgb_verde();
		}
	}
	
	// Mostrando resultados
	char msg[255] = "";
	sprintf(msg, "Distancia  ==> %.2f cm -- T: %f grados y humedad: %.2f", distancia, temperatura, humedad);
	escribe_log(msg);	
	
	// Pintando resultados en la pantalla
	//sprintf(msg, "D: %2.2f cm. T: %.2f ºC. H: %.2f", distancia, temperatura, humedad);
	sprintf(msg, "D: %5.2f cm", distancia);
	lcdClear(pantalla);
	lcdPosition(pantalla,0,0);
	lcdPuts(pantalla, msg);
	
	// Hora
	time_t tiempo = time(0);
	struct tm *ts = localtime(&tiempo);
	strftime(msg, 255, "%d %b %H:%M:%S", ts);
	lcdPosition(pantalla,0,1);
	lcdPuts(pantalla, msg);		
}


static int read_dht22_dat() {

  uint8_t laststate = HIGH;
  uint8_t counter = 0;
  uint8_t j = 0, i;

  dht22_dat[0] = dht22_dat[1] = dht22_dat[2] = dht22_dat[3] = dht22_dat[4] = 0;

  // pull pin down for 18 milliseconds
  pinMode(DHTPIN, OUTPUT);
  digitalWrite(DHTPIN, HIGH);
  delay(10);
  digitalWrite(DHTPIN, LOW);
  delay(18);
  // then pull it up for 40 microseconds
  digitalWrite(DHTPIN, HIGH);
  delayMicroseconds(40); 
  // prepare to read the pin
  pinMode(DHTPIN, INPUT);

  // detect change and read data
  for ( i=0; i< MAXTIMINGS; i++) {
    counter = 0;
    while (sizecvt(digitalRead(DHTPIN)) == laststate) {
      counter++;
      delayMicroseconds(1);
      if (counter == 255) {
        break;
      }
    }
    laststate = sizecvt(digitalRead(DHTPIN));

    if (counter == 255) break;

    // ignore first 3 transitions
    if ((i >= 4) && (i%2 == 0)) {
      // shove each bit into the storage bytes
      dht22_dat[j/8] <<= 1;
      if (counter > 16)
        dht22_dat[j/8] |= 1;
      j++;
    }
  }

  // check we read 40 bits (8bit x 5 ) + verify checksum in the last byte
  // print it out if data is good
  if ((j >= 40) && 
      (dht22_dat[4] == ((dht22_dat[0] + dht22_dat[1] + dht22_dat[2] + dht22_dat[3]) & 0xFF)) ) {
        float t, h;
        h = (float)dht22_dat[0] * 256 + (float)dht22_dat[1];
        h /= 10;
        t = (float)(dht22_dat[2] & 0x7F)* 256 + (float)dht22_dat[3];
        t /= 10.0;
        if ((dht22_dat[2] & 0x80) != 0)  t *= -1;


    printf("Humidity = %.2f %% Temperature = %.2f *C \n", h, t );
    return 1;
  }
  else
  {
    printf("Data not good, skip\n");
    return 0;
  }
}

 
float mide_temperatura(void) {

	// Lee temperatura y humedad
	//humedad, temperatura = DHT.read_retry(tipo_sensor, pin_temperatura);
	//datos = {'t': temperatura, 'h': humedad };
	//return datos;
	
	// --------------------
	//SimpleDHT11 sensor_temperatura;
	//byte t = 0;
	//byte h = 0;
	//if ( sensor_temperatura.read(PIN_TEMPERATURA, &t, &h, NULL) ) {
		//t = -1;
		//return t;
	//}
	// --------------------
	float temperatura = 24;
	
	/*
	long t = digitalRead(PIN_TEMPERATURA);
	char msg[255] = "";
	sprintf(msg, "TEMP  ==> %d", t);
	escribe_log(msg);		
	* */
	
	float t = read_dht22_dat();
	
	temperatura = (float) t;
	
	// Valor obtenido
	return (temperatura);
}	
	
float mide_duracion(void) {
	
	// Inicializacion de tiempos
	long ts_inicio 	= 0;
	long ts_final	= 0;		

	// Inicializacion del sensor
	digitalWrite(PIN_TRIG, LOW);

	// Para 1 segundo para el sensor
	delay(500);
	escribe_debug("Esperando 0.5 seg...");
	
	// Activa el sensor - envio señal
	digitalWrite(PIN_TRIG, HIGH);
	escribe_debug("enviando trigger...");

	// Espera envio de señal (10 microsegundos)
	int ts_espera = 10;
	delay(ts_espera * 0.001);
	escribe_debug("Terminado esperar 10 microseg...");

	// Desactiva el sensor - parada
	digitalWrite(PIN_TRIG, LOW);
	escribe_debug("Iniciando echo...");

	// Inicio lectura del echo
	while ( digitalRead(PIN_ECHO) == LOW ) {
		ts_inicio = micros();
		//ts_inicio = millis();
	}
	escribe_debug("Fin echo...");

	// Fin lectura del echo
	while ( digitalRead(PIN_ECHO) == HIGH ) {
		ts_final =  micros();
		//ts_final =  millis();
	}
	escribe_debug("Fin lectura...");
		
	// Calculo de distancia, lo que tarde en ir y volver la señal
	float ts_duracion = ts_final - ts_inicio;
	
	// Tiempo devuelto
	return ts_duracion;
}

int calcula_velocidad_sonido(float temperatura) {
	
	float t = temperatura;
	
	// Calculo de la velocidad del sonido en funcion de variables
	int velocidad_sonido = 343;
	
	// Velocidad calculada
	return velocidad_sonido;
}

int calcula_distancia(void) {
	
	// Midiendo temperatura y humedad
	//datos_medicion = mide_temperatura();
	//temperatura = datos_medicion['t'];
	//humedad 	= datos_medicion['h'];
	float temperatura = mide_temperatura();
	float humedad = 70;
	
	// Velocidad del sonido en aire
	// Se calculara dinamicamente en funcion del ambiente (aereo, acuatico) y de las condiciones (presion, temperatura)
	int velocidad_sonido = calcula_velocidad_sonido(temperatura);
	// print "Velocidad Sonido: ", str(velocidad_sonido);
		
	// Calculo del tiempo de propagacion del echo
	float ts_duracion = mide_duracion();
	
	// Calculo de distancia (en cm), lo que tarde en ir y volver la señal
	float distancia =  ( ( ts_duracion * velocidad_sonido ) / 2) * 100;

	char msg[255] = "";
	sprintf(msg, "duracion: %f distancia: %f sonido: %d", ts_duracion, distancia, velocidad_sonido);
	escribe_log(msg);
	
	// Muestra datos
	muestra_datos(distancia, temperatura, humedad);
	
	// Registrando datos
	// registra_datos(distancia, temperatura, humedad);
	
	// Todo correcto
	return TRUE;
}



int main(int argc, char **argv) {
	
	// Inicializa el dispositivo y los puertos
	int resultado = inicializar_dispositivos();
	if (resultado == FALSE) {
		printf ("Fallo en setup de WiringPi...\n");
		exit(1);
	}

	// Inicializacion de estados del sistema
	int estado_boton 	  = HIGH;
	int sistema_activado = FALSE;

	// Definicion de caracteristicas de la pantalla
	int numero_columnas = 16;
	int numero_filas 	= 2;
	int numero_bytes 	= 4;

	// Apagando LEDs
	digitalWrite(PIN_CIRCUITO, 	 LOW);
	digitalWrite(PIN_LED_ON_OFF, LOW);
	led_rgb_apagado();

	// Inicializacion de la pantalla
	pantalla = lcdInit(numero_filas,numero_columnas,numero_bytes,PIN_RS,PIN_EN,PIN_D4,PIN_D5,PIN_D6,PIN_D7,0,0,0,0);

	// Info en pantalla
	lcdDisplay(pantalla, TRUE);
	lcdClear(pantalla);
	lcdPuts(pantalla, "Iniciando sensor...");
		
	// Texto - fila 2
	lcdPosition(pantalla, 5, 1);
	lcdPuts(pantalla, "TFG");
	delay(1000);
	
	escribe_debug("Activada pantalla...");

	// Activar LED estado del sistema
	digitalWrite(PIN_CIRCUITO,	HIGH);

	char msg[255] = "";
	int i = 0;
	while (1) {
		
		// Obtener estado del boton de activacion
		//estado_boton = digitalRead(PIN_BOTON);
		delay(200);
		
		sistema_activado = TRUE;
		estado_boton = TRUE;
		
		// Comprobar si se pulsa el boton
		//if (estado_boton == LOW) {
		if ( FALSE ) {
			// BOTON PULSADO
			escribe_log("Boton pulsado");
			
			char msg_activacion[255] = "";
		
			// Comprobar estado del sistema
			if (sistema_activado == TRUE) {
				// Sistema esta activado. Se desactiva
				sistema_activado = FALSE;
				strcat(msg_activacion, "Desactivado");
				digitalWrite(PIN_LED_ON_OFF,	LOW);
			}
			else {
				// Sistema esta desactivado. Se activa
				sistema_activado = TRUE;
				strcat(msg_activacion, "Activado");
				digitalWrite(PIN_LED_ON_OFF,	HIGH);
			}
	
			// Pintando estado en la pantalla
			lcdClear(pantalla);
			lcdPuts(pantalla, msg_activacion);
			
		} // Fin comprobar estado boton
		
		// Comprobar estado del sistema para su funcionamiento
		if (sistema_activado == TRUE) {
			// Sistema ACTIVO
			sprintf(msg, "Activado... %d", i);
			escribe_debug(msg);
			
			// Calcula distancias
			calcula_distancia();
		}
		else {
			// Sistema DESACTIVADO
			sprintf(msg, "Desactivado... %d", i);
			escribe_debug(msg);
		} // Fin comprobar estado del sistema
			
		// Para debug
		i = i + 1;
		
	}

	escribe_log("fin sensor_TFG ...");
	return 0;
}
