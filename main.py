from flask import Flask,render_template,request,redirect,session
import mysql.connector
import os
from random import choice
import string
from datetime import datetime


app = Flask(__name__)
app.secret_key=os.urandom(10)


conect = mysql.connector.connect(host="127.0.0.1",user="root",password="Deekshitha@2605",database="seproject")
cursor= conect.cursor()

# routing to the login page
@app.route('/')
def home():
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

# authentication after clicking on login
@app.route('/authentication',methods=['POST'])
def authentication():
    email= request.form.get('email') # taking input from the users
    password= request.form.get('password')

    # checking if the given username, password exist in the database
    cursor.execute("""select * from `users` where `email` like '{}' and `password` like '{}'""".format(email,password))
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

# routing when clicked on logout
@app.route('/logout')
def logout():
    session.pop('username') # popping the username from session when logged out
    return redirect('/')

if __name__ == "__main__":
    app.run()
