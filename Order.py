from tabulate import tabulate


class Input:
    def __init__(self, text=""):
        self.self = self
        self.text = text

    def getInput(self, text):  # Returns an input function in form of text from an instance
        self.self = self
        self.text = text

        return input(text)

    def checkValidity(self, val):  # validates if an input is a number
        self.self = self
        if val.isnumeric():
            return val
        else:
            print("|| Integers Only || Restarting Query ...")
            return False

    @staticmethod
    def updateBill(order, products, chosen_item):  # Updates the dictionary with the given argument at the end
        order['Items'] += [products['Items'][int(chosen_item)]]
        order['Prices'] += [products['Prices'][int(chosen_item)]]

    # order.update(products['Items'][int(chosen_item)])
    # order.update(products['Prices'][int(chosen_item)])

    @staticmethod
    def returnBill(order, headers):  # Uses tho tabulate module to output a table with the parsed argument as a dict
        print("Your selected additional accessories: ")
        print(tabulate(order, headers, tablefmt="pipe"))
        print("-" * 46)

    @staticmethod
    def clearBill(order):
        order['Items'] = []
        order['Prices'] = []

    @staticmethod
    def updateProducts(products, index, value):
        products['Prices'][index] = value
