import serial
import json
import RPi.GPIO as GPIO
import re
import socket
import threading
import time
from pushbullet import Pushbullet
# GPIO POUR LES RELAIS 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.output(18, GPIO.LOW)
GPIO.output(23, GPIO.LOW)

serMotor = serial.Serial('/dev/ttyACM0',9600)
serSensors = serial.Serial('/dev/ttyACM1',9600)
# Adresse IP et port du serveur (PC)
HOST = '' # Remplacez cette adresse IP par celle de votre PC
PORT = 5000 # Remplacez ce port par le port que vous souhaitez utiliser

# Liste pour stocker les connexions des clients
connections = []

#Expressions Régulières 
boisson =  {"VERSER_BOISSON_1":2,"VERSER_BOISSON_2":17}
toppings = {"VERSER_TOPPING_1":3}
expression_boisson = r"VERSER_BOISSON_([1234])_QUANT_([12345])"
expression_topping = r"VERSER_TOPPING_([1234])_QUANT_([12345])"
#expression_quantite = r"VERSER_QUANT_([12345])"


#Recevoir les niveaux des capteurs
def Verifier_niveau():
    serSensors.write(b'1')
    while serSensors.in_waiting == 0:
        pass
    level = serSensors.readline().decode()
    print(level)
    level = json.loads(level)
    if level['waterLevel'] > 5:
        return True
    else:
        API_KEY = "o.pFBcJM5DrnZAwduewU3TX46h3NtkSN0N"
        text = "ERR-W404"
        pb = Pushbullet(API_KEY)
        push = pb.push_note("", text)
        return False
def reheat():
    #commandeRelay = "allumeResistance"
    #ser2.write(commandeRelay)
    #commandePompe = "VerserEau"
    GPIO.output(18, GPIO.HIGH) # Allume la LED
    time.sleep(4) # Attend 1 seconde
    GPIO.output(18, GPIO.LOW) # Éteint la LED
    
    #ser.write(commandeMotor.encode())
    # Attendre que l'Arduino réponde
       # while ser.in_waiting == 0:
           # pass
    # Lire la réponse de l'Arduino
        #etat = ser.readline().decode().strip()
        #return etat
    


def verser_boisson(numBoisson,Quant):
    commandeMotor = "Servo_" + str(numBoisson) + "_" + str(Quant)
    serMotor.write(commandeMotor.encode())
    # Attendre que l'Arduino réponde
    print("aaa")
    while serMotor.in_waiting == 0:
        pass
    # Lire la réponse de l'Arduino
    etat = serMotor.readline().decode().strip()
    time.sleep(2)
    return 0
    
def mix():
    commandeMotor = "Servo_4"
    serMotor.write(commandeMotor.encode())
 
    time.sleep(10)
    print("verser");
    GPIO.output(23, GPIO.HIGH) # Allume la LED
    time.sleep(10) # Attend 1 seconde
    GPIO.output(23, GPIO.LOW) # Éteint la LED
    return 0

def etat_next(state,action):
    if ( state == "S" ) and (action == "GET_GOBELET") :
        return "A"
    elif (state == "A") and (action == "REHEAT" ) :
        return "A1"
    elif ( state == "A1") and (re.match(expression_boisson,action)) :
        return "B"
    #elif ( state == "A2" ) and (re.match(expression_quantite,action)) :
        #return "B"
    elif (state == "B" ) and (re.match(expression_boisson,action)):
        return "B"
    #elif (state == "B1") and ( re.match(expression_quantite,action)):
        #return "B"
    elif( state == "B") and ( re.match(expression_topping,action)):
        return "C"
    #elif ( state == "B2" ) and ( re.match(expression_quantite,action)):
        #return "C"
    elif (state == "B" ) and ( action == "GET_SPOON"):
        return "F"
    elif (state == "C" ) and ( action == "GET_SPOON"):
        return "F"
    elif ( state == "C") and ( re.match(expression_topping,action)):
        return "C"
    #elif ( state == "C1") and ( re.match(expression_quantite,action)):
        #return "C"
    else:
        return "ERR"
    
    
