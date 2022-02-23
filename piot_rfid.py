"""
* Obtener, escribir y mandar datos de tarjeta
*
* Realizado por: 
* 1. DIEGO ANTONIO ROMERO PALACIOS
* 2. AMANDA SARAHÍ BASTIDA RAMÍREZ
* 3. JANETH SOTELO VALDEZ
*
* Fecha: 20 de diciembre de 2021
*
* Este programa tiene 2 funcionalidades 1 lee la tarjeta rfid
* cuando la lee manda esos datos mediante mqtt para recibirlos en otra
* plataforma
* La segunda es escribir valores a la tarjeta

*RFID RC522    raspberry 3B+
*SDA-------------- pin 24
*SCK-------------- pin 23
*MOSI------------- pin 19
*MISO------------- pin 21
*GND-------------- pin 6
*RST-------------- pin 22
*3.3v------------- pin 1
"""



#Bibliotecas
import RPi.GPIO as GPIO #Biblioteca para controlar los pines de la raspberry
from mfrc522 import SimpleMFRC522 #Biblioteca para rfid
from time import sleep #Biblioteca de tiempo
import paho.mqtt.client as mqtt #Bliblioteca para usar mqtt
import json #Biblioteca para manejo de json


#Variables, Obejetos y constantes
GPIO.setwarnings(False)
reader = SimpleMFRC522()#Objeto para leer y escribir en una tarjeta rfid
op=1 #Variable para el menu
client = mqtt.Client() #Objeto para publicar en mqtt
#broker.hivemq.com 
MQTT_ADDRESS = 'broker.hivemq.com'#'127.0.0.1'#constante para la direccion a mandar por mqtt
MQTT_TOPIC = 'mqtt/rfid/codigo'#topic de mqtt

while op != 3: # Se ejecuta mientras op sea diferente de 4
    print('1.Leer\n2.Escribir\n3.Salir') # Muestra las opciones
    op = int(input('Ingresa una opcion: ')) # Usuario ingresa opcion
    if op == 1:
        try:
                print("Acerca la tarjeta")
                id, text = reader.read() #leer el id y el texto que contiene
                #print(id)
                #print(type(id))
                separador="," #poder separar los datos
                separado = text.split(separador) #se separa los datos por ","
                curp = separado[0] #se carga el primer dato separado
                codigo = separado[1] #se carga el segundo dato separado
                print("Correcto datos leidos: ",text)
                sleep(2)
                pythonDictionary = {'curp':curp,'codigo':codigo} #acomodar los datos en json
                dictionaryToJson = json.dumps(pythonDictionary) #convertir los datos en json
                #print(dictionaryToJson)
                client.connect(MQTT_ADDRESS,1883,60) #se conecta mqtt 
                client.publish(MQTT_TOPIC ,dictionaryToJson) #publica el mensaje en el topic
        except:
                GPIO.cleanup()
    elif op == 2:
        try:
                print("Nuevo paciente") #Datos a escribir en la tarjeta
                curp = input('Curp: ')
                codigo=input("No Expediente: ")
                curp = curp.upper() #convertir a mayusculas
                text =curp+","+codigo #concatenamos todo el texto 
                #print(text)
                print("Pasa la tarjeta a escribir")
                reader.write(text)#escribir datos
                print("Listo, correctamente escrito")
                sleep(5)
        finally:
                GPIO.cleanup()
    elif op == 3:
        print("salir")
    else:
        print('Ingrese una opcion valida')

        
                        
        
        
