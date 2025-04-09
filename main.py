import requests
from requests.exceptions import HTTPError
import json
from bs4 import BeautifulSoup
from math import radians, cos, sin, asin, sqrt
from shapely.geometry import Point
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import sys


# Cookies
stravasess = 'Enter your Strava session ID'
mysp = 'Enter your SP here'

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

    # Eviter le crash si on a une mauvaise réponse du serveur.
    if(response.status_code == 429):
        print(f"Error, status code : {response.status_code}, you have most likely been banned...")
        sys.exit()
    elif(response.status_code != 200):
        print(f"Error, status code : {response.status_code}")
    else:
        print(f"Success ! Status code : {response.status_code}")
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
    act[0].append(coordinates[0][2])
    print(organised_activities)
    # Go through all coordinates
    for coord in coordinates:
        start = coord[0]
        # Boolean to check if we need to create a new location (element in organised_activity)
        bool = False
        for i in range (0,len(organised_activities)):
            point1 = [start[0], start[1]]
            point2 = [organised_activities[i][0][0][0], organised_activities[i][0][0][1]]
            if start == organised_activities[i][0][0]:
                bool = True
            #If the distance between the points is less than a kilometer
            elif (distance(point1, point2) < 1):
                organised_activities[i].append(coord)
                act[i].append(coord[2])
                bool = True

        # if the activity was not added to a list of activities then a new departure point is added.
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
    return centroid.x, centroid.y


# Get the activities on each page
def getPageActivites(urls):
    """Selenium driver config"""
    profile = webdriver.FirefoxProfile()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    profile.set_preference("general.useragent.override", user_agent)
    options = webdriver.FirefoxOptions()
    options.headless = True
    browser = webdriver.Firefox(options=options)

    try:
        # On se connecte d'abord a strava
        browser.get("https://strava.com")

        # On ajoute nos cookies pour se connecter a la session
        cookies = [
            {
                'name': '_strava4_session',  # Required field
                'value': 'cqc8oep16vg427qd9gs7jiv8a8dkbbkt',  # Required field
                'domain': 'strava.com',  # Optional, but recommended
                'path': '/',  # Optional, but recommended
                'httpOnly': True,  # Optional
                'secure': True  # Optional
            },
            {
                'name': 'sp',  # Required field
                'value': 'ef3b2692-42a5-4efe-b167-99dcaf02fe19',  # Required field
                'domain': 'strava.com',  # Optional, but recommended
                'path': '/',  # Optional, but recommended
                'httpOnly': True,  # Optional
                'secure': True  # Optional
        }
        ]

        # On ajoute les cookies
        for cookie in cookies:
            browser.add_cookie(cookie)
    except TimeoutException:
        print("I give up...")

    activities = []
    # Once connected we iterate the pages :
    for url in urls:
        print(f"URL : {url}")
        print(f"Activities : {activities}")
        try:
            # On se connecte a la bonne adresse IP
            browser.get(url)
            # On attend que le javascript charge correctement, si on dépasse 10 secondes on abandonne
            timeout_in_seconds = 10
            WebDriverWait(browser, timeout_in_seconds).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'UDqjM'))  # Adjust this to wait for a specific element if needed
            )
            # On recupere le code
            html = browser.page_source
            html = BeautifulSoup(html, features="html.parser")
            # Get all the corresponding infos
            classes = html.find_all(attrs={"class": "UDqjM"})


            # Get the activity from the classes
            for element in classes:
                # Find all <a> tags within the current element
                links = element.find_all('a')
                for link in links:
                    # Add the activity
                    href = link.get('href')
                    activity = href[12:]
                    activities.append(activity)
        except TimeoutException:
            print("I give up...")

    browser.quit()

    return activities
# Get the links from the bar graph
def getAtheleteActivities(athletenumber):
    html = requestpage("https://www.strava.com/athletes/" + str(athletenumber), 124854044)

    # html =requestpage(strava_session, mysp, url, activity_number)
    html = BeautifulSoup(html.text, features="html.parser")
    all_activities = []
    for a in html.find_all('a', href=True):
        if ("athletes" and "#interval" in a['href']):
            all_activities.append("https://strava.com" + a['href'])



    return all_activities

def main(athletenumber):
    # Get all the links
    all_links = getAtheleteActivities(athletenumber)
    all_activities = getPageActivites(all_links)

    coordinates = []
    for activity in all_activities:
        # Pour eviter le ban
        time.sleep(3)
        coordinates.append(getCoordinates(activity))
        getActivityInfo(activity)

    # Organise coordinates
    organised_coord, organised_activities = organiseCoordinates(coordinates)
    estimated_coordinates = []
    for i in range(len(organised_activities)):
        if len(organised_activities[i]) > 1:
            # Pour eviter le ban
            time.sleep(5)
            est_lat, est_lon = estimate_depart(organised_activities[i])
            estimated_coordinates.append([est_lat, est_lon])
        else:
            print(f"Skipped {organised_activities[i]} because lacked enough data to estimate departure")

    # Affichage des POI : Point of interest (les différents départs du coureur)
    print(f"Estimated coordinates of each POI : {estimated_coordinates}")
main(124854044)


