import datetime
import os
import sys
from operator import itemgetter

def get_input(products):
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
    all_products = []

    for product in input_list:
        temp_array = []
        all_info = list(filter(lambda x: x["id"] == product, full_list))
        temp_array.extend([all_info[0]["id"],all_info[0]["name"], all_info[0]["price"],all_info[0]["department"]])
        all_products.append(temp_array)
    deduped_list = dedupe(all_products)
    total_indv_cost = get_total(deduped_list)

    alpha_sort = sorted(total_indv_cost, key=itemgetter(3, 1))

    return alpha_sort

def dedupe(scanned_list):
    unique_list =  [list(x) for x in set(tuple(x) for x in scanned_list)]
    #adopted from https://stackoverflow.com/questions/3724551/python-uniqueness-for-list-of-lists

    for product in unique_list:
        count = scanned_list.count(product)
        product.append(count)

    return unique_list

def get_total(input_list):
    for product in input_list:
        product.append(product[2] * product[4])

    return input_list

def print_to_screen(header, lists, footer):
    print(header)
    for item in lists:
        print("    + {0} {1} (@ ${2:.2f} ea.) - ${3:.2f}".format(item[4], item[1], item[2], item[5]))
    print(footer)

def write_to_receipt(header, lists, footer, time):

    path = "receipts"

    if not os.path.exists(path):
        os.makedirs(path)

    file_name = str(time) + ".txt"
    receipt = open(os.path.join(path, file_name), 'w')

    receipt.write(header + "\n")
    for item in lists:
        receipt.write("    + {0} {1} (@ ${2:.2f} ea.) - ${3:.2f}\n".format(item[4], item[1], item[2], item[5]))
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

    #inputs = get_input(products)
    inputs = [2, 2, 2, 6, 6, 1 ,3, 4, 10, 11, 12, 13]
    prices = calc_list(inputs, products)
    subtotal = sum(i[5] for i in prices)
    tax = subtotal * 0.08875
    total = subtotal * 1.08875

    receipt_footer = """    --------------------------------------------------
    Subtotal: ${0:.2f}
    NYC Sales Tax (@8.875%): {1:.2f}
    Total: {2:.2f}
    --------------------------------------------------
    Thank you for your patronage! Please come again!
    """.format(subtotal, tax, total)

    print_to_screen(receipt_header, prices, receipt_footer)
    write_to_receipt(receipt_header, prices, receipt_footer, now)

if __name__ == "__main__":
    main()

#import pdb; pdb.set_trace()
