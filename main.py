from flask import Flask,render_template,request,redirect,session
import mysql.connector
import os
from random import choice
import string
from datetime import datetime


app = Flask(__name__)
app.secret_key=os.urandom(10)

conect = mysql.connector.connect(host="127.0.0.1",user="root",password="zxcvbnm9",database="amlogin")
cursor= conect.cursor()