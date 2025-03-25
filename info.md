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
on the www.strava.com website. Simple open the inspector (F12) and 
go to the Application tab and down to the Cookies. Here you should have a few cookies,
you need to copy the 'sp' and '_strava4_session' cookies.


![Screenshot 2025-03-18 204219.png](Screenshot%202025-03-18%20204219.png)

You will need to replace these in the _stravasess_ and _mysp_ in the _main.py_.


The next data you will need is the activities you want to analyse, which you
will need to add to the _myactivities_ list. You can find these in the url with the following
format :

https://www.strava.com/activities/ACTIVITYNUMBERTOCOPY

# Comment qu'on fait mtn :
On prend tous les points qu'on a, départ et arrivé avec la distance parcourue dans
la cachée. On fait un cercle de diametre de la distance cachée.
Au bout de plusieurs itérations on va avoir les cercles qui se 
recouvrent, la ou ils se recouvrent c'est la zone de départ estimée.

En axe d'amélioration on peut générer un lien qui montre directement sur Google
Maps ou c'est.