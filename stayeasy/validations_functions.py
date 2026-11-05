import models as m
import database as db
file = open("rooms.csv", 'r')
rooms = file.readlines()
roomdata = []
list_of_objects = []
for room in rooms:
    roomdata.append(room.split())
roomdata.pop(0)

file.close()

for room in roomdata:
    if room[1] == 'Standard':
        list_of_objects.append(m.StandardRoom(room[0], room[2]))
    elif room[1] == 'Deluxe':
        list_of_objects.append(m.DeluxeRoom(room[0], room[2]))
    elif room[1] == 'Suite':
        list_of_objects.append(m.SuiteRoom(room[0], room[2]))
    else:
        appwrite = open("app.log",'a+')
        appwrite.write(f"{" ".join(room)} is not acceptable as no such room type is available.\n")
        appwrite.close()


def validation_and_check():
    while True:
        try:
            from datetime import datetime
            today = datetime.today().date()
            room_type = input("Please tell us your selection from available roomtypes (Standard/Deluxe/Suite): \n").lower().capitalize()
            no_of_guests = int(input("Hey, how many of you are planning to stay: \n"))
            try:
                check_in = input("Give check-in date in YYYY-MM-DD format: \n")
                check_in = datetime.strptime(check_in, "%Y-%m-%d")
            
            except:
                print("Give proper check-in date in format")
                continue

            try:
                check_out = input("Give check-out date in YYYY-MM-DD format: \n")
                check_out = datetime.strptime(check_out, "%Y-%m-%d")
                
            except:
                print("Give proper check-out date in format.")
                continue

            if room_type not in ['Standard','Deluxe', 'Suite']:
                print("You chose invalid choice of roomtype.")
            elif no_of_guests > 4:
                print("The maximum accomedation is for 4 people in one room, so please go through plans and divide yourselves.")
            elif no_of_guests <= 0:
                print("You gave invalid number of guests.")
            elif check_in < today:
                print("Check-in date cannot be in past")
            elif check_out < check_in:
                print("Check out date cannot be before than Check in date.")
            elif check_out - check_in > 30:
                print("The stay cannot be more than 30 days.")
            elif check_in - today > 180:
                print("Cannot book a room this early")
            elif room_type == 'Standard' and no_of_guests > 2:
                print("A standard room can only accomedate maximum of 2 guests.")
                if no_of_guests == 3:
                    print("Instead, we can accomodate in Deluxe")
                    choice = input("You want us to fetch in Deluxe rooms? (y/n): \n")
                    if choice == 'y':
                        print(f"The free rooms are: {m.check_availability(check_in, check_out, 'Deluxe')} ")
                        print(f"I am allocating you room number: {min(m.check_availability(check_in, check_out, 'Deluxe'))}")
                        return [room_type, no_of_guests, check_in, check_out, min(m.check_availability(check_in, check_out, 'Deluxe'))] 
                        
                    else:
                        print("Thank you for visiting!! Bye")
                        break

                if no_of_guests == 4:
                    print("Instead, we can accomodate in Suite")
                    choice = input("You want us to fetch in suite rooms? (y/n): \n")
                    if choice == 'y':
                        print(f"The free rooms are: {m.check_availability(check_in, check_out, 'Suite')}")
                        print(f"I am allocating you room number: {min(m.check_availability(check_in, check_out, 'Suite'))}")
                        return [room_type, no_of_guests, check_in, check_out, min(m.check_availability(check_in, check_out, 'Suite'))]
                        
                    else:
                        print("Thank you for visiting!! Bye")
                        break

            elif room_type == 'Deluxe' and no_of_guests > 3:
                print("A deluxe room can only accomedate maximum of 3 guests.")
                print("Instead, we can accomodate in Suite")
                choice = input("You want us to fetch in suite rooms? (y/n): \n")
                if choice == 'y':
                    print(f"The free rooms are: {m.check_availability(check_in, check_out, 'Suite')}")
                    print(f"I am allocating you room number: {min(m.check_availability(check_in, check_out, 'Suite'))}")
                    return [room_type, no_of_guests, check_in, check_out, min(m.check_availability(check_in, check_out, 'Suite'))]
                else:
                    print("Thank you for visiting!! Bye")
                    break
            else:
                print(f"The available rooms are: {m.check_availability(check_in, check_out, room_type)}")
                print(f"I am allocating you: {min(m.check_availability(check_in, check_out, room_type))}")
                return [room_type, no_of_guests, check_in, check_out, min(m.check_availability(check_in, check_out, room_type))]
        except Exception as e:
            print(f"Invalid input is given, try again.")


def create_booking(records):

    while True:
        try:
            mobile_number = input(f"Enter the mobile number of {guest_name} : \n")
            if not db.is_newguest(mobile_number):
                print("Guest record is already present in database, lets proceed with booking.")
                break

            guest_name = input("Enter the name of the guest: \n")
            email = input(f"Enter the email address of user {guest_name}: \n")

            if guest_name == '':
                print("Guest name shouldnot be empty.")
            elif mobile_number == '':
                print("Mobile number shouldnot be empty.")
            elif email == '':
                print("Email cannot be empty.")
            elif len(mobile_number) != 10:
                print("Invalid mobile number, should have 10 digits.")
            elif mobile_number[0] not in [6,7,8,9]:
                print("Invalid mobile number, should start with 6/7/8/9.")
            elif email[-10:] == '@gmail.com':
                print("Email should end with '@gmail.com'.")

            else:
                db.register_guest(mobile_number,guest_name, email)


        except Exception as e:
            print(f"Guest registration error : {e}")

    print("Thanks are providing details. Let's proceed to booking.")
    room_type = records[0]
    no_of_guests = records[1]
    check_in = records[2]
    check_out = records[3]
    room_no = records[4]
    cancellation_fees = 0
    status = 'CONFIRMED'
    

