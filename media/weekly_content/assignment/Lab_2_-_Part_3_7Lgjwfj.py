# a. Count the number of odd numbers in L:
L = [19, 52, 87, 2, 8, 11, 18, 22]

# Use list comprehension and the modulo operator to find odd numbers
odd_numbers = [num for num in L if num % 2 != 0]

# The count of odd numbers is the length of this list
count = len(odd_numbers)

print(f"The number of odd numbers in L is {count}.")

# b. Calculate the average of all even numbers in L:
L = [38, 5, 7, 2, 8,112,18,400]

# Use list comprehension and the modulo operator to find even numbers
even_numbers = [num for num in L if num % 2 == 0]

# The average of even numbers is the sum of these numbers divided by the count
average = sum(even_numbers) / len(even_numbers)

print(f"The average of all even numbers in L is {average}.")

# c. Find the largest and the smallest number in L:

L = [38, 5, 7, 2, 8,112,18,400]

# Use the built-in functions min() and max() to find the smallest and largest number
smallest = min(L)
largest = max(L)

print(f"The smallest number in L is {smallest} and the largest number is {largest}.")





