import csv
from datetime import date, datetime
from unittest import skip
from flask import Flask, redirect, url_for, render_template, request
import time
from CustomPymata4 import *
import pandas as pd

board = CustomPymata4(baud_rate = 57600, com_port = "COM5")
RED_LED = 4
GREEN_LED = 5
YELLOW_LED = 7
OFF = 0
ON = 1
BUZZER = 3
yellow_led_state = 0
board.set_pin_mode_digital_output(RED_LED)
board.set_pin_mode_digital_output(GREEN_LED)
board.set_pin_mode_digital_output(YELLOW_LED)
board.set_pin_mode_digital_output(BUZZER)
number=0
app = Flask(__name__)
#functions
order=[]
with open('CSV/Customers.csv', 'r', newline='') as file: 
        reader = csv.DictReader(file)
        for row in reader:
            orders=row['orderID']
            order.append(orders)
        if (number):
            number=int(order[-1])
        if not number:
            number=0

def delete_checked_orders():
    df = pd.read_csv("CSV/Customers.csv")
    df.reset_index()
    listOfIdsWithValueChecked=df.index[df['state'] == "Checked"].tolist()
    for value in listOfIdsWithValueChecked:
        df.drop([value], axis=0, inplace=True)
    df["orderID"] = df["orderID"].astype(int)
    df["quantity"] = df["quantity"].astype(int)
    df.to_csv("CSV/Customers.csv", index=False)
        
def auto_increment():
    global number
    df = pd.read_csv("CSV/Customers.csv")
    if df.empty:
        number=0
    number += 1
    return str(number)

def values_from_forms(pizzaName):
        pizzaType=pizzaName
        unChecked="Unchecked"
        comment = request.form['Comment']
        firstChoice = request.form["firstChoice"]
        secondChoice= request.form["secondChoice"]
        thirdChoice=request.form["thirdChoice"]
        forthChoice=request.form["forthChoice"]
        quantity= request.form['Quantity']
        if not comment:
            comment="None"
        combine=[auto_increment(), pizzaType, firstChoice, secondChoice, thirdChoice, forthChoice, quantity, comment, unChecked]
        return combine


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
        for row in reader:
            orders=row['orderID']
            pizzaTypes=row['pizzaType']
            sizes=row['size']
            toppings1=row['topping1']
            toppings2=row['topping2']
            toppings3=row['topping3']
            quantities=row['quantity']
            comments=row['comment']
            states=row['state']
            state.append(states)
            size.append(sizes)
            order.append(orders)
            pizzaType.append(pizzaTypes)
            topping1.append(toppings1)
            topping2.append(toppings2)
            topping3.append(toppings3)
            quantity.append(quantities)
            comment.append(comments)
        return order, pizzaType, size, topping1, comment, state, topping2, topping3, quantity

#Main code
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
        with open('CSV/Customers.csv','a') as inFile:
            writer = csv.writer(inFile)
            writer.writerow(values_from_forms("original")) 
        board.digital_write(YELLOW_LED, ON)
        return redirect(url_for('main_page'))
    elif request.method=="GET":
        return render_template("original.html")


@app.route("/cheesy_index", methods =['GET','POST'])
def cheesy_index():
    if request.method == 'POST':
        with open('CSV/Customers.csv','a') as inFile:
            writer = csv.writer(inFile)
            writer.writerow(values_from_forms("cheesy")) 
        board.digital_write(YELLOW_LED, ON)
        return redirect(url_for('main_page'))
    elif request.method=="GET":
        return render_template("cheesy.html")
           

@app.route("/angus_index", methods =['GET','POST'])
def angus_index():
    if request.method == 'POST':
        with open('CSV/Customers.csv','a') as inFile:
            writer = csv.writer(inFile)
            writer.writerow(values_from_forms("angus")) 
        board.digital_write(YELLOW_LED, ON)
        return redirect(url_for('main_page'))
    elif request.method=="GET":
        return render_template("blackangus.html")
        


@app.route("/mama_index", methods =['GET','POST'])
def mama_index():
    if request.method == 'POST':
        with open('CSV/Customers.csv','a') as inFile:
            writer = csv.writer(inFile)
            writer.writerow(values_from_forms("mamaMia"))
        board.digital_write(YELLOW_LED, ON)
        return redirect(url_for('main_page'))
    elif request.method=="GET":
        return render_template("mamaMia.html")
        


    

@app.route("/cook_index", methods =['GET','POST'])
def cook_index():
    listOfOrder=[]
    with open('CSV/Customers.csv', 'r', newline='') as file: 
        reader = csv.DictReader(file)
        for row in reader:
            ordersFromRow=row['orderID']
            listOfOrder.append(ordersFromRow)
    if request.method=="POST":
        df = pd.read_csv("CSV/Customers.csv") #IMPORTANT dont remove this because thid df because it will make the checking unusable after reopenning
        row = request.form['idRow']
        state =request.form['ChangeState']
        if state == "Checked":
          board.digital_write(GREEN_LED, ON)
          board.digital_write(BUZZER, ON)
          time.sleep(0.1)
          board.digital_write(BUZZER, OFF)
          board.digital_write(GREEN_LED, OFF)
          time.sleep(0.1)
          board.digital_write(GREEN_LED, ON)
          time.sleep(0.1)
          board.digital_write(GREEN_LED, OFF)
          board.displayShow(row)
          time.sleep(0.1)
          board.displayShow("0000")
        if (row):
            value=int(row)-1
        else:
            value=900000000000
        if (listOfOrder):
            if int(listOfOrder[-1])>=int(value) and int(value)>=0:
                df.at[int(value), 'state']=state
                df.to_csv("CSV/Customers.csv", index=False)
        return redirect(url_for('cook_index', orders=readings_from_file()[0], pizzaTypes=readings_from_file()[1], sizes=readings_from_file()[2], toppings1=readings_from_file()[3], toppings2=readings_from_file()[6], toppings3=readings_from_file()[7], quantities=readings_from_file()[8], comments=readings_from_file()[4],checkboxes=readings_from_file()[5]))
    elif request.method=="GET":
        delete_checked_orders()
        with open('CSV/Customers.csv', 'r', newline='') as file: 
            reader = csv.DictReader(file)
            state=[]
            for row in reader:
                orders=row['state']
                state.append(orders)
            result = all(element == "Checked" for element in state)
            print(result)
            if result:
                    board.digital_write(YELLOW_LED, OFF)
                    board.digital_write(RED_LED, ON)  
            else:
                    board.digital_write(YELLOW_LED, ON)
                    board.digital_write(RED_LED, OFF)
                    return render_template("cookDisplay.html", orders=readings_from_file()[0], pizzaTypes=readings_from_file()[1], sizes=readings_from_file()[2], toppings1=readings_from_file()[3], toppings2=readings_from_file()[6], toppings3=readings_from_file()[7], quantities=readings_from_file()[8], comments=readings_from_file()[4],checkboxes=readings_from_file()[5])
        return render_template("cookDisplay.html", orders=readings_from_file()[0], pizzaTypes=readings_from_file()[1], sizes=readings_from_file()[2], toppings1=readings_from_file()[3], toppings2=readings_from_file()[6], toppings3=readings_from_file()[7], quantities=readings_from_file()[8], comments=readings_from_file()[4],checkboxes=readings_from_file()[5])






app.run()

    