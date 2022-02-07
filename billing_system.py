import sqlite3
from prettytable import PrettyTable
from tkinter import *
from mako.template import Template
import time

import smtplib
from email.mime.multipart import MIMEMultipart

from email.mime.text import MIMEText
from email.mime.image import MIMEImage

root = Tk()

root.title("Welcome To Our Market")
root.geometry("700x700")

#create a database

db = sqlite3.connect("DB.sqlite")
cursor = db.cursor()

#create a table
'''
try:
    cursor.execute("""CREATE TABLE inventory
                (Code integer,
                Name text,
                Rs_kg integer,
                Quantity integer)
                """)

except:
    pass

list1 = [101, "Apple", 120, 30]
list2 = [102, "Banana", 30, 30]
list3 = [103, "Grapes", 50, 30]
list4 = [104, "Melon", 40, 30]
list5 = [105, "Mango", 80, 30]
list6 = [106, "Orange", 60, 30]



cursor.execute("Insert into inventory values(?,?,?,?)", list1)
cursor.execute("Insert into inventory values(?,?,?,?)", list2)
cursor.execute("Insert into inventory values(?,?,?,?)", list3)
cursor.execute("Insert into inventory values(?,?,?,?)", list4)
cursor.execute("Insert into inventory values(?,?,?,?)", list5)
cursor.execute("Insert into inventory values(?,?,?,?)", list6)
'''

##cursor.execute("select * from inventory")
##print(cursor.fetchall())

# Create submit function
cart = {}

labelList = []

def submit():
    billList = []
    c = variable.get()
    c = int(c)
    b = enterQty.get()
    b = int(b)
    
    cartEntry = [c, listLabel[c][1], b, listLabel[c][2]*b]
    cart[c] = cartEntry

    print(cart)

    # delete existing qty
    enterQty.delete(0, END)
    #w.delete(0, END)
    for ele in cart.values():
        rec = str(ele[0]) + "    " + ele[1] + "    " + str(ele[2]) + "       " + str(ele[3]) + "\n"
    #print(rec)
    
    headerLabel = Label(root, text = "Code  Fruit   Qty  Amt", font="times 14")
    headerLabel.place(x = 60, y = 230)
    
    printCart(cart)


def printCart(cart):

    initY = 240
    
    for key, ele in cart.items():
        rec = str(ele[0]) + "    " + ele[1] + "    " + str(ele[2]) + "       " + str(ele[3]) + "\n"
        showLabel = Label(root, text = rec, font="times 12")
        initY += 30
        showLabel.place(x = 60, y = initY)
        labelList.append(showLabel)
        del_btn = Button(root, text = "Delete Item", command=lambda key=key: deleteItem(key))
        del_btn.place(x = 280, y = initY)
        labelList.append(del_btn)
        
    totaltext = "Total:" ,  calculateTotal(cart)
    
    totalLabel = Label(root, text = totaltext, font="times 14")
    totalLabel.place(x = 300, y = 450)   



def deleteItem(removeEle):
    print(removeEle)
    del cart[removeEle]
    
##    for i in range(len(cart)):
##        if cart[i][0] == removeEle:
##            cart.pop(i)
##            break
    print(cart)
    
    for each in labelList:
        each.after(1000, each.destroy())
    
    printCart(cart)

    totaltext = "Total:" ,  calculateTotal(cart)
    
    totalLabel = Label(root, text = totaltext, font="times 14")
    totalLabel.place(x = 300, y = 450) 
      
def calculateTotal(cart):
    totalPrice = 0
    for each in cart.values():
        totalPrice += each[3]
    return totalPrice
    

def updateDatabase():
    db = sqlite3.connect("DB.sqlite")
    cursor = db.cursor()
    
    for key, value in cart.items():
        cursor.execute("select * from inventory where Code=?",[key])
        list1=cursor.fetchall()
        print(list1)
        list2=[list1[0][3]-value[2],key]
        print(list2)
        cursor.execute("update inventory set Quantity=? where Code=?",list2)


    cursor.execute("select * from inventory")
    list3=cursor.fetchall()
    printMenu(list3)
    print(list3)
    
    db.commit()

    db.close()
   
