from datetime import datetime
from datetime import timedelta

# Part 1 a)
print("Part 1 (a)")

date_str = input("Enter a date (MM/DD/YYYY): ")

try:
    date_obj = datetime.strptime(date_str, "%m/%d/%Y")
    print("Datetime object:", date_obj)
except ValueError:
    print("Invalid date format. Please enter a date in the format MM/DD/YYYY.")


# Part 1 b)
print("Part 1 (b)")
def format_datetime(date_obj):
    formatted_date = date_obj.strftime("%Y-%m-%dT%H:%M:%SZ")
    return formatted_date

formatted = format_datetime(date_obj)
print("Formatted datetime:", formatted)


# Part 1 c)
print("Part 1 (c)")
def separate_datetime(date_obj):
    date_str = date_obj.strftime("%Y-%m-%d")
    time_str = date_obj.strftime("%H:%M:%S")
    return date_str, time_str

date, time = separate_datetime(date_obj)
print("Date:", date)
print("Time:", time)


# Part 1 d)
print("Part 1 (d)")
date_input1 = input("Enter the first date in the format MM/DD/YYYY: ")
date_input2 = input("Enter the second date in the format MM/DD/YYYY: ")

date_object1 = datetime.strptime(date_input1, "%m/%d/%Y")
date_object2 = datetime.strptime(date_input2, "%m/%d/%Y")

difference = abs((date_object2 - date_object1).days)

print(f"The number of days between the two dates is {difference}")

# Part 1 e)
print("Part 1 (e)")

num_of_days = input("Add the number of days you want to add !! ")
int_days = int(num_of_days)

def add_days(dt, days):
    return dt + timedelta(days=days)

print(f"Adding {int_days} to date time object {date_obj} is equal to {add_days(date_obj, int_days)}")
