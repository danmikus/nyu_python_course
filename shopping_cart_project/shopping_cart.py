import datetime
import os
import sys
from operator import itemgetter

def get_input(products):
    # Get user inputs. Validates input by checking for integer between 1 and the number of products there are.

    shopping_list = []
    while True:
        user_input = input("Please input a product identifier, or type 'DONE' if there are no more items: ")
        if user_input.strip() == "DONE":
            break
        try:
            int_input = int(user_input)
        except ValueError:
            print("ERROR: Please enter an integer")
            continue
        if int_input < 1 or int_input > len(products):
            print("ERROR: Please enter a product number between 1 and %s" % len(products))
            continue
        else:
            shopping_list.append(int(user_input))
    return shopping_list

def calc_list(input_list, full_list):
    # Retrieves the data for products given the user inputs. This includes deduplicating the list by
    # getting the number of each product and caculating the total of each type. Also sorts products alphabetically and capitalizes department names

    all_products = []

    for product in input_list:
        temp_array = []
        all_info = list(filter(lambda x: x["id"] == product, full_list))
        temp_array.extend([all_info[0]["id"],all_info[0]["name"], all_info[0]["price"],all_info[0]["department"].title()])
        all_products.append(temp_array)
    deduped_list = dedupe(all_products)
    total_indv_cost = sorted(get_total(deduped_list), key=itemgetter(3, 1))

    return total_indv_cost

def dedupe(scanned_list):
    # gets the number of each input

    unique_list =  [list(x) for x in set(tuple(x) for x in scanned_list)]
    #adopted from https://stackoverflow.com/questions/3724551/python-uniqueness-for-list-of-lists

    for product in unique_list:
        count = scanned_list.count(product)
        product.append(count)

    return unique_list

def get_total(input_list):
    # Calculates the total for each product
    # (e.g. 2 of a product @$1.00 ea. gets the total of $2.00)

    for product in input_list:
        product.append(product[2] * product[4])

    return input_list

def organize_departments(lst):
    # Organizes the products by their respective department. Also organizes departments alphabetically.

    departments = list(set(x[3] for x in lst))
    dep_lists = []
    for y in departments:
        temp = []
        temp.append(y)
        dep_lists.append(temp)

    for dept in dep_lists:
        temp_array = []
        for product in lst:
            if dept[0] == product[3]:
                temp_array.append(product)
        dept.append(temp_array)

    alpha_dept = sorted(dep_lists, key=itemgetter(0))

    return alpha_dept

def print_to_screen(header, lists, footer):
    # Prints receipt to the terminal

    print(header)
    for dept in lists:
        print("\n    " + dept[0])
        for product in dept[1]:
            print("    + {0} {1} (@ ${2:.2f} ea.) - ${3:.2f}".format(product[4], product[1], product[2], product[5]))
    print(footer)

def write_to_receipt(header, lists, footer, time):
    # Writes the receipt to a folder called "receipts" in the pwd. If the directory doesn't exist, it's created.

    path = "receipts"

    if not os.path.exists(path):
        os.makedirs(path)

    file_name = str(time) + ".txt"
    receipt = open(os.path.join(path, file_name), 'w')

    receipt.write(header + "\n")
    for dept in lists:
        receipt.write("\n    " + dept[0] + "\n")
        for product in dept[1]:
            receipt.write("    + {0} {1} (@ ${2:.2f} ea.) - ${3:.2f}\n".format(product[4], product[1], product[2], product[5]))
    receipt.write(footer)
    receipt.close()

