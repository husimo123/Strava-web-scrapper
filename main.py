import requests
import json

stravasess = 'cqc8oep16vg427qd9gs7jiv8a8dkbbkt'
mysp = 'ef3b2692-42a5-4efe-b167-99dcaf02fe19'
myactivity = [13887499261, 13872537505, 13870977175]
mydepart = []
myarrivee = []

#Get beginning and end coordinates of the run
def getCoordinates(activity_number, strava_session, sp):
    session = requests.Session()

    session.cookies.set('_strava4_session',strava_session )
    session.cookies.set('sp', sp)

    #Il faut berner strava en le faisant croire qu'on est un navigateur classique, donc il faut ajouter des entetes.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Referer': 'https://www.strava.com/activities/'+str(activity_number)
    }
    response = session.get(
        'https://www.strava.com/activities/'+str(activity_number)+'/streams?stream_types%5B%5D=timer_time&stream_types%5B%5D=latlng&_=',
    headers=headers

    )
    #translate data to json
    json_data = json.loads(response.text)
    depart = json_data['latlng'][0]
    arrivee =  json_data['latlng'][-1]
    return depart, arrivee

# Calcul de la valeur moyenne dans une liste
def avg(list_depart):
    moydep = 0
    for i in range(len(list_depart)):
        moydep += list_depart[i]
    return moydep / len(list_depart)


def main():
    #On cherche les coordonées de départ et d'arrivée et on les met dans une liste
    for i in range(len(myactivity)):
        depart, arrivee = getCoordinates(myactivity[i], stravasess, mysp)
        mydepart.append(depart)
        myarrivee.append(arrivee)
    # listes pour stocker par latitute et longitude
    deplat= []
    deplong= []
    arrlat= []
    arrlong = []

    #parsage des valeurs des json
    for i in range(len(mydepart)):
        deplat.append(mydepart[i][0])
        deplong.append(mydepart[i][1])
        arrlat.append(myarrivee[i][0])
        arrlong.append(myarrivee[i][1])
    #Calcul de la moyenne pour estimer le départ
    print("Le depart estimé est en : [" + str(avg(deplat)) + ", " + str(avg(deplong)) + " ]")
    print("L'arrivée estimé est en : [" + str(avg(arrlat)) + ", " + str(avg(arrlong)) + " ]")



main()