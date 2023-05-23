from flask import Flask,render_template,request,redirect,session
import mysql.connector
import os
from random import choice
import string
from datetime import datetime
from code import statelist
from code import citylist
from code import state_city
from code import city_place

app = Flask(__name__)
app.secret_key = os.urandom(10)

conect = mysql.connector.connect(host="127.0.0.1",user="root",password="zxcvbnm9",database="seproject")
cursor= conect.cursor()
@app.route('/')
def home():
    return render_template('index.html')

# Routing to the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    # return render_template('login.html')
    if 'username' in session:
        return render_template('userpage.html')
    else:
        return render_template('login.html')


# routing to the registration page
@app.route('/register')
def register():
    return render_template('register.html')

# routing to the userpage
@app.route('/userpage')
def userpage():
    if 'username' in session:
        return render_template('userpage.html')
    else:
        return redirect('/')


@app.route('/befroute',methods=['GET', 'POST'])
def befroute():
    state_city_dict = {
        "California": ["Los Angeles", "San Francisco"],
        "New York": ["New York City", "Albany"]
    }

    city_place_dict = {
        "Los Angeles": ["Place 1", "Place 2", "Place 3"],
        "San Francisco": ["Place 4", "Place 5", "Place 6"],
        "New York City": ["Place 7", "Place 8", "Place 9"],
        "Albany": ["Place 10", "Place 11", "Place 12"]
    }

    return render_template('befroute.html', state_city_dict=state_city, city_place_dict=city_place)


@app.route('/budget',methods = ['GET'])
def budget():
    if 'username' in session:
        return render_template('budget.html')
    else:
        return render_template('login.html')


# authentication after clicking on login
@app.route('/authentication',methods=['POST'])
def authentication():
    username= request.form.get('username') # taking input from the users
    password= request.form.get('password')

    # checking if the given username, password exist in the database
    cursor.execute("""select * from `users` where `username` like '{}' and `password` like '{}'""".format(username,password))
    users = cursor.fetchall()
    if len(users)>0:
        session['username']= users[0][2] # using session based authentication
        return redirect('/userpage')
    else:
        print("user not found")
        return redirect('/')


# adding users after registration
@app.route('/adduser',methods=['POST'])
def adduser():
    username = request.form.get('username')
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    cursor.execute("""insert into `users`(`username`,`name`,`email`,`password`) values ('{}','{}','{}','{}')""".format(username,name,email,password))
    conect.commit()
    return redirect('/')

@app.route('/submit', methods=['POST'])
def submit():
    selected_places = request.form.getlist('selectedPlaces')
    # Do something with the selected places
    print(selected_places)
    # Return a response or redirect to another page
    return 'Form submitted successfully'

# routing when clicked on logout
@app.route('/logout')
def logout():
    session.pop('username') # popping the username from session when logged out
    return redirect('/')

if __name__ == '__main__':
    app.run()

