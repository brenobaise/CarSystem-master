from tabulate import tabulate


class Input:
    def __init__(self, text=""):

        self.self = self
        self.text = text
        self.val = None

    def getInput(self, text):  # Returns an input function in form of text from an instance
        self.self = self
        self.text = text

        return input(text)

    # validates if an input is a number
    def checkValidity(self, val, allowance=None):
        isAllowance = 0  # default value of val
        if val.isdigit():
            return val
        else:  # if not a digit, then check if allowance is parsed
            match allowance:
                # cases will execute based on the condition
                case True:
                    self.val = isAllowance
                    print("[SYSTEM] Allowance set to", self.val, "due to no input.")
                    return self.val
                case False:
                    if val.lower() == "clear":
                        return False
                    else:
                        print("[SYSTEM WARNING] Only Integers accepted, restarting query ...")
                        return False

    # Updates the dictionary with the given argument at the end
    @staticmethod
    def updateBill(order, products, chosen_item):
        order['Items'] += [products['Items'][int(chosen_item)]]
        order['Prices'] += [products['Prices'][int(chosen_item)]]

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
