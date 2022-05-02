from tabulate import tabulate


class Input:
    def __init__(self, text=""):

        self.self = self
        self.text = text
        self.allowance = 0

    def getInput(self, text):  # Returns an input function in form of text from an instance
        self.self = self
        self.text = text

        return input(text)

    # validates if an input is a number
    def checkValidity(self, val):
        self.self = self
        try:
            if val.isnumeric():
                return val
            elif val.isspace():
                val = self.allowance
                return val

        except:
            print("|| Integers Only || Restarting Query ...")
            return False

        # if val.isnumeric():
        #     return val
        # elif val.isspace():
        #     val = self.allowance
        #     return val
        # else:

    # Updates the dictionary with the given argument at the end
    @staticmethod
    def updateBill(order, products, chosen_item):
        order['Items'] += [products['Items'][int(chosen_item)]]
        order['Prices'] += [products['Prices'][int(chosen_item)]]

    # order.update(PRODUCTS['Items'][int(chosen_item)])
    # order.update(PRODUCTS['Prices'][int(chosen_item)])

    # Uses tho tabulate module to output a table with the parsed argument as a dict
    @staticmethod
    def returnBill(order, headers):
        print("Your selected additional accessories: ")
        print(tabulate(order, headers, tablefmt="pipe"))
        print("-" * 46)

    # Returns the given dictionary to empty values
    @staticmethod
    def clearBill(order):
        order['Items'] = []
        order['Prices'] = []

    # Updates the dictionary with a parsed argument
    @staticmethod
    def updateProducts(products, index, value):
        products['Prices'][index] = value
