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
    "Prices": [30.50, 530.99, 301.90, 0, 370.50, 1257.99, 6]  # index 6 is the tax percentage
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


def menuControl(chosen_item):
    if chosen_item.isnumeric():
        return True
    else:
        match chosen_item.lower():
            case 'reset' | 'restart':
                reset()
            case 'exit':
                end()
            case 'clear':
                selection.clearBill(order)
                print("Order Cleared...")
                return True


# Restarts the system
def reset():
    print("Resetting System ...", end='\n')
    os.system('cls')  # Clear the console not working
    play()


# Exits the system
def end():
    print("Exiting ...")
    quit()  # use self keyword to call function inside the class


# Controls whether the user wants to add items to the order.
def additionalItems():
    while True:
        var = selection.getInput("Add an item?:(y/n) ")  # asks for input, returns str.
        if menuControl(var):
            continue
        elif var.lower() == 'y':
            itemSelection()
        elif var.lower() == 'n':
            break


# Handles user input in correlation to the menu.
def itemSelection():
    chosen_item = selection.getInput("Choose an Item: ")  # Asks for input, return str
    if menuControl(chosen_item):
        Order.Input.updateBill(order, PRODUCTS, chosen_item)  # Updates the selected item into the shopping list(order)
        selection.returnBill(order, HEADERS)  # Return the order bill in form of a table
    else:
        print("Order Cleared ...")


# Choose items to be added to the bill.
def selectItem():
    if not changePrice():  # Checks if price needs to be changed before user adds items to the order
        # First item selection of the program
        additionalItems()


#########################
# Program Functionality #
#########################


def play():
    print("You can type clear, restart or exit anytime in the program.")
    while True:
        selection.clearBill(order)
        # First input, Price of the car
        price = car_price.checkValidity(car_price.getInput("Initial car sale price: "), False)

        if int(price) < 1:  # ONLY allows the program to proceed if price is a number
            continue
        else:
            # Second input, allowance if any
            trade_in_allowance = allowance.checkValidity(allowance.getInput("Trade-in allowance: "), True)

            # Proceed to menu, select items and calculate order
            print("Basic Car Price Entered:", int(price), int(trade_in_allowance), end='\n')
            print("-" * 46)
            promptProducts()
            selectItem()
            calculate(price, trade_in_allowance)
            break


# Handles all calculations within the system
def calculate(price, trade_in_allowance):
    # calculates the subtotal of inputs and the order+
    # formula is amount divided by 100 multiplied by percentage

    # Sum of all the items in order, plus the car price
    lst = list(order['Prices'])
    subtotal = sum(lst) + int(price)
    print("Subtotal: ", "£{:,.2f}".format(subtotal))

    # Calculate the sales tax based on the subtotal
    sales_tax = (subtotal / 100) * int(PRODUCTS['Prices'][-1])
    print("Sales Tax: ", "£{:,.2f}".format(sales_tax))

    # Calculate the overall price after allowance.
    amount_due = subtotal - int(trade_in_allowance)
    print("Amount Due : ", "£{:,.2f}".format(amount_due))

    sleep(2)

    reset()


# Displays Additional Accessories Table.
def promptProducts():
    selection.returnBill(PRODUCTS, HEADERS)


# Handles the option to change the prices of the dictionary.
def changePrice():
    while True:
        var = modify_products.getInput("Would you like to change the price of a item?:(y/n) ")
        if menuControl(var):
            continue
        elif var.lower() == "y":
            try:
                modify_item = modify_products.getInput("Which item would you like to change?:")
                print(modify_item)
                new_value = modify_products.getInput("What would you like to change the price of the item to?: ")
                print(new_value)
                modify_products.updateProducts(PRODUCTS, int(modify_item), int(new_value))
                print("New prices updated to additional accessories: ")

                break
            except ValueError:
                print("Integers only")
        elif var.lower() == 'n':
            break
    return False


# Run the program #
play()
