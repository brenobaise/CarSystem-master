import Order
import os
from time import sleep

################################
# Database of items and prices #
################################
HEADERS = ["Items", "Price"]
PRODUCTS = {
    "Items": ["0-Stereo System", "1-Leather Interior", "2-Global Positioning System(GPS)",
              "3-Standard - Free of Charge", "4-Modified", "5-Customized Detailing"],
    "Prices": [30.50, 530.99, 301.90, 0, 370.50, 1257.99]  # index 6 is the tax percentage
}

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
    else:       # if the condition doesn't satisfy, check for control flow options
        match var.lower():
            case 'reset' | 'restart':
                reset()
            case 'exit':
                end()
            case 'clear':
                selection.clearBill(order)
                print("[SYSTEM] Order Cleared...")
                return True


# Restarts the system
def reset():
    print("[SYSTEM] Resetting...", end='\n')
    os.system('cls')  # Clear the console not working
    play()


# Exits the system
def end():
    print("[SYSTEM] Exiting ...")
    quit()  # use self keyword to call function inside the class


# Controls whether the user wants to add items to the order.
def additionalItems():
    while True:
        var = selection.getInput("Add an item?:(y/n) ")  # asks for input, returns str.
        if menuControl(var):  # Checks for Control Flow
            continue
        elif var.lower() == 'y':
            itemSelection()
        elif var.lower() == 'n':
            break


# Handles user input in correlation to the menu.
def itemSelection():
    chosen_item = selection.getInput("Choose an Item: ")  # Asks for input, return str
    try:
        if menuControl(chosen_item):  # Checks for Control Flow.
            Order.Input.updateBill(order, PRODUCTS, chosen_item)  # Updates item into the "shopping list" / order.
            selection.returnBill(order, HEADERS)  # Return the order bill in form of a table
        else:
            print("Order Cleared ...")
    except IndexError:
        print("[SYSTEM WARNING] You can only choose from 0 to 5 items")


# Choose items to be added to the bill.
def selectItem():
    if not changePrice():  # Checks if price needs to be changed before user adds items to the order
        # First item selection of the program
        additionalItems()


#########################
# Program Functionality #
#########################


def play():
    print("[SYSTEM] You can type clear, restart or exit anytime in the program.")
    while True:
        selection.clearBill(order)  # Clears the "shopping basket" before starting a new order.
        #
        # First input, Price of the car
        car_input = car_price.getInput("Initial car sale price: ")
        menuControl(car_input)  # Checks for Control Flow.
        checked_price = car_price.checkValidity(car_input, False)  # Check for valid input
        price = checked_price

        if int(price) < 1:  # ONLY allows the program to proceed if price is a number
            continue
        else:
            # Second input
            allowance_input = allowance.getInput("Trade-in allowance: ")
            menuControl(allowance_input)  # Check for Control Flow
            checked_allowance = allowance.checkValidity(allowance_input, True)  # Check for valid input
            trade_in_allowance = checked_allowance

            # After both inputs are checked, proceed with the program.
            # Proceed to menu, select items and calculate order
            print("Basic Car Price Entered: ", int(price),
                  "\nTrade-in Allowance: ", int(trade_in_allowance), end='\n')  # Display inputs
            print("-" * 46)
            promptProducts()  # display database
            selectItem()  # handles user choices
            calculate(price, trade_in_allowance)  # Calculations
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

    sleep(2)

    reset()


# Displays Additional Accessories Table.
def promptProducts():
    # Prints database
    selection.returnBill(PRODUCTS, HEADERS)


# Handles the option to change the prices of the dictionary.
def changePrice():
    while True:
        var = modify_products.getInput("Would you like to change the price of a item?:(y/n) ")
        if menuControl(var):  # checks Control Flow.
            continue
        elif var.lower() == "y":
            try:
                modify_item = modify_products.getInput("Which item would you like to change?:")
                item = int(modify_item)
                print("Selected Item: ", PRODUCTS['Items'][item])
                new_value = modify_products.getInput("What would you like to change the price of the item to?: ")
                print("New value of", PRODUCTS['Items'][item], ": £", new_value)
                # updates the PRODUCTS dictionary with the parsed item to change and its new value.
                modify_products.updateProducts(PRODUCTS, int(modify_item), int(new_value))
                print("[SYSTEM] New prices updated to database... ")

                break
            except IndexError:
                print("[SYSTEM] You can only choose from 0 to 5 items")
        elif var.lower() == 'n':
            break
    return False


# Run the program #
play()
