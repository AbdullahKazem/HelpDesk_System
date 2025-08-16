from flask import Flask, render_template, redirect, request, url_for, jsonify, session, Response, abort, send_from_directory
import psycopg2, openai
import requests
from functools import wraps
import importlib
from flask_mail import Mail, Message
import json
import traceback
import os, subprocess
from LayerDataFunctions import *
import LayerDataFunctions

import urllib.parse as urlparse

# Read full URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Parse the URL
url = urlparse.urlparse(DATABASE_URL)

conn = psycopg2.connect(
    dbname=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

app = Flask(__name__)

app.secret_key = os.urandom(24)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'tatbeekdb@gmail.com'
app.config['MAIL_PASSWORD'] = 'qnxkbbymrazxajkv'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/HelpDesk/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form["Username"]
        password = request.form["Password"]
        mail = request.form["Mail"]
        role = "user"
        try:
            conn = psycopg2.connect(DATABASE_URL)  
            dbCursor = conn.cursor()
            insertNewUser = "INSERT INTO users (name, password, mail, role) VALUES (%s, %s, %s, %s);"
            dbCursor.execute(insertNewUser, (username, password, mail, role))
            conn.commit()
            dbCursor.close()
            conn.close()
            print(username, password, mail)
            check = 1
            return render_template("registerPage.html", check=check)
        except (Exception):
            check = 0
            return render_template('registerPage.html', check=check)
    else:
        
        return render_template('registerPage.html', check = 0)

@app.route('/HelpDesk/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form["Username"]
        password = request.form["Password"]
        print(username, password)
        conn = psycopg2.connect(DATABASE_URL)  
        dbCursor = conn.cursor()
        getAllUsers = "select * from users order by id asc;"
        dbCursor.execute(getAllUsers)
        data = dbCursor.fetchall()
        print("Data: ", data)
        dbCursor.close()
        conn.close()
        check = 0
        if data != []:
            print("Pass: ", password, "data[0][2]: ", data[0][2])
            for row in data:
                if username == row[1]:

                    if password == row[2]:
                        check = 1
                        with open('Setup_Configrations.json', 'r') as file:
                            setupConfigrationData = json.load(file)
                        setupConfigrationData["userName"] = username
                        with open('Setup_Configrations.json', 'w') as file:
                            json.dump(setupConfigrationData, file, indent=4)
                        if row[4] == 'user':
                            return redirect(url_for("chat"))
                        else:
                            return redirect(url_for("home"))
                    else:
                        check = 0
            if check == 0:
                return render_template('loginPage.html', check=check)
        else:
            session.clear()
            return render_template('loginPage.html', check = 1)
    else:
        session.clear()
        return render_template('loginPage.html', check = 1)
        
@app.route('/HelpDesk/logout', methods=['POST', 'GET'])
def logout():
    session.clear()  # Clear the session
    return redirect(url_for('login')) 

@app.route('/HelpDesk/chat', methods=['POST', 'GET'])
def chat():
    if request.method == 'GET':

        return render_template("chat.html")
    
    elif request.method == 'POST':
        pass

@app.route('/HelpDesk/home', methods=['POST', 'GET'])
def home():
    if request.method == 'GET':
        with open('Setup_Configrations.json', 'r') as file:
            setupConfigrationData = json.load(file)
        print(setupConfigrationData["userName"])
        conn = psycopg2.connect(DATABASE_URL)  
        dbCursor = conn.cursor()
        getAllTickets = "select * from tickets where assigned = %s order by id asc;"
        dbCursor.execute(getAllTickets, (setupConfigrationData["userName"],))
        data = dbCursor.fetchall()

        dbCursor.close()
        conn.close()
        print("Data: ", data)
        rows = []
        numberOfRows = 0
        for row in data:
            if row[4] == 'Solved':
                continue
            numberOfRows = numberOfRows + 1
            ticketId = row[0]
            name = row[1]
            place = row[2]
            issue = row[3]
            status = row[4]
            rows.append([ticketId, name, place, issue, status])
        print("Rows: ", rows)
        rows, numberOfRows = (["" for i in range(5)], 1) if numberOfRows == 0 else (rows, numberOfRows)

        return render_template("attendance.html", rows = rows, numberOfRows = numberOfRows)
    
    elif request.method == 'POST':
        ticketId = request.form["ticketId"]
        status = request.form["status"]
        print("Ticket Id: ", ticketId, "status: ", status)

        conn = psycopg2.connect(DATABASE_URL)  
        dbCursor = conn.cursor()
        updateTicket = "update tickets set status = %s where id = %s ;"
        dbCursor.execute(updateTicket, (status, ticketId))
        conn.commit()
        dbCursor.close()
        conn.close()
        return redirect(url_for('home'))

@app.route('/HelpDesk/connect', methods=['POST', 'GET'])
def connect():
    if request.method == 'GET':
        with open('Setup_Configrations.json', 'r') as file:
            setupConfigrationData = json.load(file)
        print(setupConfigrationData["userName"])
        conn = psycopg2.connect(DATABASE_URL)  
        dbCursor = conn.cursor()
        getAllTickets = "select * from tickets where name = %s order by id asc;"
        dbCursor.execute(getAllTickets, (setupConfigrationData["userName"],))
        data = dbCursor.fetchall()

        dbCursor.close()
        conn.close()
        print("Data: ", data)
        rows = []
        numberOfRows = 0
        for row in data:
            numberOfRows = numberOfRows + 1
            name = row[1]
            place = row[2]
            issue = row[3]
            status = row[4]
            rows.append([name, place, issue, status])

        rows, numberOfRows = (["" for i in range(4)], 1) if numberOfRows == 0 else (rows, numberOfRows)

        return render_template("connect.html", rows = rows, numberOfRows = numberOfRows)
    
    elif request.method == 'POST':
        name = request.form["name"]
        place = request.form["place"]
        issue = request.form["issue"]
        status = "Pending"
        assigned = "ali"
        conn = psycopg2.connect(DATABASE_URL)  
        dbCursor = conn.cursor()
        insertNewTicket = "INSERT INTO tickets (name, place, issue, status, assigned) VALUES (%s, %s, %s, %s, %s);"
        dbCursor.execute(insertNewTicket, (name, place, issue, status, assigned))
        conn.commit()
        dbCursor.close()
        conn.close()
        return redirect(url_for('connect'))

if __name__ == "__main__":

    app.run(debug=True)
