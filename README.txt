The following app was design to keep track of a user's transactional histories, if they chose to use it. 

The project specifications were as follows: 

Command Line Checkbook Application

You will be creating a command line checkbook application that allows users to track their finances with a command line interface.

When run, the application should welcome the user, and prompt them for an action to take:

1.view current balance
2. add a debit (withdrawal)
3. add a credit (deposit)
4. exit

The application should persist between times that it is run, that is, if you run the application, add some credits, 
exit the application and run it again, you should still see the balance that you previously created. In order to do this, 
your application will need to store it's data in a text file. Consider creating a file where each line in the file represents a single transaction.

Additional Features that were requested: 

1. add a menu item that allows the user to view all historical transactions
assign categories to each transaction
2. add a menu item to allow the user to view all the transactions in a given category
    *provide the user with summary statistics about the transactions in each category
    *keep track of the date and time that each transaction happened
3. allow the user to view all the transactions for a given day
    *make sure your list of previous transactions includes the timestamp for each
4. allow the user to optionally provide a description for each transaction
    *allow the user to search for keywords in the transaction descriptions, and show all the transactions that match the user's search term
5. allow the user to modify past transactions

For this project - all base function, and additional features were created. 

Further work: 
Although the app works as specify, there are some additional functions that I would have liked to be able to add if I had more time:
1. Exit function: The exit for a user to type exit in any input option. This would return the user to the main menu. The function was successfully built, but I was unable to work on
    finding the right position within the loop statements to successfully break the loop, if the user chose to do it. 
2. Formatting: While several of the outputs have been printed with pprints, it would have been ideal to create further formating outputs to 
    ensure that the app is easier to navigate and comprehend
