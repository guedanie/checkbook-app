import datetime
currentDT = datetime.datetime.now()
import json
import pprint
import numpy as np
import os

###############
## Functions ##
###############

# Function to create a new dictionary in  json file. This creates a first entry if one doesn't currently exist
def create_dict(file_name):
    transaction_history = []
    amount = 0
    category = "first_entry"
    description = "first_entry"
    type_transaction = "n/a"
    date = currentDT.strftime("%Y/%m/%d")
    time = currentDT.strftime("%H:%M:%S")


    
    transaction_history = {
        "amount": amount,
        "category": category,
        "description": description,
        "transaction_type": type_transaction,
        "date": f"first access to checkbook app on {date}",
        "time": time
    }
    
    j = json.dumps(transaction_history)
    with open(file_name, "w") as f:
        f.write(j)

# Function to check if a dictionary with a specific file name already 
# exits. If it doesn't, it creates a new dictionary with an entry dictionary with a value of 0
def check_for_json_file(file_name):
    if os.path.exists(file_name) == False:
        create_dict(file_name)

# def is_it_float(user_input):
#     user_input_float = user_input
#     if user_input_float.replace('.','',1).isdigit() == True:
#         amount = float(user_input_float)
#         return amount
#     else:
#         print("Please enter a valid amount")
#         deposite_with_time()

def check_if_digit(string):
   string.replace('.','',1).replace(',','').isdigit() == True

# Function used to import dictionary from the json file
def grab_dictionary():
    with open("dict.json") as f:
        data = json.load(f)
    return data
    
# Function used to ensure that there is enough value in the checkbook 
# to withdraw funds
def is_there_enough_balance():
     with open("dict.json") as f:
        data = json.load(f)
     total_deposit = [x['amount'] for x in data if x['transaction_type'] == 'deposit']
     total_withdraw = [x['amount'] for x in data if x['transaction_type'] == 'withdraw']      
     total_balance = (sum(total_deposit) - sum(total_withdraw))
     return total_balance

# Function to deposit funds - it works by creating a new dictionary based on user inputs
def deposite_with_time():
    amount = input("How much would you like to deposit: $ ")
    if amount.replace('.','',1).isdigit() == True and int(amount.replace('.','',1)) >= 0:
        amount = float(amount.replace(',',''))
        category = input("What category would you like to give to this transaction: ")
        description = input("Add a small description: ")
        type_transaction = 'deposit'
        date = currentDT.strftime("%Y/%m/%d")
        time = currentDT.strftime("%H:%M:%S")
    
        # the function then opens the existing dictionary stores it in a local 
        # variable - which can then append with the new information. 
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
        # lastly the function makes a data dump back to the json file, completely overwriting the
        # content with the contents inside the local variable
        j = json.dumps(transaction_history)
        with open("dict.json", "w") as f:
            f.write(j)
    else:
        print("Please enter a valid number")
        deposite_with_time()

# Function to withdraw funds. It works just like the deposit function, but with the additional function to check that there are sufficient funds before the 
# transaction takes place. This is done through a loop
def withdraw_with_time():
    amount = input("How much would you like to withdraw: $ ")
    if amount.replace('.','',1).isdigit() == True and int(amount.replace('.','',1)) >= 0:
        amount = float(amount.replace(',',''))
        total_amount = is_there_enough_balance()
        if total_amount > amount:
            category = input("What category would you like to give to this transaction: ")
            description = input("Add a small description: ")
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
        else:
            print(f"Insuficient funds, your current balance is ${total_amount} ")
    else:
        print("Please enter a valid number")
        withdraw_with_time()

# Function used to display the total amount in the checkbook. This function runs a list comprehension and pulls total values from withdraw and deposit 
# dictionaries, then returns a variable with the difference. 
def display_total_amount():
    with open("dict.json") as f:
        data = json.load(f)
    total_deposit = [x['amount'] for x in data if x['transaction_type'] == 'deposit']
    total_withdraw = [x['amount'] for x in data if x['transaction_type'] == 'withdraw']      
    total_balance = (sum(total_deposit) - sum(total_withdraw))
    print(f"Your total balance is ${total_balance}")
    print()

# Function used to pull history transactions. Broad list comprehension with a pprint 
def show_history():
    transaction_history = grab_dictionary()
    pprint.pprint(transaction_history)