def main():

    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M")

    receipt_header = """
    --------------------------------------------------
    Mikus Mart of Park Slope
    --------------------------------------------------
    Web: https://github.com/danmikus/nyu_python_course
    Phone: 212-867-5309
    Checkout Time: {0}
    --------------------------------------------------
    Shopping Cart Items:""".format(time)

    products = [
        {"id":1, "name": "Chocolate Sandwich Cookies", "department": "snacks", "aisle": "cookies cakes", "price": 3.50},
        {"id":2, "name": "All-Seasons Salt", "department": "pantry", "aisle": "spices seasonings", "price": 4.99},
        {"id":3, "name": "Robust Golden Unsweetened Oolong Tea", "department": "beverages", "aisle": "tea", "price": 2.49},
        {"id":4, "name": "Smart Ones Classic Favorites Mini Rigatoni With Vodka Cream Sauce", "department": "frozen", "aisle": "frozen meals", "price": 6.99},
        {"id":5, "name": "Green Chile Anytime Sauce", "department": "pantry", "aisle": "marinades meat preparation", "price": 7.99},
        {"id":6, "name": "Dry Nose Oil", "department": "personal care", "aisle": "cold flu allergy", "price": 21.99},
        {"id":7, "name": "Pure Coconut Water With Orange", "department": "beverages", "aisle": "juice nectars", "price": 3.50},
        {"id":8, "name": "Cut Russet Potatoes Steam N' Mash", "department": "frozen", "aisle": "frozen produce", "price": 4.25},
        {"id":9, "name": "Light Strawberry Blueberry Yogurt", "department": "dairy eggs", "aisle": "yogurt", "price": 6.50},
        {"id":10, "name": "Sparkling Orange Juice & Prickly Pear Beverage", "department": "beverages", "aisle": "water seltzer sparkling water", "price": 2.99},
        {"id":11, "name": "Peach Mango Juice", "department": "beverages", "aisle": "refrigerated", "price": 1.99},
        {"id":12, "name": "Chocolate Fudge Layer Cake", "department": "frozen", "aisle": "frozen dessert", "price": 18.50},
        {"id":13, "name": "Saline Nasal Mist", "department": "personal care", "aisle": "cold flu allergy", "price": 16.00},
        {"id":14, "name": "Fresh Scent Dishwasher Cleaner", "department": "household", "aisle": "dish detergents", "price": 4.99},
        {"id":15, "name": "Overnight Diapers Size 6", "department": "babies", "aisle": "diapers wipes", "price": 25.50},
        {"id":16, "name": "Mint Chocolate Flavored Syrup", "department": "snacks", "aisle": "ice cream toppings", "price": 4.50},
        {"id":17, "name": "Rendered Duck Fat", "department": "meat seafood", "aisle": "poultry counter", "price": 9.99},
        {"id":18, "name": "Pizza for One Suprema Frozen Pizza", "department": "frozen", "aisle": "frozen pizza", "price": 12.50},
        {"id":19, "name": "Gluten Free Quinoa Three Cheese & Mushroom Blend", "department": "dry goods pasta", "aisle": "grains rice dried goods", "price": 3.99},
        {"id":20, "name": "Pomegranate Cranberry & Aloe Vera Enrich Drink", "department": "beverages", "aisle": "juice nectars", "price": 4.25}
        ]
        # Products based on data from Instacart: https://www.instacart.com/datasets/grocery-shopping-2017

    #inputs = range(1, 21, 1)
    #this input is used for debugging inputs. Uncomment for use

    inputs = get_input(products)
    prices = calc_list(inputs, products)
    subtotal = sum(i[5] for i in prices)
    tax = subtotal * 0.08875
    total = subtotal * 1.08875

    formatted_list = organize_departments(prices)



    receipt_footer = """    --------------------------------------------------
    Subtotal: ${0:.2f}
    NYC Sales Tax (@8.875%): {1:.2f}
    Total: {2:.2f}
    --------------------------------------------------
    Thank you for your patronage! Please come again!
    """.format(subtotal, tax, total)

    print_to_screen(receipt_header, formatted_list, receipt_footer)
    write_to_receipt(receipt_header, formatted_list, receipt_footer, now)

if __name__ == "__main__":
    main()

#import pdb; pdb.set_trace()
