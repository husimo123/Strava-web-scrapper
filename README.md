# Strava scrapper

### Informations générales
Cet outil a été developpé dans le cadre du cours Cybersécurité/OSINT de 4A SAGI Polytech Angers. Sous la direction de 
Mr. Sébastien Lagrange.

Ce document a pour objectif d'expliquer le fonctionnement du script ainsi des buts d'utilisation.

L'objectif principal de ce projet est de montrer la quantité inquiétante d'information que l'on peut
trouver sur un compte public Strava, ainsi que les risques qui peuvent être liés a cette
information tel qu'une estimation de l'emplacement de l'habitation d'une personne (en admettant que
cette personne à assez de données disponibles sur son compte).

#### Bilan du projet

Malgré un temps d'execution très élevé, lors d'un test sur un camarade, le point estimé de départ est exactement où 
il démarre ses courses Strava, ce qui est preuve que le projet fonctionne. De plus l'indice de confiance est extremement élévé

### Comment utiliser l'outil
Afin d'utiliser l'outil, il faut un compte strava, la version gratuite suffit (utilisez un compte poubelle
il y a de fortes chances que le compte soit banni après plusieurs utilisations), ainsi qu'une personne cible
consentante pour le test de l'outil.

La premiere étape est de récupérer ses cookies. Ils sont disponibles une fois connecté sur le site
www.strava.com, ouvrez l'inspecteur (F12) et cliquez sur l'onglet Application sur Chrome ou Storage sur Firefox
cliquez sur les Cookies, et recopiez les 2 cookies 'sp' et '_strava4_session' dans le main.py.






![Screenshot 2025-03-18 204219.png](Screenshot%202025-03-18%20204219.png)




## Fonctionnement :
Il suffit d'entrer le **numéro d'athlète** de la personne dans la fonction _main()_ qui va ensuite 
récupérer toutes les activités de ce dernier. Ce numéro est accessible dans l'URL de la page du profil du coureur :
https://www.strava.com/athletes/NUMERO_A_COPIER. Le processus utilise selenium qui est très lent,
cependant, c'est la seule solution trouvée qui fonctionne a chaque itération pour récupérer les activités.
En effet, la page principale d'un compte est géré avec des composants REACT, qui sont donc chargés dynamiquement. 
La bibliothèque requests ne permet pas de les récupérer.

Par faute de ne pas avoir trouvé les données en clair et faute de temps, c'est la solution qui à été adoptée.
D'autres possiblilités plus efficaces peuvent marcher, tel que la bibliothèque "request-html" mais qui présente de
nombreux problèmes d'installation et une irrégularité dans les réponses de requètes.

Strava masque le point de départ des coureurs afin de cacher leur lieu de vie. En effet, souvent
les coureurs activent une activité Strava en quittant leur domicile, cependant lorsque leur profil est publique,
tout le monde a accès à leurs traces GPX, point de départ et d'arrivée ainsi que toutes leurs 
statistiques de courses.

Notre script est par définition un web scrapper qui vient chercher sur chaque page d'activités
d'un athlete donné :

- La trace GPX
- La distance totale parcourue
- Le temps total de déplacement
- Le rythme de course

Ces données sont ensuite stockés dans un fichier JSON pour faciliter
la lecture et leur traitement, en évitant des requètes redondantes.

Comme expliqué avant, Strava masque le point de départ et d'arrivée de course
avec un rayon inconnu, notre objectif est de déterminer statistiquement ce départ.

Nous calculons donc pour chaque activité la distance totale parcourue par rapport
à la distance annoncée par l'activité avec la fonction : 

    getdistancedifference()

Celle-ci somme la distance entre tous les points GPX de la course et la retire à
la distance annoncée.

Dans la fonction :

    estimate_depart()

On crée deux cercles avec la bibliothèque Shapely pour chaque activité, un pour 
le départ et un autre pour l'arrivée. C'est la distance calculée précédemment qui est utilisée
comme rayon, car l'endroit de départ réel est obligatoirement dans un rayon de la distance masquée 
par Strava.

Ces cercles sont ensuite stockés dans une liste pour déterminer l'intersection des
cercles avec la fonction *intersection* de Shapely. C'est cette intersection qui va 
être l'estimation du point de départ réel. Avec assez de données, en théorie, on est capable 
de trouver l'habitation d'une personne.



**Remarques :**

Afin d'éviter que le résultat soit erroné par des départs inhabituels, un système
de tri est implémenté. En effet, une personne peut être en vacances et donc courir 
dans une autre ville, voire un autre pays. Ce qui rendrait le calcul completement incohérent.

    organiseCoordinates()

Cette fonction tri les activités en fonction de leur proximité géographique dans un 
rayon de 1km. Au dela, c'est une autre zone d'intérèt qui est créé et qui sera
traité.


Lorsque tous les points sont traités, un graphique est affiché étant témoin de l'indice de 
confiance (le cercle violet par rapport aux cercles rouges). Ainsi que les coordonnées de l'estimation 
de chaque point de départ.

Le logiciel renvoie les coordonnées des points d'intérèt du coureur, il suffit de les copier dans Maps pour visualiser
l'endroit.


## Autre remarques et points d'amélioration :

J'ai été banni de strava avec mon compte de test, il est important d'utiliser un compte secondaire 
pour tester cet outil. J'ai ajouté des temps de pause pour limiter le risque de ban.

Malgré son fonctionnement, l'outil n'est pas optimisé, l'utilisation de selenium dans la
recherche des activités est un gros frein, bien que ce soit la seule solution fiable. 

De plus, l'outil effectue beaucoup trop de requêtes et réitère les fonctions sur les mêmes 
activités (ce qui est la cause du bannissement de mon compte). Le coût est assez élévé sur des grosses quantités d'activités.
C'est dû a la méthode de développement,j'ai commencé par analyser chaque page d'activités et puis j'ai développé le tri
des activités en fonctionde leurs coordonnées GPX, c'est en imbriquant les fonctions ensemble que j'aurai dû mieux gérer ça.

L'estimation du ou des points de départ réel n'est pas forcément très précis, on ne peut être certain du réel point 
de départ, car il suffit qu'un coureur parte toujours dans la meme direction pour fausser le calcul.
Cependant, cela est au dela de mon ressort.
