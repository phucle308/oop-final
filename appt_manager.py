import os
from appointment import Appointment
PRICES = {
    0: 0,   
    1: 40,  
    2: 60,  
    3: 40,  
    4: 80}

def create_weekly_calendar(appt_list):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    appt_list.clear()
    
    for day in days:
        for hour in range(9, 17):
            new_appt = Appointment(day, hour)
            appt_list.append(new_appt)
            
    print("Wicked calendar created")
    
def load_schedule_appointments(appt_list):
    filename = input("Enter appointment filename: ")
    if not os.path.exists(filename):
        print(f"File not found. Re-enter appointment filename: {filename}")
        filename = input("Enter appointment filename: ")
        if not os.path.exists(filename):
            return 0
        
    count = 0
    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(',')
                    client_name = parts[0]
                    client_phone = parts[1]
                    appt_type = int(parts[2])
                    day = parts[3]
                    start_hour = int(parts[4])
                    
                    appt = find_appointment_by_time(appt_list, day, start_hour)
                    if appt:
                        appt.schedule(client_name, client_phone, appt_type)
                        count += 1
                        
        print(f"{count} previously scheduled appointments have been loaded")
        return count
    except Exception as e:
        print(f"Error loading file: {e}")
        return 0
    
def find_appointment_by_time(appt_list, day, start_hour):
    for appt in appt_list:
        if appt.get_day_of_week().lower() == day.lower() and appt.get_start_time_hour() == start_hour:
            return appt
        
    return None
    
def show_appointments_by_name(appt_list, client_name):
    print(f"Appointments for {client_name}")
    print(f"{'Client Name':<20} {'Phone':<15} {'Day':<10} {'Start':<7} {'End':<7} {'Type':<15}")
    print("-" * 80)
    
    found = False
    for appt in appt_list:
        if client_name.lower() in appt.get_client_name().lower() and appt.get_appt_type() != 0:
            print(appt)
            found = True
            
    if not found:
        print("No appointment found.")
        
def show_appointments_by_day(appt_list, day):
    print(f"Appointment for {day}")
    print(f"{'Client Name':<20} {'Phone':<15} {'Day':<10} {'Start':<7} {'End':<7} {'Type':<15}")
    print("-" * 80)
    
    for appt in appt_list:
        if appt.get_day_of_week().lower() == day.lower():
            print(appt)
            
def save_scheduled_appointments(appt_list):
    filename = input("Enter appointment filename: ")
    if os.path.exists(filename):
        overwrite = input(f"File already exists. Do you want to overwrite it (Y/N)? ").lower()
        if overwrite != 'y':
            filename = input("Enter appointment filename: ")
    
    count = 0
    try:
        with open(filename, 'w') as f:
            for appt in appt_list:
                if appt.get_appt_type() != 0:
                    f.write(appt.format_record() + "\n")
                    count += 1
                    
        print(f"{count} scheduled appointments have been successfully saved")
        return count
    except Exception as e:
        print(f"Error saving file: {e}")
        return 0
    
def print_menu():
    print("\n========================================")
    print(" Hair Salon Appointment Manager")
    print("========================================")
    print(" 1) Schedule an appointment")
    print(" 2) Find appointment by name")
    print(" 3) Print calendar for a specific day")
    print(" 4) Cancel an appointment")
    print(" 5) Change an appointment")
    print(" 6) Calculate total fees for a day")
    print(" 7) Calculate total weekly fees")
    print(" 9) Exit the system")
    
    selection = input("Enter your selection: ")
    return selection

def calculate_fees_per_day(appt_list):
    print(f"\nFees calculation per day...")
    day_input = input("What day: ")
    
    total_fees = 0
    valid_day_found = False
    
    for appt in appt_list:
        if appt.get_day_of_week().lower() == day_input.lower():
            valid_day_found = True
            appt_type = appt.get_appt_type()
            total_fees += PRICES.get(appt_type, 0)
            
    if valid_day_found:
        formatted_day = day_input.capitalize()
        print(f"Total fees for {formatted_day} is ${total_fees}")
    else:
        print(f"{day_input} is invalid day or the salon is closed")
        
def calculate_weekly_fees(appt_list):
    total_fees = 0
    for appt in appt_list:
        appt_type = appt.get_appt_type()
        total_fees += PRICES.get(appt_type, 0)
    print(f"Total weekly fees is ${total_fees}")
        