def automate(data):
    etat = "S"
    nb_steps = 0
    for key, value in data.items():
        if isinstance(value, dict):
            for key2,value2 in value.items():
               etat =  etat_next(etat,value2)
               nb_steps = nb_steps + 1 
        else:
            etat = etat_next(etat,value)
            nb_steps = nb_steps + 1 
    if etat == "F":
        return nb_steps
    else:
        nb_steps = 0
        return nb_steps
         
 

        
    
def executer_action(action):
    if (action == "GET_GOBELET"):
        #conn.sendall(b'depot du gobelet en cours')
        print("depot du gobelet en cours")
        time.sleep(2)
    elif (action == "REHEAT"):
        #conn.sendall(b'rechauffement de la boisson')
        print("réchauffement de la boisson")
        reheat()
    elif (re.match(expression_boisson,action)):
        resultat = re.search(expression_boisson, action)
        #conn.sendall(b"Versement d'une boisson")
        print("Versement de la boisson numéro ", resultat.group(1))
        verser_boisson(resultat.group(1),2)

        
    elif (re.match(expression_topping,action)):
        resultat = re.search(expression_topping, action)
        #conn.sendall(b"Versement d'un topping")
        print("Versement du topping numéro ", resultat.group(1))
    elif (action == "GET_SPOON"):
        #conn.sendall(b'depot de la cuillere')
        mix();
        print("depot de la cuillère")
    else:
        print("quant")
    
    
    
    
# Fonction exécutée dans un thread pour chaque client connecté
def client_thread(conn, addr):
    print('Nouvelle connexion:', addr)
    connections.append(conn)

    while True:
        try:
            # Recevoir les données envoyées par le client
            data = conn.recv(1024)
            if not data:
                break
            # Afficher les données reçues dans la console du serveur
            print('Données reçues:', data.decode())
            data = data.decode()
            data = json.loads(data)
            nb = automate(data)
            if nb > 0:
                #Vérifier les niveaux
                if True:#Verifier_niveau():
                    current = 0
                    for key, value in data.items():
                        if isinstance(value, dict):
                            for key2,value2 in value.items():
                                executer_action(value2)
                                current = current + 1
                                conn.sendall(str(current/nb * 100).encode())
                        else:
                            executer_action(value)
                            current = current + 1
                            time.sleep(3)
                            conn.sendall(str(current/nb * 100).encode())
                    # Envoyez une réponse au client
                    print('OK')
                else:
                    conn.sendall(b'Niveau eau faible')
            else:
                print('ERROR')
                conn.sendall(b'ERROR!')         
        except ConnectionResetError:
            break

    # Fermer la connexion avec le client
    conn.close()
    connections.remove(conn)
    print('Connexion fermée:', addr)
    time.sleep(5)
# Fonction principale du serveur
def server():
    # Créer une socket d'écoute pour le serveur
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()

    print('Serveur démarré sur', HOST, ':', PORT)

    # Attendre les connexions des clients
    while True:
        conn, addr = s.accept()

        # Démarrer un nouveau thread pour gérer la connexion avec le client
        t = threading.Thread(target=client_thread, args=(conn, addr))
        t.start()

# Démarrer le serveur dans un thread séparé
server_thread = threading.Thread(target=server)
server_thread.start()

# Attendre les commandes du serveur
while True:
    command = input('> ')
    if command.startswith('exit'):
        parts = command.split()
        if len(parts) > 1:
            index = int(parts[1]) - 1
            if index >= 0 and index < len(connections):
                conn = connections[index]
                conn.sendall(b'Deconnexion demandee par le serveur')
                conn.close()
                connections.remove(conn)
                print('Connexion fermée:', conn.getpeername())
        else:
            print('Commande invalide')
    else:
        print('Commande invalide')