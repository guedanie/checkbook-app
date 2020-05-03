import tkinter
import pandas as pd
import datetime
currentDT = datetime.datetime.now()
import json
import pprint
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter.font as tkFont


def get_current_balance():
    data = grab_dictionary()
    df = pd.DataFrame(data)
    current_balance = df[df.transaction_type == "deposit"].amount.sum() - df[df.transaction_type == "withdraw"].amount.sum()
    return current_balance

# Function used to import dictionary from the json file
def grab_dictionary():
    with open("dict.json") as f:
        data = json.load(f)
    return data

def create_new_withdraw_window():
    
    fontStyle = tkFont.Font(family="Lucida Grande", size=20)
    newWindow = tkinter.Toplevel(window)
    newWindow.columnconfigure([0,6], minsize=100)
    newWindow.rowconfigure([0, 6], minsize=100)
    withdraw = tkinter.Entry(newWindow)
    withdraw_description = tkinter.Entry(newWindow)
    withdraw_category = tkinter.Entry(newWindow)

    def close_window():
        newWindow.destroy()

    def myClick_withdraw():
        global current_balance

        amount = withdraw.get()
        category = withdraw_category.get()
        description = withdraw_description.get()
        if amount.replace(".","",1).isdigit():
            amount = float(amount.replace(',',''))
            if current_balance > amount:
            
                category = category
                description = description
                type_transaction = 'withdraw'
                date = currentDT.strftime("%Y/%m/%d")
                time = currentDT.strftime("%H:%M:%S")
        

                with open("dict.json") as f:
                    transaction_history = json.load(f)
                    transaction_history.append({
                        "amount": amount,
                        "category": category,
                        "description": description,
                        "transaction_type": type_transaction,
                        "date": date,
                        "time": time
                    })
                
                j = json.dumps(transaction_history)
                with open("dict.json", "w") as f:
                    f.write(j)
                
                close_window()
            else:
                tkinter.Label(newWindow, text=f"Insuficient funds, your current balance is ${current_balance}").grid(row=6, column = 3)
           
        else:
            tkinter.Label(newWindow, text="Please enter a valid number").grid(row=6, column = 3)


    def changeText():
        global text
        current_balance = get_current_balance()
        text.set(f'Your new balance is ${current_balance:,.2f}')
    
    tkinter.Label(newWindow, text = "Withdraw", font=fontStyle).grid(row=0, column = 3, columnspan=3)
    
    tkinter.Label(newWindow, text = "How much would you like to Withdraw?").grid(row=1, column = 2)
    withdraw.grid(row=1, column=3)
    tkinter.Label(newWindow, text = "Category (Optional)").grid(row=2, column=2)
    withdraw_category.grid(row=2, column= 3)
    tkinter.Label(newWindow, text = "Description (Optional)").grid(row=3, column = 2)
    withdraw_description.grid(row=3, column = 3)
    tkinter.Button(newWindow, text="Withdraw", command= lambda: [myClick_withdraw(), changeText()]).grid(row=5, column=3)
    tkinter.Button(newWindow, text="Cancel", command= close_window, bg="red").grid(row=5, column=2)

