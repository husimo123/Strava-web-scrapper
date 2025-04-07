import requests
from requests.exceptions import HTTPError
import json
from bs4 import BeautifulSoup
from math import radians, cos, sin, asin, sqrt
from shapely.geometry import Point
import matplotlib.pyplot as plt


stravasess = 'cqc8oep16vg427qd9gs7jiv8a8dkbbkt'
mysp = 'ef3b2692-42a5-4efe-b167-99dcaf02fe19'

myactivity = [13887499261, 13870977175, 13742684320,13734824328,
              11718106606 , 14003910377,13985575843, 13307719262,
              14056422650]
mydepart = []
myarrivee = []

colors = [
    '#FF0000',  # Red
    '#FFA500',  # Orange
    '#FFFF00',  # Yellow
    '#008000',  # Green
    '#0000FF',  # Blue
    '#4B0082',  # Indigo
    '#EE82EE',  # Violet
    '#FFC0CB',  # Pink
    '#800000',  # Maroon
    '#FF69B4',  # Hot Pink
    '#00FFFF',  # Cyan
    '#808000',  # Olive
    '#800080',  # Purple
    '#00FF00',  # Lime
    '#FF00FF',  # Magenta
    '#C0C0C0',  # Gray
    '#808080',  # Dark Gray
    '#FFFFFF',  # White
    '#000000',  # Black
    '#964B00',  # Brown
    '#FFD700',  # Gold
    '#008000',  # Forest Green
    '#00BFFF',  # Deep Sky Blue
    '#4B0082',  # Navy Blue
    '#FF99CC',  # Pastel Pink
    '#CCFFCC',  # Pale Green
    '#CCCCFF',  # Light Blue
    '#FFCC99',  # Light Orange
    '#99CCFF',  # Sky Blue
    '#CC99FF',  # Pastel Purple
    '#FFFF99',  # Light Yellow
    '#99FF99',  # Pale Lime
    '#FF99FF',  # Pastel Magenta
    '#CCFF99',  # Light Green
    '#99CCCC',  # Pale Cyan
    '#CCCC99',  # Light Beige
    '#FFCCCC',  # Light Pink
    '#CCCC00',  # Light Olive
    '#CC99CC',  # Pastel Gray
    '#999999',  # Dark Gray Blue
    '#666666',  # Dark Gray
    '#333333',  # Very Dark Gray
    '#0099CC',  # Teal
    '#CC0099',  # Plum
    '#99CC00',  # Lime Green
    '#009999',  # Aqua
    '#CC00CC',  # Fuchsia
    '#9900CC',  # Purple
    '#00CC99',  # Sea Green
    '#CC9900',  # Golden Brown
    '#0099FF',  # Sky Blue
    '#FF0099',  # Hot Pink
    '#99FF00',  # Chartreuse
    '#FFCC00',  # Amber
    '#00FFCC',  # Pale Turquoise
    '#CC00FF',  # Pastel Purple
    '#FF00CC',  # Magenta
    '#CCFF00',  # Lime Green
    '#00CCCC',  # Pale Aqua
    '#CCCCFF',  # Light Lavender
    '#FFCCCC',  # Pastel Pink
    '#CCCC00',  # Beige
    '#CC99FF',  # Pastel Magenta
    '#99CCCC',  # Pale Cyan
    '#CCCC99',  # Light Gray Brown
    '#FFCC99',  # Light Orange
    '#99CCFF',  # Sky Blue
    '#CCFFCC',  # Pale Green
    '#FF99CC',  # Pastel Pink
    '#CCFF99',  # Light Green
    '#99FFCC',  # Pale Turquoise
    '#FFCCFF',  # Pastel Magenta
    '#CCCCFF',  # Light Lavender
    '#CCFFFF',  # Pale Aqua
    '#FFFFCC',  # Light Yellow
    '#CCFFCC',  # Pale Green
    '#FFCCCC',  # Pastel Pink
    '#CCCC00',  # Beige
    '#CC99CC',  # Pastel Gray
    '#999999',  # Dark Gray Blue
    '#666666',  # Dark Gray
    '#333333',  # Very Dark Gray
]


# Request Data from website, return the text of the page ( with cookies )
def requestpage(url, activity_number):
    session = requests.Session()

    session.cookies.set('_strava4_session', stravasess)
    session.cookies.set('sp', mysp)

    # Il faut berner strava en le faisant croire qu'on est un navigateur classique, donc il faut ajouter des entetes.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Referer': 'https://www.strava.com/activities/' + str(activity_number) + "/overview"
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
    act  = [[]] # Same list as above but only activities.
    # Add the first activity to have something to compare
    organised_activities[0].append(coordinates[0])
    act[0].append(coordinates[0])
    print(organised_activities)
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
                act[i].append(coord[2])
                bool = True
        if not bool:
            organised_activities.append([])
            organised_activities[-1].append(coord)
            act.append([])
            act[-1].append(coord[2])
    return organised_activities, act


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

# Estimate the main start point
def estimate_depart(list_activity):
    # Creer la figure
    plt.figure()
    area = 0
    circles = []
    for i in range(len(list_activity)):
        # Info of all activities
        dep, arr, act = getCoordinates(list_activity[i])
        getActivityInfo(list_activity[i])
        distance = getdistancedifference(list_activity[i])

        # On ajoute les points de départ et d'arrivés sous la forme d'objet Shapely
        circles.append(Point((dep[0],dep[1])).buffer(distance))
        circles.append(Point((arr[0],arr[1])).buffer(distance))

        # On ajoute les points au tracé.
        plt.gca().add_patch(plt.Circle((dep[0], dep[1]), distance , color='r', alpha=0.5))
        plt.gca().add_patch(plt.Circle((arr[0], arr[1]), distance , color='r', alpha=0.5))


    # Calculate the area of intersection and union of all circles
    intersection_area = circles[0]
    union_area = circles[0]
    for circle in circles[1:]:
        intersection_area = intersection_area.intersection(circle)
        union_area = union_area.union(circle)

    # Plot the intersection area
    if intersection_area.area >0:
        plt.gca().add_patch(plt.Polygon(list(intersection_area.exterior.coords), color='b', alpha=0.5))
        # On recupere le centre de l'intersection et on la marque sur le plot
        centroid = intersection_area.centroid
        plt.scatter([centroid.x], [centroid.y], color='k', marker='x', s=100)
        # on renvoit les coordonées du centre.
        print("Intersection centroid:", centroid.x, centroid.y)
    else:
        print("No intersection found")

    # On affiche le plot.
    plt.axis('equal')
    plt.show()

"""
coordinates = []

for activity in myactivity:
    coordinates.append(getCoordinates(activity))
    getActivityInfo(activity)

organised_coord, organised_activities = organiseCoordinates(coordinates)
for i in range(len(organised_activities)):
    if len(organised_activities[i]) > 1:
        estimate_depart(organised_activities[i])
    else:
        print(f"Skipped {organised_activities[i]} because lacked enough data to estimate departure")

"""