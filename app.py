from flask import Flask,render_template,request,redirect,session,url_for
import mysql.connector
import os
import pandas as pd
import requests
from random import choice
import string
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(10)

conect = mysql.connector.connect(host="127.0.0.1",user="root",password="Deekshitha@2605",database="seproject")
cursor= conect.cursor()

df = pd.read_csv('dataset.csv')
state_city = {}
city_place = {}

statelist = df["State"].tolist()
statelist = list(set(statelist))

citylist = df["City"].tolist()
citylist = list(set(citylist))

for i in range(0,df.shape[0]):
    if df.iloc[i]['State'] not in state_city.keys():
        state_city[df.iloc[i]['State']] = [df.iloc[i]['City']]
    elif df.iloc[i]['State'] in state_city.keys() and df.iloc[i]['City'] not in state_city[df.iloc[i]['State']]:
        state_city[df.iloc[i]['State']].append(df.iloc[i]['City'])

for i in range(0,df.shape[0]):
    if df.iloc[i]['City'] not in city_place.keys():
        city_place[df.iloc[i]['City']] = [df.iloc[i]['Name']]
    elif df.iloc[i]['City'] in city_place.keys() and df.iloc[i]['Name'] not in city_place[df.iloc[i]['City']]:
        city_place[df.iloc[i]['City']].append(df.iloc[i]['Name'])
@app.route('/')
def home():
    return render_template('home.html')

# Routing to the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    # return render_template('login.html')
    if 'username' in session:
        return render_template('userpage.html')
    else:
        return render_template('login.html')

@app.route('/userpage',methods=['GET'])
def userpage():
    if 'username' in session:
        return render_template('userpage.html')
    else:
        return redirect('/')


@app.route('/budget',methods=['GET', 'POST'])
def budget():
    if 'username' in session:
        return render_template('budget.html')
    else:
        return redirect('/')


@app.route('/authentication',methods=['POST','GET'])
def authentication():
    username = request.form.get('username') # taking input from the users
    password = request.form.get('password')

    # checking if the given username, password exist in the database
    cursor.execute("""select * from `users` where `username` like '{}' and `password` like '{}'""".format(username, password))
    userdata = cursor.fetchall()
    print(userdata)
    if len(userdata)>0:
        session['username']= userdata[0][0] # using session based authentication
        return redirect('/userpage')
    else:
        print("user not found")
        return redirect('/')

# adding users after registration
@app.route('/adduser',methods=['GET','POST'])
def adduser():
    username = request.form.get('username')
    # name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    cursor.execute("""insert into `users`(`username`,`email`,`password`) values ('{}','{}','{}')""".format(username, email,password))
    conect.commit()
    return redirect('/login')


@app.route('/befroute',methods=['GET', 'POST'])
def befroute():
    # if 'username' in session:
    return render_template('befroute.html', state_city_dict=state_city, city_place_dict=city_place)
    # else:
    #     return render_template('home.html')

@app.route('/submit', methods=['POST'])
def submit():
    selected_places = request.form.getlist('selectedPlaces')
    selected_start = request.form.getlist('selectedStart')
    import googlemaps

    gmaps_client = googlemaps.Client(key='AIzaSyBrKKiqxY2fD8RW2wCPpA9-_b-kPE2H-AA')

    matrix_result = gmaps_client.distance_matrix(selected_places, selected_places, mode="driving")
    g = []

    if matrix_result["status"] == "OK":

        for i, origin in enumerate(selected_places):
            l = []
            for j, destination in enumerate(selected_places):
                distance = matrix_result["rows"][i]["elements"][j]["distance"]["text"]
                distance = distance.replace("km", "")
                distance = distance.replace("m", "")
                distance = float(distance)
                duration = matrix_result["rows"][i]["elements"][j]["duration"]["text"]
                # print("Distance:", distance)
                l.append(distance)
            g.append(l)
        print(g)

    else:
        print("Distance matrix retrieval failed.")

    # Do something with the selected places
    print(selected_places)
    print(selected_start)
    locpoints = []
    # startpoint = ""
    for i in selected_places:
        for j in range(len(df)):
            if df.iloc[j]['Name'] == i:
                locpoints.append(df.iloc[j]['Coordi,ats'])
            if df.iloc[j]['Name'] == selected_start[0]:
                startpoint = df.iloc[j]['Coordi,ats']
    print(locpoints)

    sourcepoint = selected_places.index(selected_start[0])

    graph = g
    pathll = []

    print(traveling_salesman(graph, sourcepoint))
    for i in traveling_salesman(graph, sourcepoint):
        a, b = locpoints[i].split(",")
        a = float(a)
        b = float(b)
        pathll.append([a, b])
    print(pathll)
    return render_template('map.html', lat_lng_list=pathll)


def tsp(path, graph, visited, cost, min_cost, min_path):

    if len(path) == len(graph):
        if cost < min_cost:
            min_cost = cost
            min_path = path
        return min_path, min_cost

    for node in range(len(graph)):
        if not visited[node]:
            visited[node] = True
            new_path = path + [node]
            new_cost = cost + graph[path[-1]][node]
            min_path, min_cost = tsp(new_path, graph, visited, new_cost, min_cost, min_path)
            visited[node] = False
    return min_path, min_cost

def traveling_salesman(graph, source):
    min_cost = float("inf")
    min_path = None
    visited = [False] * len(graph)

    visited[source] = True
    path, cost = tsp([source], graph, visited, 0, min_cost, min_path)
    visited[source] = False

    return path


# routing when clicked on logout
@app.route('/logout')
def logout():
    session.pop('username') # popping the username from session when logged out
    return redirect('/')

if __name__ == '__main__':
    app.run(port=6080)


# print(df['Name'])