# Function used to pull all categories from the json file
def look_up_by_category(category):
    data = grab_dictionary()
    total = 0
    transactions = [x for x in data if x['category'] == category]
    for transaction in transactions:
        total += transaction['amount']
    return total

# Function used to get unique categories based on their transaction type
def get_unique_categories_deposit():
    data = grab_dictionary()
    categories = [x['category'] for x in data if x['transaction_type'] == 'deposit']
    unique_category = []
    for x in categories:
        if x not in unique_category:
            unique_category.append(x)
    return unique_category

def get_unique_categories_withdraw():
    data = grab_dictionary()
    categories = [x['category'] for x in data if x['transaction_type'] == 'withdraw']
    unique_category = []
    for x in categories:
        if x not in unique_category:
            unique_category.append(x)
    return unique_category
    
# Function uses two previous functions to run a list comprehension and return a list with 
# the sum values per categories. It provides two lists, one with all the categories that are categorized as 'withdraw' and 'deposit'
def get_all_categories():
    categories_deposit = get_unique_categories_deposit()
    categories_withdraw = get_unique_categories_withdraw()
    data_category_deposit = [(x, look_up_by_category(x)) for x in categories_deposit]
    data_category_withdraw = [(x, look_up_by_category(x)) for x in categories_withdraw]
    print("Sum of deposits by category")
    print()
    pprint.pprint(data_category_deposit)
    print()
    print("Sum of withdraws by category")
    print()
    pprint.pprint(data_category_withdraw)
    print()



#Function used to pull transactions based on input by user. This looks to match dates
def get_transaction_by_date(date):
    data = grab_dictionary()
    transactions = [x for x in data if date in x['date']]
    if len(transactions) != 0:
        pprint.pprint(transactions)
    else:
        print()
        print(f"No transactions found matching date: '{date}'")


#Function used to pull transactions based on input by user. This looks to match a keyword from the description key
def transactions_by_keyword(keyword):
    data = grab_dictionary()
    transactions = [x for x in data if keyword in x['description']]
    if len(transactions) != 0:
        pprint.pprint(transactions)
    else: 
        print()
        print(f"No transactions found matching the keyword: '{keyword}'")


## Function to let user amend a previous transaction
# Function pulls and prints data with line numbers from the json file
def pull_data_with_id():
    with open("dict.json") as f:
        data = json.load(f)
        data_index = [index for index in enumerate(data)]
        pprint.pprint(data_index)

def pull_data_id():
    with open("dict.json") as f:
        data = json.load(f)
        data_index = [index[0] for index in enumerate(data)]
        return data_index

# Function used to let users select what line they want to select       
def select_line_number():
    print("Please identify the line number matching the transaction you want to update")
    print()
    user_line_choice = input("What line number do you want to update: ")
    data_index = pull_data_id()
    if user_line_choice == 'exit':
        exit_function()
    elif user_line_choice.isdigit() == False:
        print("Please enter a valid number")
        select_line_number()
    elif int(user_line_choice) not in data_index:
        print("Line number not found")
        select_line_number()
        print()
    else:
        return int(user_line_choice)
    

# def line_selected_by_user(user_line_choice):
#        with open("dict.json") as f:
#         data = json.load(f)
#         for index, line in enumerate(data):
#             if str((index + 1)) == user_line_choice:
#                 return line

# Function used to let users update historical transactions. It uses an index to match what the user has input. It then asks the user to input the new values.
def update_data(user_index):
    amount = input("Please enter new value: $ ")
    if amount.replace('.','',1).replace(',','').isdigit() == True and int(amount.replace('.','',1).replace(',','')) >= 0:
        amount = float(amount.replace(',',''))
        category = input("What category would you like to give to this transaction: ")
        description = input("Add a small description: ")
        type_transaction = input("please write if this is a deposit or a withdraw: ")
        date = currentDT.strftime("%Y/%m/%d")
        time = currentDT.strftime("%H:%M:%S")
    
        # Then it pulls the existing dictionary from json file, and then updates the dictionary matching the user index
        with open("dict.json") as f:
            transaction_history = json.load(f)
            transaction_history[user_index].update({
                "amount": amount,
                "category": category,
                "description": description,
                "transaction_type": type_transaction,
                "date": f"updated on {date}", # this entry is different, so that users can see what transactions have been updated, and when they were updated
                "time": time
            })
        
        j = json.dumps(transaction_history)
        with open("dict.json", "w") as f:
            f.write(j)

    else:
        print("Please enter a valid number")
        update_data(user_index)
    
    
