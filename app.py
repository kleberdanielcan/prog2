from flask import Flask, render_template, request
import csv
import os
import json
from urllib.request import urlopen 
import pandas as pd 
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "calories.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

class Calculator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Float)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    calories = db.Column(db.Float)



@app.route("/")
def login():
    """
    Summary: 
        Starting point of the application
    Returns:
        The home.html page
    """
    return render_template("home.html")

@app.route("/calculate",  methods = ['POST'])
def calculate():
    """
    Summary: 
        Calculate Calories based on the form input
    Returns:
        The calculated calories with the calories.html page
    """
    gender = request.form.get('gender')
    name= request.form['name']
    bodyweight = float(request.form['bodyweight'])
    height = float(request.form['height'])
    age = float(request.form['age'])
    breakfast = float(request.form['breakfast'])
    lunch = float(request.form['lunch'])
    dinner = float(request.form['dinner'])
    
    if gender == "Männer":
        Calorie = 666.47 + (13.7 * bodyweight) + (5 * height) - (6.8 * age)
    else:
        Calorie = 665.1 + (9.6 * bodyweight) + (1.8 * height) - (4.7 * age)  

    calorie={}
    calorie['calorie'] = Calorie
    calorie['breakfast'] = breakfast
    calorie['lunch'] = lunch
    calorie['dinner'] = dinner     

    record = Calculator(name=name, age=age, height=height, weight=bodyweight, calories=Calorie)
    db.session.add(record)
    db.session.commit()
    return render_template("calories.html",calorie=calorie)

@app.route("/records")
def records():
    """
    Summary: 
        List all saved records
    Returns:
        Returns the page with all saved records
    """
    records = Calculator.query.all()
    return render_template("records.html",records=records)

if __name__ == "__main__":
    app.run(debug=True)