def create_new_deposit_window():
    
    fontStyle = tkFont.Font(family="Lucida Grande", size=20)
    newWindow = tkinter.Toplevel(window)
    # newWindow.geometry('500x250')
    newWindow.columnconfigure([0,6], minsize=100)
    newWindow.rowconfigure([0, 6], minsize=100)
    deposit = tkinter.Entry(newWindow)
    deposit_description = tkinter.Entry(newWindow)
    deposit_category = tkinter.Entry(newWindow)

    def close_window():
        newWindow.destroy()

    def myClick_deposit():
        global current_balance

        amount = deposit.get()
        category = deposit_category.get()
        description = deposit_description.get()
        if amount.replace(".","",1).isdigit():
            amount = float(amount.replace(',',''))
         
        
            category = category
            description = description
            type_transaction = 'deposit'
            date = currentDT.strftime("%Y/%m/%d")
            time = currentDT.strftime("%H:%M:%S")
    

            with open("dict.json") as f:
                transaction_history = json.load(f)
                transaction_history.append({
                    "amount": amount,
                    "category": category,
                    "description": description,
                    "transaction_type": type_transaction,
                    "date": date,
                    "time": time
                })
            
            j = json.dumps(transaction_history)
            with open("dict.json", "w") as f:
                f.write(j)
            
            close_window()
            
           
        else:
            tkinter.Label(newWindow, text="Please enter a valid number").grid(row=6, column = 3)


    def changeText():
        global text
        current_balance = get_current_balance()
        text.set(f'Your new balance is ${current_balance:,.2f}')
    
    tkinter.Label(newWindow, text = "Depost", font=fontStyle).grid(row=0, column = 3, columnspan=3)
    
    tkinter.Label(newWindow, text = "How much would you like to Deposit?").grid(row=1, column = 2)
    deposit.grid(row=1, column=3)
    tkinter.Label(newWindow, text = "Category (Optional)").grid(row=2, column = 2)
    deposit_category.grid(row=2, column = 3)
    tkinter.Label(newWindow, text = "Description (Optional)").grid(row=3, column = 2)
    deposit_description.grid(row = 3, column = 3)
    tkinter.Button(newWindow, text="Deposit", command= lambda: [myClick_deposit(), changeText()]).grid(row=5, column= 3)
    tkinter.Button(newWindow, text="Cancel", command= close_window).grid(row=5, column = 2)


def create_new_spending_window():

    newWindow = tkinter.Toplevel(window)
    # newWindow.geometry('800x750')

    def create_plot():
        data = grab_dictionary()

        df = pd.DataFrame(data)
        df_withdraw = df[df.transaction_type == "withdraw"]
        
        # Set up the matplotlib figure
        f, ax = plt.subplots(figsize=(5, 3))

        sns.barplot(data=df_withdraw, x="category", y="amount", ci=None)
        plt.title("Spend by Category")
        plt.xticks(rotation=45, ha="right")

        return f

    def create_plot_time():
        data = grab_dictionary()

        df = pd.DataFrame(data)
        df_withdraw = df[df.transaction_type == "withdraw"]
        
        # Set up the matplotlib figure
        f, ax = plt.subplots(figsize=(5, 3))

        sns.barplot(data=df_withdraw, x="date", y="amount", ci=None)
        plt.title("Spend Over Time")
        plt.xticks(rotation=45, ha="right")

        return f

    fig_1 = create_plot()
    fig_2 = create_plot_time()

    canvas_1 = FigureCanvasTkAgg(fig_1, master=newWindow)  # A tk.DrawingArea.
    canvas_1.draw()
    canvas_1.get_tk_widget().pack()
    canvas_2 = FigureCanvasTkAgg(fig_2, master=newWindow)  # A tk.DrawingArea.
    canvas_2.draw()
    canvas_2.get_tk_widget().pack()

    tkinter.Button(newWindow, text="Return to Menu", command=newWindow.destroy).pack()

def close_window():
    window.destroy()

window = tkinter.Tk()
# window.geometry('500x150')
window.columnconfigure([0,6], minsize=100)
window.rowconfigure([0, 6], minsize=100)
window.title("Personal Banking App")

current_balance = get_current_balance()

text = tkinter.StringVar()
text.set(f'Your current balance is: ${current_balance:,.2f}')

fontStyle = tkFont.Font(family="Lucida Grande", size=18)
tkinter.Label(window, text = "~~ Welcome to your personal banking app ~~", font=fontStyle).grid(row = 0, column = 2, columnspan=4)

tkinter.Label(window, textvariable = text).grid(row= 1, column = 2, columnspan=3)

tkinter.Label(window, text = "Please select one of the options below to proceed").grid(row= 2, column = 2, columnspan=3)


tkinter.Button(window, bg="red", text = "Exit", command = close_window).grid(row=3, column= 1, sticky="w")
tkinter.Button(window, text = "Withdraw", command = create_new_withdraw_window).grid(row=3, column = 2, sticky="e")
tkinter.Button(window, text = "Deposit", command = create_new_deposit_window).grid(row=3, column = 3)
tkinter.Button(window, text = "Spending", command = create_new_spending_window).grid(row= 3, column = 4, sticky="w")

tkinter.mainloop()

