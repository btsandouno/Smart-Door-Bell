#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 09:37:35 2019

@Auteur: BERNARD TAMBA SANDOUNO
Mineure DS4H Sensors and Network Devices
Université Côte d'Azur
Copyright, 2020


Le code suivant est l'implementation d'une 'sonnette intelligente'. La Raspberry
fait office dans ce projet de la sonnette.Techniquement, il s'agit d'une architecture client-serveur
où  la raspberry Pi fait office de Client. La Raspberry Elle est equipée d'un detecteur de presence,
d'une LED RGB et d'un Active Buzzer. La Raspberry enverra des notifications à l'utilisateur 
dès qu'une presence est detectée dans son domaine. Elle permettra egalement la 
communication entre le visiteur et le proprietaire independemment de la localisation 
du proprietaire. Ce dernier peut ainsi decider d'ouvrir la porte, declencher une alarme,etc.

"""
#Importation des packages pour la raspberry
import RPi.GPIO as GPIO
import time

# Importatoon du package de la socket
import socket

#Les paramètres de la socket
hote = '192.168.43.39' #L'adresse IP de l'utilisateur(et non celle de la Raspberry)
port = 4003 # Le port sur lequel repond l'utilisateur

#Implementation du PIR situé sur la broche 23(GPI011), GND sur la broche 20 et l'alimentation (+5V) sur 4
#La LED(la broche ROuge uniquement) est située sur la broche GPIO14 et le buzzer sur la GPIO17
GPIO.setmode(GPIO.BCM)
PIR = 11
BUZZER = 17
LED = 14
GPIO.setup(PIR,GPIO.IN)
GPIO.setup(LED,GPIO.OUT)
GPIO.setup(BUZZER,GPIO.OUT)

#Etablissement de la connexion entre la Raspberry et l'utilisateur
connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_avec_serveur.connect((hote, port))

        
#Fonction permettant d'executer les actions demandées par l'utilisateur
def Action(msg_recu):
    if(msg_recu =="C"): #Si l'utilisateur veut communiquer avec le visiteur
        print("Entrez votre nom complet")
        while msg_recu != b"fin":
            msg_a_envoyer = input("> ")
            msg_a_envoyer = msg_a_envoyer.encode()
            connexion_avec_serveur.send(msg_a_envoyer)
            msg_recu = connexion_avec_serveur.recv(1024)
            print(msg_recu.decode())
            
    elif(msg_recu=="A"):#Si l'utilisateur veut declencher une alarme
        connexion_avec_serveur.send(b"Je declenche alarme")
        GPIO.setwarnings(False)
        for i in range(10):
            GPIO.output(BUZZER,GPIO.HIGH)
            GPIO.output(LED,GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(BUZZER,GPIO.LOW)
            GPIO.output(LED,GPIO.LOW)
            time.sleep(0.5)

    elif(msg_recu=="R"):#Repondeur: Si l'utilisateur est indisponible: Pour que le visiteur lui laisse un message
        print("Je ne suis pas disponible, veuillez me laisser un message")
        msg_a_envoyer = input("> ")
        msg_a_envoyer = msg_a_envoyer.encode()
        connexion_avec_serveur.send(msg_a_envoyer)
        
    elif(msg_recu=="O"):#Si l'utilisateur veut ouvrir la porte au visiteur
        connexion_avec_serveur.send(b"La porte est ouverte")
        print("La porte est ouverte, vous pouvez entrer")
        

#Implementation du PIR pour l'envoie de la notification au serveur, une fois la presence detectée par le PIR
time.sleep(5)

state = GPIO.input(PIR)
while(state==0):
    time.sleep(3)
    state = GPIO.input(PIR)
connexion_avec_serveur.send(b"Presence detectee")
msg_recu = connexion_avec_serveur.recv(1024)
msg_recu = msg_recu.decode()

while(msg_recu!="Quit"):
    Action(msg_recu)
    msg_recu = connexion_avec_serveur.recv(1024)
    msg_recu = msg_recu.decode()
connexion_avec_serveur.close()#La connexion entre le visiteur et l'utilisateur est fermée, lorsque ce dernier ferme son dashboard