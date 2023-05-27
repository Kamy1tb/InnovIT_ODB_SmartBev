import socket
import json
import time
import serial
import threading
# Définition de l'adresse IP et du port du serveur
HOST = ''
PORT = 3000

#serSensors = serial.Serial('/dev/ttyACM1',9600)

def get_niveau():
    serSensors.write(b'1')
    while serSensors.in_waiting == 0:
        pass
    level = serSensors.readline().decode()
    level = json.loads(level)
    return level


connections = []



def generate_data(levels=[], recipients=[], temperatures=[]):
    # Vérification de la validité des données
    for level in levels:
        if not all(key in level for key in ['name', 'level']):
            raise ValueError('Chaque objet "level" doit contenir une clé "name" et une clé "level".')

    for recipient in recipients:
        if not all(key in recipient for key in ['name', 'level']):
            raise ValueError('Chaque objet "recipient" doit contenir une clé "name" et une clé "level".')

    for temperature in temperatures:
        if not all(key in temperature for key in ['name', 'level']):
            raise ValueError('Chaque objet "temperature" doit contenir une clé "name" et une clé "level".')

    # Construction de l'objet JSON
    data = {}
    if levels:
        data['levels'] = levels
    if recipients:
        data['recipients'] = recipients
    if temperatures:
        data['temperatures'] = temperatures

    # Encodage de l'objet JSON en chaîne de caractères
    json_data = json.dumps(data)

    # Retourner l'objet JSON
    return json_data


# Boucle d'attente des connexions entrantes
def client_thread(conn, addr):
    print('Nouvelle connexion:', addr)
    connections.append(conn)

    while len(connections) > 0:
        try:
            #level = get_niveau()
            levels = [
            {'name': 'water', 'level': 78}, #int(level['waterLevel'])},
            {'name': 'coffee', 'level': 50}
            ]

            recipients = [
            {'name': 'gobelet', 'level': 10},
            {'name': 'spoon', 'level': 60}
            ]

            temperatures = [
            {'name': 'water', 'level': 5}#int(level['temperature'])}
            ]

            json_data = generate_data(levels=levels, recipients=recipients, temperatures=temperatures)
            conn.sendall(json_data.encode())
            time.sleep(2)
                        
        except (ConnectionResetError,BrokenPipeError) as e:
            conn.close()
            break
        except (json.decoder.JSONDecodeError) as je:
            time.sleep(3)
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