def change_appointment_by_day_time(appt_list):
    print(f"\nChange an appointment for:")
    old_day = input("What day: ")
    
    try:
        old_hour = int(input("Enter start hour (24 hour clock): "))
    except ValueError:
        print("Invalid hour format")
        return
    
    old_appt = find_appointment_by_time(appt_list, old_day, old_hour)
    
    if old_appt is None:
        print("Invalid day or time entered")
        return
    
    if old_appt.get_appt_type() == 0:
        print("That time slot isn't booked and doesn't need to be changed")
        return
    
    new_day = input("Enter a new day: ")
    try:
        new_hour = int(input("Enter start hour (24 hour clock): "))
    except ValueError:
        print("Invalid hour format.")
        return
    
    new_appt = find_appointment_by_time(appt_list, new_day, new_hour)
    
    if new_appt is None:
        print("Sorry that time slot is not in the weekly calendar!")
        return
    
    if new_appt.get_appt_type() != 0:
        print("The new time slot is already booked")
        return
    
    new_appt.schedule(old_appt.get_client_name(), old_appt.get_client_phone(), old_appt.get_appt_type())
    old_appt.cancel()
    
    print(f"Appointment for {new_appt.get_client_name()} has been changed to:")
    print(f"Day = {new_appt.get_day_of_week()}")
    print(f"Time = {new_appt.get_start_time_hour()}")
    
def main():
    print("Starting the Appointment Manager System")
    appointment_list = []
    create_weekly_calendar(appointment_list)
    
    load_choice = input("Would you like to load previously scheduled appointments from a file (Y/N)? ").lower()
    if load_choice == 'y':
        load_schedule_appointments(appointment_list)
        
    running = True
    
    while running:
        choice = print_menu()
        if choice == '1':
            print("\n** Sechedule an appointment **")
            day = input("What day: ")
            try:
                hour = int(input("Enter start hour (24 hour clock): "))
                appt = find_appointment_by_time(appointment_list, day, hour)
                
                if appt:
                    if appt.get_appt_type() == 0:
                        name = input("Client Name: ")
                        phone = input("Client Phone: ")
                        print("Appointment types")
                        print("1: Mens Cut $40, 2: Ladies Cut $60, 3: Mens Colouring $40, 4: Ladies Colouring $80")
                        type_code = int(input("Type of Appointment: "))
                        
                        if type_code in [1, 2, 3, 4]:
                            appt.schedule(name, phone, type_code)
                            print(f"OK, {name}'s appointment is scheduled!")
                        else:
                            print("Invalid appointment type.")
                    else:
                        print("Sorry that time slot is booked already!")
                else:
                    print("Sorry that time slot is not in the weekly calendar!")
            except ValueError:
                print("Invalid input format.")
                
        elif choice == '2':
            print("\n** Find appointment by name **")
            name = input("Enter Client Name: ")
            show_appointments_by_name(appointment_list, name)
            
        elif choice == '3':
            print("\n** Print calendar for a specific day **")
            day = input("Enter day of week: ")
            show_appointments_by_day(appointment_list, day)
            
        elif choice == '4':
            print("\n** Cancel an appointment **")
            day = input("What day: ")
            try:
                hour = int(input("Enter start hour (24 hour clock): "))
                appt = find_appointment_by_time(appointment_list, day, hour)
                
                if appt:
                    if appt.get_appt_type() != 0:
                        print(f"Appointment: {day} {hour}:00 - {hour+1}:00 for {appt.get_client_name()} has been cancelled!")
                        appt.cancel()
                    else:
                        print("That time slot isn't booked and doesn't need to be cancelled")
                else:
                    print("Sorry that time slot is not in the weekly calendar!")
            except ValueError:
                print("Invalid input.")
                
        elif choice == '5':
            change_appointment_by_day_time(appointment_list)
            
        elif choice == '6':
            calculate_fees_per_day(appointment_list)
            
        elif choice == '7':
            calculate_weekly_fees(appointment_list)
            
        elif choice == '9':
            print("\n** Exit the system **")
            save = input("Would you like to save all scheduled appointments to save all scheduled appointments to a file (Y/N)? ").lower()
            if save == 'y':
                save_scheduled_appointments(appointment_list)
            print("Good Bye!")
            running = False
            
        else:
            print("\nInvalid option")
                
if __name__ == "__main__":
    main()