# Strava scrapper

### General overview
This document is dedicated to explaining what the script does and what it
it is meant to be used for.

The main objective of this project is to show the amount of information 
that can be found on Strava, and the potential risks that can be linked
to said information, such as a precise guess (considering there is enough 
available information) of the location of a persons house.


### How to use the tool
The requirements for the functioning of the code is a strava account, the free version 
and a person that accepts to be the subject of test.


The first step is to get your cookie data. Which can be found once connected
on the www.strava.com website. Simply open the inspector (F12) and 
go to the Application tab and down to the Cookies. Here you should have a few cookies,
you need to copy the 'sp' and '_strava4_session' cookies.


![Screenshot 2025-03-18 204219.png](Screenshot%202025-03-18%20204219.png)

You will need to replace these in the _stravasess_ and _mysp_ in the _main.py_.


The next data you will need is the activities you want to analyse, which you
will need to add to the _myactivities_ list. You can find these in the url with the following
format :

https://www.strava.com/activities/ACTIVITYNUMBERTOCOPY

## Fonctionnement :
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
rayon de 300 mètres. Au dela, c'est une autre zone d'intérèt qui est créé et qui sera
traité.
