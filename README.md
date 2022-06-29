# Codes-en-Python-Memoire-Packing-Coloring
Le problème de coloration de graphe consiste à trouver le nombre minimum de couleurs (appelé nombre chromatique) nécessaire pour colorier les nœuds du graphe de telle sorte que deux nœuds voisins aient des couleurs différentes.

EXECUTION DES PROGRAMMES
-------------------------

Pour exécuter les différents programmes du mémoire de recherche on a 2 possibilités :

1) Soit on exécute le programme global (Code_Python_final_packing_Coloring) qui reprend tous les modèles ILP implémentés sous forme de méthodes en python et appelés dans un programmme principal de type MAIN ; alors quelle est la procédure : 

        * Pour cela, il faudra installer l'environnement de développement en python qui est l'IDE Jupyter Notebook ;
         
        * Ensuite, il faudra créer votre fichier programme avec l'extension .ipynb. Ce fichier contiendra votre code ainsi que l’output généré par ce code lors de son exécution ;
        
        * Ensuite, on utilisera une application web, qui est chargée d’afficher les notebooks (possibilité de modifier le code) et permet à l’utilisateur d’interagir ;
        
        * Enfin, un kernel, chargé d’exécuter le code contenu dans le notebook. Il s’agit d’un kernel Python ;
         
        * Si toutes ces étapes sont remplies, alors vous cliquez sur le bouton "Exécuter" qui se trouve dans l'application web appelée Jupyter.
         
            
 2) Soit on peut exécuter chaque modèle de façon individuelle de manière à vouloir mieux comprendre le fonctionnement du modèle :
            
        * Pour cela, nous allons utiliser un autre environnement de développement et d'exécution qui est "Anaconda Powershell Prompt (anaconda3)" ;
           
        * Comme exemple, nous allons montrer comment exécuter un modèle en utilisant quelques lignes de commandes :
            
              (base) PS C:\Users\landr> cd .\pyomo1\  ............ pyomo1 est le repertoire où se trouve le fichier qui contient le code et peut s'appeller programme.py
                      
              (base) PS C:\Users\landr\pyomo1> pyomo solve --solver=cplex DEMO.modeleiLP_ASS6.py............pyomo solve --solver=cplex est la ligne de commande 
              qui permet de compiler et d'exécuter le solver et il faut lui passer en paramètre le fichier programme DEMO.modeleiLP_ASS6.py pour l'exécution du modèle.
