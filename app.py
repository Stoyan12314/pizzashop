import csv
from math import comb
from datetime import date, datetime
from typing import Counter
from xml.etree.ElementTree import Comment
from flask import Flask, redirect, url_for
import time
from datetime import datetime
from flask import render_template, request, redirect, flash
import flask
from jinja2 import FileSystemLoader
from CustomPymata4 import *
import pandas as pd

board = CustomPymata4(baud_rate = 57600, com_port = "COM3")
RED_LED = 4
GREEN_LED = 5
YELLOW_LED = 7
OFF = 0
ON = 1
YELLOW_INTERVAL = 0.5
yellow_led_state = 0
board.set_pin_mode_digital_output(RED_LED)
board.set_pin_mode_digital_output(GREEN_LED)
board.set_pin_mode_digital_output(YELLOW_LED)


def Order():
       with open('CSV/Customers.csv', 'r', newline='') as file: 
        reader = csv.DictReader(file)
        #header=next(reader)
        for row in reader:
            orders=row['orderID']
            order = orders
        return order

app = Flask(__name__)
df = pd.read_csv("CSV/Customers.csv")
number = 0000000

if df.empty:
 def auto_increment():
     global number
     number += 1
     return str(number)
else:
    checkorder = int(Order())
    number=checkorder
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
        return redirect(url_for('main_page'))
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
        return redirect(url_for('main_page'))
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
    
@app.route("/cook_index", methods =['GET','POST'])
def cook_index():
   
    if request.method=="POST":
        df = pd.read_csv("CSV/Customers.csv")
       
        row = request.form['idRow']
        state =request.form['ChangeState']

        if state == "Checked":
          board.digital_write(5, 1)
          time.sleep(0.3)
          board.digital_write(5, 0)
          time.sleep(0.3)
          board.digital_write(5, 1)
          time.sleep(0.3)
          board.digital_write(5, 0)

        value=int(row)-1
        
        print(row)
        print(state)
        df.at[int(value), 'state']=state
        df.to_csv("CSV/Customers.csv", index=False)
        print(df)
        return redirect(url_for('cook_index', orders=readings_from_file()[0], pizzaTypes=readings_from_file()[1], sizes=readings_from_file()[2], toppings1=readings_from_file()[3], toppings2=readings_from_file()[6], toppings3=readings_from_file()[7], quantities=readings_from_file()[8], comments=readings_from_file()[4],checkboxes=readings_from_file()[5]))
        #return redirect(url_for('cook_index'))
    #return render_template("cookDisplay.html", orders=readings_from_file()[0], pizzaTypes=readings_from_file()[1], sizes=readings_from_file()[2], toppings1=readings_from_file()[3], toppings2=readings_from_file()[6], toppings3=readings_from_file()[7], quantities=readings_from_file()[8], comments=readings_from_file()[4],checkboxes=readings_from_file()[5])
    elif request.method=="GET":
        with open('CSV/Customers.csv', 'r', newline='') as file: 
            reader = csv.DictReader(file)
       
            # If there is an unchecked order, turn on yellow light.
            yellow_led_time = datetime.now()
            state=[]
            for row in reader:
                orders=row['state']
                state.append(orders)
            #for states in state:
                #if states=="Unchecked":
            result = all(element == "Checked" for element in state)
            print(result)
            if result:
                   board.digital_write(YELLOW_LED, OFF)
                   board.digital_write(RED_LED, ON)
                   print("arduino LED off")

                    # current_time = datetime.now()
                    # if (current_time - yellow_led_time).total_seconds() > YELLOW_INTERVAL:
                    #     yellow_led_state = not yellow_led_state
                    #     board.digital_write(YELLOW_LED, yellow_led_state)
                    #     yellow_led_time = current_time
                    #     print("aruino LED On")
            else:
                    board.digital_write(YELLOW_LED, ON)
                    board.digital_write(RED_LED, OFF)
                    print("arduino led on")

                    return render_template("cookDisplay.html", orders=readings_from_file()[0], pizzaTypes=readings_from_file()[1], sizes=readings_from_file()[2], toppings1=readings_from_file()[3], toppings2=readings_from_file()[6], toppings3=readings_from_file()[7], quantities=readings_from_file()[8], comments=readings_from_file()[4],checkboxes=readings_from_file()[5])
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
        return redirect(url_for('main_page'))
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
        return redirect(url_for('main_page'))
    elif request.method=="GET":
        return render_template("mamaMia.html")
        

app.run()

    