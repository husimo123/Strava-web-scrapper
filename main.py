import requests
from requests.exceptions import HTTPError
import json
from bs4 import BeautifulSoup
stravasess = 'cqc8oep16vg427qd9gs7jiv8a8dkbbkt'
mysp = 'ef3b2692-42a5-4efe-b167-99dcaf02fe19'
myactivity = [13887499261, 13870977175, 13742684320,13734824328]
mydepart = []
myarrivee = []


# Request Data from website, return the text of the page ( with cookies )
def requestpage(url, activity_number):
    session = requests.Session()

    session.cookies.set('_strava4_session', stravasess)
    session.cookies.set('sp', mysp)

    # Il faut berner strava en le faisant croire qu'on est un navigateur classique, donc il faut ajouter des entetes.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Referer': 'https://www.strava.com/activities/' + str(activity_number)
    }
    try:
        response = session.get(str(url), headers=headers)
        response.raise_for_status()
    except HTTPError as httperr:
        print(f"Http error : {httperr}")
    else:
        print(f"success ! Status code : {response.status_code}")

    return response


#Get beginning and end coordinates of the run
def getCoordinates(activity_number):
    # Build URL for activiy
    url = "https://www.strava.com/activities/"+ str(activity_number) + "/streams?stream_types%5B%5D=timer_time&stream_types%5B%5D=latlng&_="
    # Request the data and load it into a json object.
    json_data = json.loads(requestpage(url, activity_number).text)

    to_file(json_data,"C:/Users/hugos/PycharmProjects/strava/GPX_files/" + str(activity_number) + ".json")
    # Parse values
    depart = json_data['latlng'][0]
    arrivee = json_data['latlng'][-1]
    # Organisation des traces en fonction du départ.
    # objectif : comparer les valeurs des nouvelles traces avec la moyenne de celles enregistés, si la différence est inférieure a
    # 0.003 ce qui correspond a 500 m
    organised_activities = []
    for i, activity in organised_activities:
        #Latitude
        if organised_activities == []:
            organised_activities[0].append(depart[0])
        elif (abs(depart[0]) - abs(avg(organised_activities[i]))) < 0.003:
            organised_activities[i].append(depart[0])

    print(organised_activities)
    return depart, arrivee


# Writing data to json file, with appropriate name and folder
def to_file(data, filename):
    json_object = json.dumps(data, indent=4)
    with open(filename, "w") as outfile:
        outfile.write(json_object)


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
        print(mydepart[i], myarrivee[i])
        deplat.append(mydepart[i][0])
        deplong.append(mydepart[i][1])
        arrlat.append(myarrivee[i][0])
        arrlong.append(myarrivee[i][1])
    #Calcul de la moyenne pour estimer le départ
    print("Le depart estimé est en : [" + str(avg(deplat)) + ", " + str(avg(deplong)) + " ]")
    print("L'arrivée estimé est en : [" + str(avg(arrlat)) + ", " + str(avg(arrlong)) + " ]")





# Request activity info
def getActivityInfo(activity_number):
    url = "https://www.strava.com/activities/" + str(activity_number)
    html = requestpage(url, activity_number)

    #html =requestpage(strava_session, mysp, url, activity_number)
    html = BeautifulSoup(html.text, features = "html.parser")
    # Concentrate on the section we want the data from
    ul_delimiter = html.find(attrs={"class": "inline-stats section"})
    #Get the value
    strongs = ul_delimiter.find_all('strong')
    #Get the corresponding text
    span = ul_delimiter.find_all('span')

    # Create json to update the file that corresponds to the data.
    json_data = {
        f"{span[0].text}" : f"{strongs[0].contents[0]}", # "Moving Time" : "10.00"
        f"{span[1].text}" : f"{strongs[1].contents[0]}",
        f"{span[2].text}" : f"{strongs[2].contents[0]}",
    }

    try:
        # Open file
        with open("C:/Users/hugos/PycharmProjects/strava/GPX_files/" + str(activity_number) + ".json") as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        print("File not found")
    else:
        # Add info to the end of the json
        data.update(json_data)
        # Write data to the file
        to_file(data,"C:/Users/hugos/PycharmProjects/strava/GPX_files/" + str(activity_number) + ".json")





