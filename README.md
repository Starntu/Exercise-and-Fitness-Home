# Fitness and Exercise Home

#### Video Demo: <https://youtu.be/vyRFvOOwVEg>

#### -Description-
Fitness and Exercise Home is a tool used for people who want to get into, keep track of, and understand fitness and exercise. It allows you to find your bmi, set schedules, and look up information. You can add and delete exercise tasks to a table and include when you want to do them. You can also find an exercise that matches the type, muscle group, and difficulty you want. When you find that exercise you will be given the name, equipment, and instructions of that exercise. Fitness and Exercise Home is what people who want to get into exercise and become more physically active and healthier use.

## Project.py file

### Before explaining any functions in my code:
I would like to talk about my experience making my project. In all, I had quqite a fun time making it and really enjoyed the process. I was able to research my way through any problems I had. That saying, if I had to decide what was the hardest part, it would be writing all code relating to csv files. It took the longest for me to do and I had to go back and relearn things a lot. Despite that, everything worked out well.

### Main function:
The main function of my code interacts with the users through the command-line interface. It prompts them for things and prints explanations that allows them to use the functions of the project more easily. It also is where the information for the API used in my project is.

### Read function:
This function reads the csv file that has all the exercise tasks and dates the user inputted previously, returning them back in a list. However, if the file does not exist meaning this is the users first time, it simply returns an empty list.

### Save function:
Used to continuosly save any edits to the list of exercise tasks back to the csv file so the users progress is not deleted every rerun of the project.

### Delete function:
Used to open file and only write to it rows that do not match the parameters of the row the user wants deleted. Effectively deletes row.

### Valid_date function:
Used to make sure the user inputs a date that is actually a real date. Uses datetime to do so.

### Metric function:
Used to calculate and return BMI when height and weight are in metric units

### Imperial function:
Used to calculate and return BMI when height and weight are in imperial units. Height should already be seperated into feet and inches before being passed in to function.

### Interpret_bmi function:
Used to check what category users BMI puts them in and then returns the category as a string.

## Test_project.py file

### Overview
My testing file that tests 4 functions from my projecct.py file. These are the valid_date, metric, imperial, and interpret_bmi files. Using it I was able to make sure my project had as little bugs as possible.

## Requirements.txt File
### Overview
This requirements file is a simple list of all pip installations needed to run my project. There are only 2, tabulate, and requests.

## External API
The Fitness and Exercise Home project uses an external API from [API Ninjas](https://api.api-ninjas.com/v1/exercises). This API supplies access to a list of thousands of exercises, seperating the exercises into dictionaries with name, type, muscle, equipment, difficulty, and instructions keys.

## License
** This project is licensed under the Creative Commons Attribution 4.0 International License (CC-BY 4.0). See the [LICENSE](LICENSE) file for details. **
