# Create a list of fitness items
fit_items = ['treadmill', 'lifting bars', 'weights', 'exercise bike', 'rower', 'yoga mat', 'dumbbells', 'resistance bands', 'kettlebell', 'medicine ball']

# Initialize empty dictionaries to hold item categories and quantities
d1 = {}
d2 = {}

# Open the catalog file
with open('category.txt', 'r') as f:
    while True:
        # Read three lines at a time - item, category, quantity
        item = f.readline().strip()
        category = f.readline().strip()
        quantity = f.readline().strip()
        # Consume the empty line after each set
        empty_line = f.readline()

        # If the item line is empty, it means we've reached the end of the file, hence break
        if not item:
            break
        
        # Check if the item is in the fit_items list
        if item in fit_items:
            # If it is, add it to the dictionaries
            d1.update({item: category})
            d2.update({item: int(quantity)})
            # Print a line to show that a match was found in the file
            print(f"Found matching item in the file: {item}")

# Create a loop that will keep asking the user for an item
while True:
    # Ask the user for an item
    s = input("Enter a fitness item: ")

    try:
        # Try to find the item in the dictionaries
        category = d1[s]
        quantity = d2[s]

        # If it is found, print the category and quantity
        print("Category:", category)
        print("Quantity:", quantity)

        # Ask the user if they want to search for another item
        again = input("Do you want to search for another item? (yes/no): ")

        # If the user answers no, exit the loop
        if again.lower() == 'yes':
            continue
        else:
            break
    except KeyError:
        # If the item is not found in the dictionaries, print an error message
        print("The item you entered is not in the catalog. Please try again.")
