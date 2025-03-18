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



# infos pour moi

on va faire tous les calculs d'endroit a la fin, puis on va trier les 
fichiers dans des dossiers a la fin, meme si c'est pas opti de fou ca m'évite de tout réécrire.


Il faut savoir que la difference entre *
    Between [47.478668, -0.565233] and [47.478889, -0.565208]: 47.478889−47.478668=0.000221 degrees
    Between [47.478571, -0.564751] and [47.478962, -0.56484]: 47.478962−47.478571=0.000391 degrees

These differences are smaller than 0.005 degrees. To find the actual distance, you would multiply these differences by 111.32 kilometers per degree. For example, for the first pair:
0.000221×111.32=0.0246 kilometers or approximately 24.6 meters.

And for the second pair:
0.000391×111.32=0.0435 kilometers or approximately 43.5 meters