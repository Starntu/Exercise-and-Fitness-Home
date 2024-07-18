from sys import exit
from tabulate import tabulate
import csv
import requests
from datetime import datetime


def main():
    # Get API
    responses = requests.get(
        "https://api.api-ninjas.com/v1/exercises",
        headers={"X-Api-Key": "API_KEY"},
    )
    if responses.status_code == 200:
        data = responses.json()
    else:
        print(f"Failed to fetch data: {response.status_code}")

    # See if the user wants to go to the tracker or info
    wants = input("Are you here for the tracker or info or to see your bmi?: ")
    wants = wants.lower().capitalize()

    # Get the returned tasks from read()
    tasks = read("tasks.csv")
    # Initalize the header
    header = ["Exercise Task", "Day"]

    # On the BMI page, ask the user for their measurement system and then height and weight before giving them their interpreted BMI
    if wants == "Bmi":
        system = input("Do you use metric or imperial?: ")
        system = system.lower()
        if system == "metric":
            print("Height should be in meters")
            height = input("Height: ")
            weight = input("Weight: ")
            bmi = metric(height, weight)
            interpret_bmi(bmi)
            print(f"You are: {interpret_bmi(bmi)}")
        elif system == "imperial":
            height = input("Height: ")
            weight = input("Weight: ")
            try:
                feet, inches = height.split("'")
                bmi = imperial(feet, inches, weight)
                print(f"You are: {interpret_bmi(bmi)}")
            except ValueError:
                print("Invalid imperial height")
                exit(1)
        else:
            print("Neither metric nor imperial typed")
            exit(1)
    # Let users add or delete from their tracker
    elif wants == "Tracker":
        # Check to see if user wants to add or delete from the tracker
        modify = input("Type add to add to tracker or delete to delete from tracker: ")
        modify = modify.lower()
        modify = modify.capitalize()

        if modify == "Add":
            # If theres something in tasks because the file was made previously, show user the table first
            if tasks:
                print(tabulate(tasks, header, tablefmt="grid"))
            # Ask user for task and day to complete and add it to list,
            # Saving every time and printing the new table out until user presses control+d
            while True:
                try:
                    task = input("Task: ")
                    task = task.lower().capitalize()

                    date = input("Date: ")
                    date = valid_date(date)

                    tasks.append([task, date])

                    save("tasks.csv", tasks)
                    print(tabulate(tasks, header, tablefmt="grid"))
                except EOFError:
                    print("Saving and Exiting")
                    save("tasks.csv", tasks)
                    exit(1)
        elif modify == "Delete":
            # Can not delete if tasks is empty, if not empty, first show user whats in table
            if tasks:
                try:
                    print(tabulate(tasks, header, tablefmt="grid"))
                    print(
                        "Type in the exercise name and date, a row will only be deleted if it matches both"
                    )
                    name = input("Name of exercise that should be deleted: ")
                    date = input("Date of the exercise that should be deleted: ")
                    tasks = delete("tasks.csv", name, date)
                    save("tasks.csv", tasks)
                    print(tabulate(tasks, header, tablefmt="grid"))
                except EOFError:
                    print("Saving and Exiting")
                    save("tasks.csv", tasks)
                    exit(1)
            else:
                print("Nothing is in tracker")
                exit(1)
        else:
            print("Neither add nor delete inputted")
            exit(1)
    # On the info page, give users the list of options and then ask them for arguments before releasing exercise match
    elif wants == "Info":
        print("\nSay the type of exercise, the muscle group, and the difficulty.\n")
        print(
            "\nTypes are: cardio, olympic_weightlifting, plyometrics, powerlifting, strength, stretching, and strongman\n"
        )
        print(
            "\nMuscle groups are: abdominals, abductors, adductors, biceps, calves, chest, forearms, glutes, hamstrings, lats, lower_back, middle_back, neck, quadriceps, traps, and triceps\n"
        )
        print("\nDifficulty levels are: beginner, intermediate, and expert\n")
        _type = input("Type: ")
        _type = _type.lower()
        group = input("Muscle Group: ")
        group = group.lower()
        difficulty = input("Difficulty Level: ")
        difficulty = difficulty.lower()
        found = 0

        for response in data:
            if (
                response["type"] == _type
                and response["muscle"] == group
                and response["difficulty"] == difficulty
            ):
                print("Name: ", response["name"])
                print("Equipment: ", response["equipment"])
                print("Instructions: ", response["instructions"])
                found += 1

        if found == 0:
            print("No matching exercise found")
    else:
        print("Neither tracker nor info nor bmi inputted")
        exit(1)


# A function that reads the csv file of tasks if it exists, otherwise it passes. Returns tasks list
def read(filename):
    # Set an empty tasks list which will hold all the tasks the user adds
    tasks = []

    # If file exists, add all tasks to the tasks list otherwise pass
    try:
        with open(filename, "r", newline="") as file:
            # Read csv file
            reader = csv.reader(file)
            # Go through each row in file and add to table
            for row in reader:
                tasks.append(row)
    except FileNotFoundError:
        pass

    return tasks


# A function that saves to a file a list of tasks
def save(filename, tasks):
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(tasks)


# A function that deletes a row from csv file
def delete(filename, name, date):
    tasks = []

    with open(filename, "r", newline="") as fileread:
        # Read csv file
        reader = csv.reader(fileread)
        # Go through each row in file and add to table
        for row in reader:
            if row[0] == name and row[1] == date:
                continue
            tasks.append(row)

    return tasks


# A function that validates day
def valid_date(date):
    date_formats = [
        "%Y-%m-%d",  # YYYY-MM-DD
        "%Y/%m/%d",  # YYYY/MM/DD
        "%Y-%m-%d",  # YYYY-M-D
        "%Y/%m/%d",  # YYYY/M/D
        "%B %d, %Y",  # September 16, 2024
        "%d %B %Y",  # 16 September 2024
        "%m/%d/%Y",  # MM/DD/YYYY
        "%m-%d-%Y",  # MM-DD-YYYY
        "%m/%d/%Y",  # M/D/YYYY
        "%m-%d-%Y",  # M-D-YYYY
    ]

    for date_format in date_formats:
        try:
            datetime.strptime(date, date_format)
            return date
        except ValueError:
            continue

    raise ValueError


# A function that calculates BMI from height and weight when in metric
def metric(height, weight):
    try:
        height = float(height)
        weight = float(weight)
        bmi = weight / (height**2)
        return round(bmi, 2)
    except (ValueError, ZeroDivisionError, TypeError):
        return None


# A function that calculates BMI from height and weight when in imperial
def imperial(feet, inches, weight):
    try:
        feet = float(feet)
        inches = float(inches)
        weight = float(weight)

        weight = weight * 703
        con_feet = feet * 12
        total_inches = con_feet + inches
        bmi = weight / (total_inches**2)
        return round(bmi, 2)
    except (ValueError, ZeroDivisionError, TypeError):
        return None


# A function that checks the BMI and returns BMI category
def interpret_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi >= 18.5 and bmi < 25:
        return "Normal weight"
    elif bmi >= 25 and bmi < 30:
        return "Overweight"
    elif bmi >= 30:
        return "Obese"


if __name__ == "__main__":
    main()
