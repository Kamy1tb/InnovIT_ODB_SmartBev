import socket
import serial
import json
import RPi.GPIO as GPIO
import re
import time
#ser = serial.Serial('/dev/arduinoSensors', 9600)
HOST = ''   # Laissez la valeur par défaut pour utiliser toutes les interfaces disponibles
PORT = 5000 # Port utilisé pour la communication
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.output(18, GPIO.LOW)
boisson =  {"VERSER_BOISSON_1":2,"VERSER_BOISSON_2":17}
toppings = {"VERSER_TOPPING_1":3}
expression_boisson = r"VERSER_BOISSON_([1234])"
expression_topping = r"VERSER_TOPPING_([1234])"
expression_quantite = r"VERSER_QUANT_([12345])"

def get_niveau(conteneur):
    if conteneur == "Water":
        ser2.write(0)
        # Attendre que l'Arduino réponde
        while ser.in_waiting == 0:
            pass
    # Lire la réponse de l'Arduino
        level = ser.readline().decode().strip()
        print(level)
        return level
    else:
        return 0
    
def reheat():
    commandeRelay = "allumeResistance"
    #ser2.write(commandeRelay)
    commandePompe = "VerserEau"
    GPIO.output(18, GPIO.HIGH) # Allume la LED
    time.sleep(2) # Attend 1 seconde
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
    #ser.write(commandeMotor.encode())
    # Attendre que l'Arduino réponde
    #while ser.in_waiting == 0:
       # pass
    # Lire la réponse de l'Arduino
    #etat = ser.readline().decode().strip()
    return 0#etat
    
def etat_next(state,action):
    if ( state == "S" ) and (action == "GET_GOBELET") :
        return "A"
    elif (state == "A") and (action == "REHEAT" ) :
        return "A1"
    elif ( state == "A1") and (re.match(expression_boisson,action)) :
        return "A2"
    elif ( state == "A2" ) and (re.match(expression_quantite,action)) :
        return "B"
    elif (state == "B" ) and (re.match(expression_boisson,action)):
        return "B1"
    elif (state == "B1") and ( re.match(expression_quantite,action)):
        return "B"
    elif( state == "B") and ( re.match(expression_topping,action)):
        return "B2"
    elif ( state == "B2" ) and ( re.match(expression_quantite,action)):
        return "C"
    elif (state == "B" ) and ( action == "GET_SPOON"):
        return "F"
    elif (state == "C" ) and ( action == "GET_SPOON"):
        return "F"
    elif ( state == "C") and ( re.match(expression_topping,action)):
        return "C1"
    elif ( state == "C1") and ( re.match(expression_quantite,action)):
        return "C"
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
        GPIO.output(boisson.get(action), GPIO.HIGH) # Allume la LED
        time.sleep(3) # Attend 1 seconde
        GPIO.output(boisson.get(action), GPIO.LOW) # Éteint la LED
        
    elif (re.match(expression_topping,action)):
        resultat = re.search(expression_topping, action)
        #conn.sendall(b"Versement d'un topping")
        print("Versement du topping numéro ", resultat.group(1))
        GPIO.output(toppings.get(action), GPIO.HIGH) # Allume la LED
        time.sleep(3) # Attend 1 seconde
        GPIO.output(toppings.get(action), GPIO.LOW) # Éteint la LED
    elif (action == "GET_SPOON"):
        #conn.sendall(b'depot de la cuillere')
        print("depot de la cuillère")
        GPIO.output(24, GPIO.HIGH) # Allume la LED
        time.sleep(3) # Attend 1 seconde
        GPIO.output(24, GPIO.LOW) # Éteint la LED
    else:
        print("quant")
# Créez un objet socket pour écouter les connexions entrantes
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

# Attendez une connexion entrante
conn, addr = s.accept()
print('Connecté avec', addr)

while True:
    # Recevez les données du client
    data = conn.recv(1024)
    if not data:
        break
    data = data.decode()
    data = json.loads(data)
    nb = automate(data)
    if nb > 0:
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
                conn.sendall(str(current/nb * 100).encode())
        # Envoyez une réponse au client
        print('OK')
    else:
        print('ERROR')
        conn.sendall(b'ERROR!')

# Fermez la connexion
conn.close()
