"""
* Obtener temperatura del paciente y mandarlos por mqtt
*
* Realizado por: 
* 1. DIEGO ANTONIO ROMERO PALACIOS
* 2. AMANDA SARAHÍ BASTIDA RAMÍREZ
* 3. JANETH SOTELO VALDEZ
*
* Fecha: 15 de febrero de 2021
*
* Este programa toma la temperatura de un paciente 
* cuando la lee manda esos datos mediante mqtt para recibirlos en otra
* plataforma

*MLX90614   raspberry 3B+
*VCC-------------- pin 2
*GND-------------- pin 34
*SDA------------- pin 3
*SCL------------- pin 5
"""

#Bibliotecas
import paho.mqtt.client as mqtt #Bliblioteca para usar mqtt
import json #Biblioteca para manejo de json
from smbus2 import SMBus #Biblioteca para usar IC2
from time import sleep #Biblioteca de tiempo
from mlx90614 import MLX90614 #Biblioteca para manejar el sensor infrarojo

#Variables, Obejetos y constantes
client = mqtt.Client() #Objeto para publicar en mqtt
MQTT_ADDRESS = 'broker.hivemq.com'#constante para la direccion a mandar por mqtt
MQTT_TOPIC = 'mqtt/rfid/temp'#topic de mqtt
b=True #Para el while


while (b):
    op=input("Tomar Temperatura [S/N]: ")
    if(op=="S" or op=="s"):
        bus = SMBus(1)
        codigo2=input("No Expediente: ")
        print("Acercarse lo mas posible...")
        sleep(5)
        sensor = MLX90614(SMBus(1), address=0x5A)
        temp=sensor.get_object_1()
        print ("Temperatura ambiente :", round(sensor.get_ambient(),2))
        print ("Temperatura de Persona u objeto :", round(sensor.get_object_1(),2))
        pythonDictionary = {'Temperatura':round(temp,2),'codigo':codigo2} #acomodar los datos en json
        dictionaryToJson = json.dumps(pythonDictionary) #convertir los datos en json
        #print(dictionaryToJson)
        client.connect(MQTT_ADDRESS,1883,60) #se conecta mqtt 
        client.publish(MQTT_TOPIC,dictionaryToJson) #publica el mensaje en el topic
        bus.close()
        print("Temperatura Guardada")
    elif(op=="N" or op=="n"):
        op2=input("oprimir S para salir del programa: ")
        if(op2=="S" or op2=="s"):
            b =False
        else:
            print("Regresando....")
    else:
        print("Error tecla no valida: ")
