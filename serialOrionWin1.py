# -*- coding: utf-8 -*-
# Author: Esteban Gabriel Vega Hissi
# email: egvega@unsl.edu.ar
#
# Version: 1.0
#

# Importacion de modulos
import serial
import time
import string

# Solicita al usuario un prefijo para el nombre del archivo de registro de datos
print "Prefijo de archivo de datos: "
fileName='output'+raw_input()+'.txt'
outFile=open(fileName,'w')
outFile.close()

# Solicita tiempo en que se registraran datos expresado en minutos
print "Correr Registro durante minutos: "
timeLimit=int(raw_input())*60

# Solicita numero de puerto al que esta conectado el cable
print "Numero del puerto COM: "
comPort=raw_input()

# Abre puerto e Inicia registro
print "\nRecibiendo desde el puerto COM%d durante %d minutos\n"%(comPort,timeLimit/60)

serialCom = serial.Serial('COM'+comPort, baudrate=1200, timeout=None) #

timeRecord=0
blockOld=False

while serialCom.isOpen():
    outFile=open(fileName,'a')
    serialCom.flushInput()
    block=serialCom.read(111)
    if not blockOld:
        timeIni=time.time()
        blockOld=True
    timeRecord=time.time()
    concentrationRecord=float(block[string.find(block,'=')+1:].split('\n')[0].strip())
    outFile.write("%8.3f %8.3f \n"%(timeRecord-timeIni, concentrationRecord))
    print "%8.3f %8.3f"%(timeRecord-timeIni, concentrationRecord)
    outFile.close()
    if (timeRecord-timeIni)+0.01>=timeLimit:    
        break

print "\nRegistro de datos finalizado en %d min\n"%(timeLimit/60)
serialCom.close()
raw_input()

