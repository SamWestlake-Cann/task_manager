# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username,password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate Reports
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r':
        '''Add a new user to the user.txt file'''
        # - Request input of a new username
        new_username = input("New Username: ")

        # - Request input of a new password
        new_password = input("New Password: ")

        # - Request input of password confirmation.
        confirm_password = input("Confirm Password: ")

        # - Check if the new password and confirmed password are the same.
        if new_password == confirm_password:
            # - If they are the same, add them to the user.txt file,
            print("New user added")
            username_password[new_username] = new_password
            
            with open("user.txt", "w") as out_file:
                user_data = []
                for k in username_password:
                    user_data.append(f"{k};{username_password[k]}")
                out_file.write("\n".join(user_data))

        # - Otherwise you present a relevant message.
        else:
            print("Passwords do no match")
            
            input("Press enter to continue")

    elif menu == 'a':
        '''Allow a user to add a new task to task.txt file
            Prompt a user for the following: 
             - A username of the person whom the task is assigned to,
             - A title of a task,
             - A description of the task and 
             - the due date of the task.'''
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            continue
        task_title = input("Title of Task: ")
        task_description = input("Description of Task: ")
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                break

            except ValueError:
                print("Invalid datetime format. Please use the format specified")


        # Then get the current date.
        curr_date = date.today()
        ''' Add the data to the file task.txt and
            Include 'No' to indicate if the task is complete.'''
        new_task = {
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": False
        }

        task_list.append(new_task)
        with open("tasks.txt", "w") as task_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))
        print("Task successfully added.")
        
        input("Press enter to continue")


    elif menu == 'va':
        '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling) 
        '''

        for t in task_list:
            disp_str = f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            print(disp_str)
            
            input("Press enter to continue")
            


    elif menu == 'vm':
        '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling)
        '''
        for t in task_list:
            if t['username'] == curr_user:
                disp_str = f"Task: \t\t {t['title']}\n"
                disp_str += f"Assigned to: \t {t['username']}\n"
                disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Task Description: \n {t['description']}\n"
                print(disp_str)
                
                input("Press enter to continue")
                
    
    elif menu == 'gr':
        
        # creating dictionary with values for task_overview file
        stat_dict_task_overview = {
                    "Tasks": 0,
                    "Completed": 0,
                    "Uncompleted": 0,
                    "Overdue": 0,
                    "Percentage Incomplete": 0,
                    "Percentage Overdue": 0
                    }
        
        # creating dictionary with values for user_overview file
        stat_dict_user_overview = {
                    "Users": 0,
                    "Tasks": 0,
                    "Current user tasks": 0,
                    "Percent assigned me": 0,
                    "My Completed tasks": 0,
                    "My incomplete tasks": 0,
                    "Percent incomplete and overdue": 0
                    
                         }
       
        # Creating variables for both stat_dict
        sdto = stat_dict_task_overview
        sduo = stat_dict_user_overview
        
        # Open task.txt as task
        with open("tasks.txt", "r") as task:
            # create variable to hold length of task_list
            amount_tasks = len(task_list)
            # Set stat_dict_task_overview["Tasks"] to amount_task 
            sdto["Tasks"] = amount_tasks
            
            
        # updating stat_dict_task_overview from task.txt  
        current_date = datetime.today()
        for task in task_list:
            if task["completed"]:
                sdto["Completed"] += 1
            else:
                sdto["Uncompleted"] += 1
                if task["due_date"] < current_date:
                    sdto["Overdue"] += 1
                
        
        
        # updating stat_dict_task_overview from task.txt 
        percent_incomplete = (sdto["Uncompleted"] / sdto["Tasks"]) *100
        sdto["Percentage Incomplete"] = round(percent_incomplete)
        
        percent_overdue = (sdto["Overdue"] / sdto["Tasks"]) *100
        sdto["Percentage Overdue"] = round(percent_overdue) 
        
        users = len(username_password)
        sduo["Users"] = users    
        sduo["Tasks"] = amount_tasks
        
        
        # updating stat_dict_user_overview from task.txt 
        user_overdue = 0
        for task in task_list:
            if task["username"] == curr_user:
                sduo["Current user tasks"] += 1
                if task["completed"]:
                    sduo["My Completed tasks"] += 1
                else:
                    sduo["My incomplete tasks"] += 1
                    if task["due_date"] < current_date:
                        user_overdue += 1
                        
        percentage_user_overdue = (user_overdue /   sduo["Current user tasks"]) *100
        percent_assigned_me = (sduo["Current user tasks"] /  sduo["Tasks"]) *100
        sduo["Percent incomplete and overdue"] = round(percentage_user_overdue)
        sduo["Percent assigned me"] = round(percent_assigned_me)
        
        
        
        # setting variables for each value in stat_dict_task_overview 
        sdto_tasks = stat_dict_task_overview["Tasks"]
        sdto_completed = stat_dict_task_overview["Completed"]
        sdto_uncompleted = stat_dict_task_overview["Uncompleted"]
        sdto_overdue = stat_dict_task_overview["Overdue"]
        sdto_perc_incomplete = stat_dict_task_overview["Percentage Incomplete"]
        sdto_perc_overdue = stat_dict_task_overview["Percentage Overdue"]         
        
        # Open and write to task_overview.txt
        with open("task_overview.txt", "w+") as file:
            file.write("""
            -----------------------------------
                      TASK OVERVIEW            
            -----------------------------------\n\n""")
            file.write(f"""\t\t\tAmount of tasks: {sdto_tasks}
            Amount of tasks Completed: {sdto_completed}
            Amount of tasks Uncompleted: {sdto_uncompleted}
            Amount of tasks Overdue: {sdto_overdue}
            Percentage of tasks Incomplete: %{sdto_perc_incomplete}
            Percentage of tasks Overdue: %{sdto_perc_overdue}
            """)              
        
        
        # setting variables for each value in stat_dict_user_overview 
        sduo_users = stat_dict_user_overview["Users"]    
        sduo_tasks = stat_dict_user_overview["Tasks"]
        sduo_curr_user_task = stat_dict_user_overview["Current user tasks"]
        sduo_perc_ass_me = stat_dict_user_overview["Percent assigned me"]
        sduo_my_completed = stat_dict_user_overview["My Completed tasks"]
        sduo_my_incomplete = stat_dict_user_overview["My incomplete tasks"]
        sduo_perc_inc_and_overdue = stat_dict_user_overview["Percent incomplete and overdue"]            
        
         # Open and write to user_overview.txt
        with open("user_overview.txt", "w+") as file:
            file.write("""
            -----------------------------------
                      USER OVERVIEW            
            -----------------------------------\n\n""") 
            file.write(f"""\t\t\tAmount of users: {sduo_users}
            Amount of tasks: {sduo_tasks}
            Your amount of tasks: {sduo_curr_user_task}
            My Completed tasks: {sduo_my_completed}
            My Incomplete tasks: {sduo_my_incomplete}
            Percentage of tasks assigned to you: %{sduo_perc_ass_me}
            Percentage of my tasks incomplete and overdue: %{sduo_perc_inc_and_overdue}
            
            """)
            
            
        input("Press enter to continue")
            
                        
    elif menu == 'ds' and curr_user == 'admin': 
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''
        num_users = len(username_password.keys())
        num_tasks = len(task_list)

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")
        
        input("Press enter to continue")    

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")
        
        input("Press enter to continue")