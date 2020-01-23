#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 15:18:23 2019

@Auteur: BERNARD TAMBA SANDOUNO

le code suivant est l'implementation du Dashboard qui sera utilisé par l'utilisateur
de la 'sonnette intelligente'. D'un point de vue technique, il s'agit d'une architecture
Client-Serveur. L'utilisateur(i.e le code suivant) est le serveur tandisque la Raspberry est
le client. Ceci est rendu possible par l'utilisation des Sockets. En plus des sockets,
une interface graphique, faisant office de Dashboard est ainsi implemenntée ci-dessous.
"""
#Importation des Packages de l'interface graphique
from tkinter import * 
import tkinter.font as F
import tkinter.messagebox as A
#Importation du package pour la socket
import socket

#Implementation de la socket
hote = '192.168.43.39' # L'addresse IP de cette machine. A remplacer par l'adresse IP de votre machine
port = 4003 #Le port sur lequel repond ledit serveur. Il peut etre n'importe quel nombre à priori

connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Creation de la socket en mode TCP et IPv4
connexion_principale.bind((hote, port)) # Association de l'@ IP et du numero port à la socket
connexion_principale.listen(5) # Lancement du serveur: Il est maintenant pret à recevoir les messages de la Raspberry
connexion_avec_client, infos_connexion = connexion_principale.accept() #Recuperation des informations de la raspberry, une fois ce derniere connectée

# La partie suivante s'execute quand une presence est detectee par la Raspberry.
msg_recu = connexion_avec_client.recv(1024)# Reception de la notification envoyée par la raspberry

"""Les fonctions ci-dessous, sont celles qui sont invoquées, quand l'utilisateur
initie une action """

def CommunicationAction():
    connexion_avec_client.send(b"C")
    msg_recu = connexion_avec_client.recv(1024)
    print(msg_recu.decode())
    msg_a_envoyer = b""
    while msg_a_envoyer != b"fin":
        msg_a_envoyer = input("> ")
        msg_a_envoyer = msg_a_envoyer.encode()
        connexion_avec_client.send(msg_a_envoyer)
        if msg_a_envoyer != b"fin":
            msg_recu = connexion_avec_client.recv(1024)
            print(msg_recu.decode())
        
        
def OuvertureAction():
    connexion_avec_client.send(b"O")
    msg_recu = connexion_avec_client.recv(1024)
    A.showinfo("Ouverture de la porte",msg_recu.decode())
    
    
def AlarmeAction():
    connexion_avec_client.send(b"A")
    msg_recu = connexion_avec_client.recv(1024)
    print(msg_recu.decode())
    
def RepondeurAction():
    connexion_avec_client.send(b"R")
    msg_recu = connexion_avec_client.recv(1024)
    A.showinfo("Nouveau Message",msg_recu.decode())
    
def QuitterAction():
    connexion_avec_client.send(b"Quit")
    fen.quit()
    fen.destroy()
    connexion_avec_client.close()
    connexion_principale.close()

#Dès que la notification est recu par l'utilisateur, le Dashboard s'affiche automatiquement
#Implementation du Dashboard
fen = Tk() # Creation de la fenetre
fen.geometry("1300x700") # Dimensionnement de la fenetre du Dashboard

photo = PhotoImage(file="a.gif")# Chargement de l'image de fond. Elle peut etre n'importe quelle image(de preference en .gif)

# Creation et Placement des differents boutons du Dashboard
MyFont = F.Font(family='Verdana', size=20, weight='bold')
canvas = Canvas(fen,width=1300, height=700)
canvas.create_image(0, 0, anchor=NW, image=photo)
#Bouton pour communiquer avec le visiteur
Communication = Button(text="COMMUNICATION", bd=5, height=1, width=12,bg="#556DD9",fg="#D3D3D3",
               font=MyFont, command =CommunicationAction)
#Bouton pour l'ouverture de  la porte
Ouverture = Button(text="OUVERTURE", bd=5, height=1, width=12,bg="#556DD9",fg="#D3D3D3",
               font=MyFont,command = OuvertureAction)
#Declenchement de l'alarme
Alarme = Button(text="ALARME", bd=5, height=1, width=12,bg="#E40E35",fg="#D3D3D3",
                   font=MyFont,command = AlarmeAction)
# Le bouton repondeur
repondeur = Button(text="REPONDEUR", bd=5, height=1, width=12,bg="#556DD9",fg="#D3D3D3",
                   font=MyFont,command = RepondeurAction)
canvas.create_window(430,250, window=Communication)
canvas.create_window(650,250, window=Ouverture)
canvas.create_window(870,250, window=repondeur)
canvas.create_window(650,350, window=Alarme)
canvas.pack()
fen.protocol("WM_DELETE_WINDOW", QuitterAction)
fen.mainloop()#Affichage de la fenetre