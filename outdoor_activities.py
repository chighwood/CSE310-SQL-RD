"""Outdoor Activity Database"""

import sqlite3
conn = sqlite3.connect("database/database.db")
cursor = conn.cursor()

while True:
    print()
    # Allow user to choice what task they want to do
    choice = input("Type one of the following for the activity: \n 1. Add \n 2. Update \n 3. Delete \n 4. List of Activities \n Choice: ")
    print()

    if choice == "1":
        # This choice adds a new activity with all of the data needed in two different tables
        activity = input("Name of Activity: ")
        location = input("Location the activity took place: ")
        when = input("When did it happen M/D/Y: ")
        shelter = input("What shelter did you use: ")
        food = input("Favorite food that you ate during the activity: ")
        print()

        # Adds the data to the respective tables
        data1 = [ activity ]
        data2 = [ location, when, shelter, food ]

        cursor.execute("INSERT INTO `activities` (`activity`) VALUES (?)", data1)
        1
        cursor.execute("INSERT INTO `information` ( `location`, `when`, `shelter`, `food`) VALUES ( ?, ?, ?, ?)", data2)


    elif choice == "2":
        # Updates the activity depending on what the user wants to update
        id = input("Provide ID for the activity you want to change: ").strip()
        print()

        # Gather the infomation needed depending on the id chosen
        cursor.execute("SELECT * FROM activities WHERE id=?", (id,))
        activity = cursor.fetchone()

        if not activity:
            print("No activity found with the given ID.")
        else:
            # After the id is chosen, this allows the user to pick the exact information to change
            number = input("What information do you want to update? \n 1. Activity Name \n 2. Location \n 3. When \n 4. Shelter Used \n 5. Favorite Food Eaten \n Choice: ").strip()
            print()

            activity_fields = {
                "1": ("activities", "activity", "Enter the new Activity Name: ")
            }
            
            information_fields = {
                "2": ("information", "location", "Enter the new location: "),
                "3": ("information", "when", "Enter the new time (When): "),
                "4": ("information", "shelter", "Enter the new shelter used: "),
                "5": ("information", "food", "Enter the new favorite food eaten: ")
            }
            # This if statement choses which table to change depending on the choice above that is chosen
            if number in activity_fields:
                table, field, prompt = activity_fields[number]
            elif number in information_fields:
                table, field, prompt = information_fields[number]
            else:
                print("Invalid choice. Please select a valid option.")
                continue

            new_value = input(prompt).strip()
            # Insert new value into the corresponding table
            if new_value:
                if table == "activities":
                    cursor.execute(f"UPDATE {table} SET {field}=? WHERE id=?", (new_value, id))
                else:
                    cursor.execute(f"UPDATE {table} SET {field}=? WHERE activity_id=?", (new_value, id))

                # Report back to user that the changes were made
                conn.commit()
                print(f"{field.replace('_', ' ').capitalize()} updated successfully!")
                print()
            else:
                print("No update was made. You must enter a value.")


            
    elif choice == "3":
        # Delete fuction that allows the user to delete the activity of their choosing
        id = input("Provide ID for the activity you want to delete: ").strip()
        
        cursor.execute("SELECT activity FROM activities WHERE id=?", (id,))
        activity = cursor.fetchone()
        
        if activity:
            name = activity[0]
            # Ask the user if they are sure they want to delete it
            confirm = input(f"Are you sure you want to delete '{name}'? (yes/no): ").strip().lower()
            
            # Delete data from both tables to make sure no data is stored 
            if confirm == "yes" or "y":
                cursor.execute("DELETE FROM information WHERE activity_id=?", (id,))
                
                cursor.execute("DELETE FROM activities WHERE id=?", (id,))
                
                # User gets a message of it is deleled or deleting canceled depending on the choice they made
                conn.commit()
                print(f"Activity '{name}' and its related information have been deleted.")
                print()
            else:
                print("Deletion canceled.")
                print()
        else:
            print("No activity found with the given ID.")


    elif choice == "4":
        # Shows user all of the activites with the correct id number, the activity, and location of corresponding id
        query = ('SELECT a.id, a.activity, i.location FROM information i JOIN activities a ON a.id = i.activity_id')
        
        data = cursor.execute(query)
        activities = data.fetchall()

        if not activities:
            print("No activities found.")
        else:
            print("\nAll Activities:\n")
            for activity in activities:
                print(f"{activity[0]}. {activity[1]} - Location: {activity[2]}")
            print()

    else:
        break

    