#Global variable for variable in funtion
enterMail = Entry(root, width = 25)

def clearCart():
    cart.clear()
    for each in labelList:
        each.after(1000, each.destroy())
        
    totaltext = "Total: 000" 
    
    totalLabel = Label(root, text = totaltext, font="times 14")
    totalLabel.place(x = 300, y = 450) 
    print(cart)

def billMail():
    #print("hello")

    updateDatabase()
    
    mailLabel = Label(root, text = "Enter Mail ID", font="times 14")
    mailLabel.place(x = 70, y = 550)

    enterMail.place(x = 200, y = 550)

    #time.sleep(5)
    sendmail_btn = Button(root, text = "Send Mail", command = billFinal)
    sendmail_btn.place(x = 150, y = 600)
    
def billFinal():

    message = MIMEMultipart()
    
    message["Subject"] = "Fruit Super Market"
    message["From"] = "Vendor fruit"

    username = input("Enter your mailid:")
    password = input("Enter your password:")

    sender = username
    receiver = enterMail.get()
    
    body = createMailBody(cart)
    txt = MIMEText(body,'html') # string -> plain
    message.attach(txt)


    # to send an email

    server = smtplib.SMTP("smtp.gmail.com","587")
    server.starttls()
    print("Connected")


    server.login(username,password)
    print("Login Successfull")

     
    server.sendmail(sender,receiver,message.as_string())
    print("Mail Sent Successfully")

    mailLabel = Label(root, text = "Thank you for shopping!! Visit Again", font="times 14")
    mailLabel.place(x = 70, y = 650)
    
def createMailBody(cart):

    mytemplate = Template(filename='template.txt')
    bodyTemp = mytemplate.render(cart=cart, total=calculateTotal(cart))
    print(bodyTemp)
    print(type(bodyTemp))
    return bodyTemp

def printMenu(listQty):
    
    headerLabel = Label(root, text = "Code  Fruit  Rs/Kg  Rem_Qty", font="times 16")
    headerLabel.place(x = 450, y = 140)
    
    initialYPos = 140
    for l in listQty:
        textlabel = (str(l[0])+ "   " + l[1] + "    " + str(l[2]) + "       " + str(l[3]))    
        newLabel = Label(root, text=textlabel, font="times 14")
        initialYPos += 30
        newLabel.place(x=450, y=initialYPos)
        listLabel[l[0]] = l

# main title
label8 = Label(root, text="Billing System",
               font="times 28 bold")
label8.place(x=350, y=20, anchor="center")
 
# Menu Card
label1 = Label(root, text="Menu",
               font="times 28 bold")
label1.place(x=520, y=70)

cursor.execute("select * from inventory where Quantity > ?", [0])
listQty = cursor.fetchall()
print(listQty)

listLabel = {}

listCode = []
for c in listQty:
    listCode.append(c[0])
print(listCode)

## organize menu
printMenu(listQty)


print(listLabel)
labelFruit = Label(root, text="Select fruit code",font="times 28 bold")
labelFruit.place(x=10, y=70)

# Selct code btton

variable = StringVar(root)
variable.set("Select Fruit Code") # default value
options = []
w = OptionMenu(root, variable, *listCode)
##w.pack()
w.place(x = 95, y = 120)



qtyLabel = Label(root, text = "Enter Quantity", font="times 12")
qtyLabel.place(x = 0, y = 160)

enterQty = Entry(root, width = 15)
enterQty.place(x = 95, y = 160)


sub_btn = Button(root, text = "Add Item", command = submit)
sub_btn.place(x = 95, y = 200)

bill_btn = Button(root, text = "Print Bill", command = billMail)
bill_btn.place(x = 95, y = 500)

bill_btn = Button(root, text = "Clear Cart", command = clearCart)

bill_btn.place(x = 200, y = 500)

db.commit()

db.close()

root.mainloop()
