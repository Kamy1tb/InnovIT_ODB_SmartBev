# Distributeur de café intelligent

Dans le cadre d'un projet à l'école nationnale supérieure d'informatique d'Alger, il nous a été demandé de créer un système de gestion de distributeurs de café intelligent. Ce repository comporte la partie IOT de ce projet, ou l'on a utilisé pour créer un prtotype de distributeur en simulant les fonctions mécaniques tout en utilisant diverses capteurs afin d'emettre des notificcations et des alertes à chaque anomalie ou panne. 
## Table des matières

- [Aperçu](#aperçu)
- [Installation](#installation)
- [Licence](#licence)

## Aperçu

Ce repository comporte deux branches contenant le code des objets intelligents. D'une partie on apperçois le code de la raspberry et de l'autre le code de deux arduinos Méga. Concernant les arduino, on trouvera le code de l'arduino qui simule la partie mécanique qui va manipuler les différents moteurs utilisés pour créer le protoype. Et cela, en créant un ensemble de directives pour manipuler chaque moteur. Pour le deuxième code arduino, il contiendra les différentes valeurs des capteurs de niveau et securité qui vont etre rassemblé en un format JSON qui pourra etre envoyé via Serial afin de les utiliser. On passe au code de la raspberry pi 4, qui va jouer le role de l'ordinateur de la machine à café, on elle va se connecter en réseau local avec la tablette du distributeur ou son code se trouve sur le repo [InnovIT_2CS_Project_AppTablette](https://github.com/RyanBelbachir/InnovIT_2CS_Project_AppTablette). Cette tablette envoie la recette commandé ar l'utilisateur, que la raspberry avec ce code va la traduire en série de commandes de moteurs et va les communiquer d'un façon synchrone avec le Arduino de la partie mécaniqeu. La raspberry reçois par l'arduino des capteurs les différentes valeurs de ces derniers qui vont etre utilisé afin d'envoyer diverses notifications à l'application de maintenance et aussi de mettre à jour la valeurs des dashboards en insérant les changements dans la base de données du système. 

## Installation

Pour installer les diverses codes, il suffira de uploader grace à Arduino IDE les codes des arduinos. Il faudra effectuer également les branchements nécessaires se trouvant dans le rapport de l'ordinateur de bord. Concernant la raspberry, Il faudra cloner le projet avec la directive (git clone https://github.com/Kamy1tb/InnovIT_ODB_SmartBev) dans la branche Raspberry pi. Ensuite, de lancer les diverses scripts en utilisant la directive ( python ./script.py)


## Licence

Ce projet est sous licence du groupe d'étudiants de l'esi InnovIT du projet 2CS 2022/2023

