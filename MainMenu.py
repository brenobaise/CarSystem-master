# CarSystem
# Author: Joao Breno Baise
# Final update: 20/05/2022
from tabulate import tabulate

import Order
import os
from time import sleep


################################
# Database of items and prices #
################################
def main():
    HEADERS = ["Items", "Price"]
    PRODUCTS = {
        "Items": ["0-Stereo System", "1-Leather Interior", "2-Global Positioning System(GPS)"],
        "Prices": [30.50, 530.99, 301.90]  # index 6 is the tax percentage
    }

    detailing = {"Items": ["0-Standard - Free of Charge", "1-Modified", "2-Customized Detailing"],
                 "Prices": [0, 370.50, 1257.99]}

    order = {"Items": [],
             "Prices": []}

    # Initialize objects
    car_price = Order.Input()
    allowance = Order.Input()
    selection = Order.Input()
    modify_products = Order.Input()

    ##############################
    #  Program Control Functions #
    ##############################

    # Control Flow
    def menuControl(var):
        if var.isnumeric():  # Checking if it's a valid input
            return True
        elif var:
            match var.lower():  # if the condition doesn't satisfy, check for control flow options
                case 'reset' | 'restart':
                    reset()  # F
                case 'exit':
                    end()  # F
                case 'clear':
                    selection.clearBill(order)
                    print("[SYSTEM] Order Cleared...")
                    return True
        else:
            return False

    # Restarts the system
    def reset():
        print("[SYSTEM] Resetting...", end='\n')
        os.system('cls')  # Clear the console not working
        main()  # F

    # Exits the system
    def end():
        print("[SYSTEM] Exiting ...")
        quit()  # F  # use self keyword to call function inside the class

    # Controls whether the user wants to add items to the order.
    def additionalItems():
        while True:
            var = selection.getInput("Add an item?:(y/n) ")  # asks for input, returns str.
            menuControl(var)  # F  # Checks for Control Flow
            if var.lower() == 'y':
                itemSelection()  # F
            elif var.lower() == 'n':
                break

    # Handles user input in correlation to the menu.
    def itemSelection():
        chosen_item = selection.getInput("Choose an Item: ")  # Asks for input, return str
        try:  # First try check for out of range index
            try:  # Second try checks for any wrong input
                if menuControl(chosen_item):  # F # Checks for Control Flow.

                    Order.Input.updateBill(order, PRODUCTS,
                                           chosen_item)  # Updates item into the "shopping list" / order.
                    selection.returnBill(order, HEADERS)  # Return the order bill in form of a table
            except ValueError:
                pass
        except IndexError:
            print("[SYSTEM WARNING] You can only choose from 0 to 2 items")

    # Choose items to be added to the bill.
    def selectItem():
        promptProducts(detailing)  # F # Display Detailing Menu
        while True:
            chosen_item = selection.getInput("Choose your Detailing: ")  # Asks for input, return str
            try:
                try:
                    menuControl(chosen_item)  # F
                    Order.Input.updateBill(order, detailing, chosen_item)  # Updates item into the "shopping list"
                    print("Your chosen detailing: ", detailing["Items"][int(chosen_item)])  # Display selected item
                    break
                except ValueError:
                    pass
            except IndexError:
                print("[SYSTEM WARNING] You can only choose from 0 to 2 items")

        promptProducts()  # F # Print PRODUCTS DATABASE
        if not changePrice():  # F  # Checks if price needs to be changed before user adds items to the order
            # First item selection of the program
            additionalItems()  # F

    #########################
    # Program Functionality #
    #########################

    def play():
        print("[SYSTEM] You can type clear, restart or exit anytime in the program.")
        while True:
            # First input, Price of the car
            car_input = car_price.getInput("Initial car sale price: ")
            menuControl(car_input)  # F # Checks for Control Flow.
            checked_price = car_price.checkValidity(car_input, False)  # Check for valid input
            price = checked_price

            if int(price) < 1:  # ONLY allows the program to proceed if price is a number
                continue
            else:
                # Second input
                allowance_input = allowance.getInput("Trade-in allowance: ")
                menuControl(allowance_input)  # F # Check for Control Flow
                checked_allowance = allowance.checkValidity(allowance_input, True)  # Check for valid input
                trade_in_allowance = checked_allowance

                # After both inputs are checked, proceed with the program.
                # Proceed to menu, select items and calculate order
                print("Basic Car Price Entered: ", int(price),
                      "\nTrade-in Allowance: ", int(trade_in_allowance), end='\n')  # Display inputs
                print("-" * 46)
                selectItem()  # F # handles user choices
                calculate(price, trade_in_allowance)  # F  # Calculations

                break

    # Handles all calculations within the system
    def calculate(price, trade_in_allowance):
        # Calculates the subtotal of inputs and the order/"shopping basket"
        # formula of % : is amount divided by 100 multiplied by percentage

        # Sum of all the items in order, plus the car price
        # order dictionary has to be converted into a list because of sum().
        lst = list(order['Prices'])
        subtotal = sum(lst) + int(price)
        print("Subtotal: ", "£{:,.2f}".format(subtotal))

        # Calculate the sales tax based on the subtotal
        sales_tax = (subtotal / 100) * 6
        print("Sales Tax: ", "£{:,.2f}".format(sales_tax))

        # Calculate the overall price after allowance.
        amount_due = subtotal - int(trade_in_allowance)
        print("Amount Due : ", "£{:,.2f}".format(amount_due))

        while True:
            var = selection.getInput("Would you like to print? :(y/n) ")  # asks for input, returns str.
            menuControl(var)  # F  # Checks for Control Flow
            if var.lower() == 'y':
                with open("TestFile.txt", "w") as f:
                    f.write("Here is your receipt\n")
                    f.write(tabulate(order, HEADERS, tablefmt="pipe"))
                    f.write("\n" + "Thank you for shopping with us! \n")
                    f.write('Subtotal: {} \n'.format("£{:,.2f}".format(subtotal)))
                    f.write('Sales Tax: {} \n'.format("£{:,.2f}".format(sales_tax)))
                    f.write("Amount Due: {} \n".format("£{:,.2f}".format(amount_due)))

                os.startfile("TestFile.txt",
                             "print")
            elif var.lower() == 'n':
                break

        sleep(2)  # F
        # Program Ends
        reset()  # F

    # Displays Additional Accessories Table.
    def promptProducts(*args):
        # Prints database
        if args:
            selection.returnBill(detailing, HEADERS, menu=True)  # if menu = True return exterior finish
        else:
            selection.returnBill(PRODUCTS, HEADERS)  # if menu not specified return accessories

    # Handles the option to change the prices of the dictionary.
    def changePrice():
        while True:
            var = modify_products.getInput("Would you like to change the price of a item?:(y/n) ")
            menuControl(var)  # F # checks Control Flow.
            if var.lower() == "y":
                try:
                    modify_item = modify_products.getInput("Which item would you like to change?:")
                    menuControl(modify_item)  # F # checks Control Flow.

                    item = int(modify_item)
                    print("Selected Item: ", PRODUCTS['Items'][item])
                    new_value = modify_products.getInput("What would you like to change the price of the item to?: ")
                    menuControl(new_value)  # F  # checks Control Flow.
                    print("New value of", PRODUCTS['Items'][item], ": £", new_value)
                    # updates the PRODUCTS dictionary with the parsed item to change and its new value.
                    modify_products.updateProducts(PRODUCTS, int(modify_item), int(new_value))
                    print("[SYSTEM] New prices updated to database... ")

                    break
                except ValueError:
                    print("[SYSTEM] Invalid Input")
                except IndexError:
                    print("[SYSTEM] You can only choose from 0 to 2 items")
            elif var.lower() == 'n':
                break

        return False

    play()


# Run the program #
if __name__ == "__main__":
    main()  # F