# def line_selected_by_user(user_line_choice):
#     data_with_id = pull_data_with_id()
#     transaction = ''
#     if data_with_id[5] == user_line_choice:
#         transaction = data_with_id[6:]
#     print(transaction)

# deposite_with_time()
# withdraw_with_time()

# To whipe the dict.json file:
# def restart_json_dict():
#     with open("dict.json","w") as f:
#         f.write(json.dumps([]))


# def get_transaction_history():
#     with open("dict.json") as json_file:
#         data = json.load(json_file)
#         return data

#############
## user ui ##
#############
# Function used to print the sub menu, under "Additional Transaction Options"
def user_sub_menu_transactions():
    print("What would you like to do?")
    print()
    print("1) View transactional history")
    print("2) View total spent transactions by category")
    print("3) Find transaction by keyword")
    print("4) Find transactions by date")
    print("5) Update previous transactions")
    print("6) Return to main menu")
# Function used to ask user for an input
def user_input_sub_menu():
    user_subchoice = input("Your choice? ")
    return user_subchoice
# Function that takes user input and runs functions based on user choice. This runs the sub-menu options.
def user_sub_choice(user_subchoice):
    user_subchoice.replace(',','').replace(')','').replace('.','')
    if user_subchoice == '1':
        show_history()
    elif user_subchoice == '2':
        get_all_categories()
    elif user_subchoice == '3':
        keyword = input("What keyword would you like to search for: ")
        transactions_by_keyword(keyword)
    elif user_subchoice == '4':
        date = input("Please enter a date (YYYY/MM/DD): ")
        if date.replace('/','',2).isdigit() == True:
            get_transaction_by_date(date)
        else:
            print()
            print("Please enter a valid date")
    elif user_subchoice == '5':
        pull_data_with_id()
        user_subchoice_id = select_line_number()
        update_data(user_subchoice_id)
    elif user_subchoice == '6':
        print("Going back to main menu")
    else: 
        print(f"{user_subchoice} is an invalid choice")
        print()
# Function used to call the initial greeting
def initial_greeting():
    print("~~~ Welcome to your terminal checkbook! ~~~")
# Function used to print the main menu
def user_menu():
    print("What would you like to do?")
    print()
    print("1) view current balance")
    print("2) Record a debit (withdraw)")
    print("3) Record a credit (deposit)")
    print("4) View transactional options")
    print("5) exit")


# Function to take user input for the main menu
def user_input_menu():
    user_choice = input("Your choice? ")
    user_choice.strip().replace(',','').replace(')','').replace('.','')
    return user_choice
# Function that takes user input and runs functions based on user choice from the main menu
def user_choice(user_input):
        user_input.strip().replace(',','').replace(')','').replace('.','')
        if user_input == '1':
            display_total_amount()
        elif user_input == '2':
            withdraw_with_time()
        elif user_input == '3':
            deposite_with_time()
        elif user_input == '4': #This part of the function runs the submenu, which deals with the transaction options (additional features).
            user_subchoice_loop()
        elif user_input == '5':
            print("Have a nice day!")
            print()
        else: 
            print(f"{user_input} is an invalid choice")
            print()

def user_subchoice_loop():
    user_subchoice = '0' # Similar to the main sequence, this uses a while loop that runs until the user input str(6), which returns them to the main menu
    while user_subchoice != '6':
        print()
        user_sub_menu_transactions()
        print()
        user_subchoice = user_input_sub_menu()
        user_sub_choice(user_subchoice)

#Function creted to let users exit the current feature and return to the main menu. Not currently working properly so 
# has been commented out.
def exit_function():
    user_input = '0'
    user_subchoice = '0' 
    while user_subchoice != '6':
        print()
        user_sub_menu_transactions()
        print()
        user_subchoice = user_input_sub_menu()
        user_sub_choice(user_subchoice)
    while user_input != '5':
        print()
        user_menu()
        print()
        user_input = user_input_menu()
        print()
        user_choice(user_input)    

##################
## Running Code ##
##################
# Main code that runs the sequence. Uses a while loop that keeps the functions running until the user inputs str(5). This runs the main menu. The submenu 
# sequence is within the user choice function
check_for_json_file("dict.json")
user_input = '0'
print()
initial_greeting()
print()
while user_input != '5':
    print()
    user_menu()
    print()
    user_input = user_input_menu()
    print()
    user_choice(user_input)

    