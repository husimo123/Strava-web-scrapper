import requests
from requests.exceptions import HTTPError
import json
from bs4 import BeautifulSoup
from math import radians, cos, sin, asin, sqrt
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
    return depart, arrivee, activity_number



# Organise coordinates according to geographic proximity
def organiseCoordinates(coordinates):
    # List of lists to get the store each run depending on geographical location.
    organised_activities = [[]]

    # Add the first activity to have something to compare
    organised_activities[0].append(coordinates[0])
    # Go through all coordinates
    for coord in coordinates:
        start = coord[0]
        # Boolean to check if we need to create a new location (element in organised_activity)
        bool = False
        for i in range (0,len(organised_activities)):

            if start == organised_activities[i][0][0]:
                bool = True
            elif (abs(start[0]- organised_activities[i][0][0][0]) < 0.004) and (abs(start[1]- organised_activities[i][0][0][1]) < 0.004) :
                organised_activities[i].append(coord)
                bool = True
        if not bool:
            organised_activities.append([])
            organised_activities[-1].append(coord)
    for i in range (0,len(organised_activities)):
        print(organised_activities[i])
    return organised_activities




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
    # Create json to update the file that corresponds to the data.
    json_data = {
        f"Distance" : f"{strongs[0].contents[0]}", # "Moving Time" : "10.00"
        f"Moving Time" : f"{strongs[1].contents[0]}",
        f"Pace" : f"{strongs[2].contents[0]}",
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

"""
coordinates = []
coordinates.append(getCoordinates(11718106606))
coordinates.append(getCoordinates(13742684320))
coordinates.append(getCoordinates(13757934814))
coordinates.append(getCoordinates(13870977175))
coordinates.append(getCoordinates(13887499261))
organiseCoordinates(coordinates)"""



# https://www.geeksforgeeks.org/program-distance-two-points-earth/
def distance(point1, point2):
    # The math module contains a function named
    # radians which converts from degrees to radians.

    lat1 = radians(point1[0])
    lat2 = radians(point2[0])
    lon1 = radians(point1[1])
    lon2 = radians(point2[1])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2

    c = 2 * asin(sqrt(a))

    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371

    # calculate the result
    return (c * r)


# driver code
lat1 = 53.32055555555556
lat2 = 53.31861111111111
lon1 = -1.7297222222222221
lon2 = -1.6997222222222223
p1 = [lat1, lon1]
p2 = [lat2, lon2]

# Calculate the distance from the GPX file
def getdistancedifference(activity_number):
    try:
        # Open file
        with open("C:/Users/hugos/PycharmProjects/strava/GPX_files/" + str(activity_number) + ".json") as json_file:
            data = json.load(json_file)

    except FileNotFoundError:
        print("File not found")
    else:
        d = 0

        # Sum the distance between each point
        for i in range(0, len(data['latlng']) -  1):
            d += distance(data['latlng'][i], data['latlng'][i + 1])

    return abs(float(d) - float(data["Distance"]))


getCoordinates(11718106606)
getActivityInfo(11718106606)

print(f"Distance hidden by Strava : {getdistancedifference(11718106606)} KM")
