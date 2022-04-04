import csv


from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


from math import comb
from typing import Counter
from xml.etree.ElementTree import Comment
from flask import Flask, redirect, url_for
import time
from datetime import datetime
from flask import render_template, request, redirect, flash
from jinja2 import FileSystemLoader
from CustomPymata4 import *
import pandas as pd

number=0000000
app = Flask(__name__)
def auto_increment():
   global number
   number+=1
   return str(number)


@app.route("/")

@app.route("/loginIn_index")
def loginIn_index(): 
   return render_template("login.html")

@app.route("/", methods =['POST'])
def login_check_index():
    
    login = request.form['login']
    password=request.form['password']
    if login=="1" and password=="1":
        return redirect(url_for('main_page'))

    return redirect(url_for('login_check_index'))



@app.route("/main_page")
def main_page():
    return render_template("index.html")

@app.route("/original_index", methods =['GET','POST'])
def original_index():
    if request.method == 'POST':
        comment = request.form['Comment']
        pizzaType="original"
        firstChoice = request.form.get("firstChoice")
        secondChoice= request.form.get("secondChoice")
        thirdChoice=request.form.get("thirdChoice")
        forthChoice=request.form.get("forthChoice")
        quantity= request.form['Quantity']
        unChecked="Unchecked"
        if not comment:
            comment="None"
        combine=[auto_increment(), pizzaType, firstChoice, secondChoice, thirdChoice, forthChoice, quantity, comment, unChecked]
        with open('CSV/Customers.csv','a') as inFile:
            writer = csv.writer(inFile)
            writer.writerow(combine) 
        return render_template("original.html")
    elif request.method=="GET":
        return render_template("original.html")


@app.route("/cheesy_index", methods =['GET','POST'])
def cheesy_index():
    if request.method == 'POST':
        comment = request.form['Comment']
        pizzaType="cheesy"
        unChecked="Unchecked"
        firstChoice = request.form.get("firstChoice")
        secondChoice= request.form.get("secondChoice")
        thirdChoice=request.form.get("thirdChoice")
        forthChoice=request.form.get("forthChoice")
        quantity= request.form['Quantity']
        if not comment:
            comment="None"
        combine=[auto_increment(), pizzaType, firstChoice, secondChoice, thirdChoice, forthChoice, quantity, comment, unChecked]
        with open('CSV/Customers.csv','a') as inFile:
            writer = csv.writer(inFile)
            writer.writerow(combine) 
        return render_template("cheesy.html")
    elif request.method=="GET":
        return render_template("cheesy.html")

def readings_from_file():
    with open('CSV/Customers.csv', 'r', newline='') as file: 
        reader = csv.DictReader(file)
        size=[]
        order=[]
        pizzaType=[]
        topping1=[]
        topping2=[]
        topping3=[]
        quantity=[]
        comment=[]
        state=[]
        #header=next(reader)
        for row in reader:
            orders=row['orderID']
            pizzaTypes=row['pizzaType']
            sizes=row['size']
            toppings1=row['topping1']
            toppings2=row['topping2']
            toppings3=row['topping3']
            quantities=row['quantity']
            comments=row['comment']
            checked=row['state']
            state.append(checked)
            size.append(sizes)
            order.append(orders)
            pizzaType.append(pizzaTypes)
            topping1.append(toppings1)
            topping2.append(toppings2)
            topping3.append(toppings3)
            quantity.append(quantities)
            comment.append(comments)
        return order, pizzaType, size, topping1, comment, state, topping2, topping3, quantity

def on_modified(event):
    flash('New Orders')
    
@app.route("/cook_index", methods =['GET','POST'])
def cook_index():
    #event_handler = FileSystemEventHandler
   # event_handler.on_modified = on_modified
    #observer= Observer()
   # path="CSV/Customers.csv"
    #observer.schedule(event_handler,path ,recursive=True)
   # observer.start()
    if request.method=="POST":
        df = pd.read_csv("CSV/Customers.csv")
       
        row = request.form['idRow']
        state =request.form['ChangeState']
        value=int(row)-1
        
        print(row)
        print(state)
        df.at[int(value), 'state']=state
        df.to_csv("CSV/Customers.csv", index=False)
        print(df)
        render_template("cookDisplay.html", orders=readings_from_file()[0], pizzaTypes=readings_from_file()[1], sizes=readings_from_file()[2], toppings1=readings_from_file()[3], toppings2=readings_from_file()[6], toppings3=readings_from_file()[7], quantities=readings_from_file()[8], comments=readings_from_file()[4],checkboxes=readings_from_file()[5])
        #return redirect(url_for('cook_index'))
    return render_template("cookDisplay.html", orders=readings_from_file()[0], pizzaTypes=readings_from_file()[1], sizes=readings_from_file()[2], toppings1=readings_from_file()[3], toppings2=readings_from_file()[6], toppings3=readings_from_file()[7], quantities=readings_from_file()[8], comments=readings_from_file()[4],checkboxes=readings_from_file()[5])

@app.route("/angus_index", methods =['GET','POST'])
def angus_index():
    if request.method == 'POST':
        comment = request.form['Comment']
        pizzaType="angus"
        unChecked="Unchecked"
        firstChoice = request.form.get("firstChoice")
        secondChoice= request.form.get("secondChoice")
        thirdChoice=request.form.get("thirdChoice")
        forthChoice=request.form.get("forthChoice")
        quantity= request.form['Quantity']
        if not comment:
            comment="None"
        combine=[auto_increment(), pizzaType, firstChoice, secondChoice, thirdChoice, forthChoice, quantity, comment, unChecked]
        with open('CSV/Customers.csv','a') as inFile:
            writer = csv.writer(inFile)
            writer.writerow(combine) 
        return render_template("blackangus.html")
    elif request.method=="GET":
        return render_template("blackangus.html")
        


@app.route("/mama_index", methods =['GET','POST'])
def mama_index():
    if request.method == 'POST':
        comment = request.form['Comment']
        pizzaType="mamaMia"
        unChecked="Unchecked"
        firstChoice = request.form.get("firstChoice")
        secondChoice= request.form.get("secondChoice")
        thirdChoice=request.form.get("thirdChoice")
        forthChoice=request.form.get("forthChoice")
        quantity= request.form['Quantity']
        if not comment:
            comment="None"
        combine=[auto_increment(), pizzaType, firstChoice, secondChoice, thirdChoice, forthChoice, quantity, comment, unChecked]
        with open('CSV/Customers.csv','a') as inFile:
            writer = csv.writer(inFile)
            writer.writerow(combine) 
        return render_template("mamaMia.html")
    elif request.method=="GET":
        return render_template("mamaMia.html")
        



    