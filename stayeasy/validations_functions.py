import models as m
import database as db
import pricing as pc
from datetime import datetime, timedelta
import exceptions as ex
import os
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
        list_of_objects.append(m.StandardRoom(room[0], room[2], 'Standard'))
    elif room[1] == 'Deluxe':
        list_of_objects.append(m.DeluxeRoom(room[0], room[2], 'Deluxe'))
    elif room[1] == 'Suite':
        list_of_objects.append(m.SuiteRoom(room[0], room[2], 'Suite'))
    else:
        appwrite = open("app.log",'a+')
        appwrite.write(f"{' '.join(room)} is not acceptable as no such room type is available.\n")
        appwrite.close()


def validation_and_check():
    while True:
        try:
            from datetime import datetime
            today = datetime.today().date()
            room_type = input("Please tell us your selection from available roomtypes (Standard/Deluxe/Suite): \n").lower().capitalize()
            no_of_guests = int(input("Hey, how many of you are planning to stay: \n"))
    
            try:
                check_in = input("Give check-in date in DD-MM-YYYY format: \n")
                check_in = datetime.strptime(check_in, "%d-%m-%Y").date()
                
            except:
                print("Give proper check-in date in format")
                continue

            try:
                check_out = input("Give check-out date in DD-MM-YYYY format: \n")
                check_out = datetime.strptime(check_out, "%d-%m-%Y").date()
                
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
            elif check_out <= check_in:
                print("Check out date cannot be before than Check in date.")
            elif (check_out - check_in).days > 30:
                print("The stay cannot be more than 30 days.")
            elif (check_in - today).days > 180:
                print("Cannot book a room this early")
            elif room_type == 'Standard' and no_of_guests > 2:
                print("A standard room can only accomedate maximum of 2 guests.")
                if no_of_guests == 3:
                    print("Instead, we can accomodate in Deluxe")
                    choice = input("You want us to fetch in Deluxe rooms? (y/n): \n")
                    if choice == 'y':
                        available_rooms = db.check_availability(check_in, check_out, 'Deluxe')
                        if not available_rooms:
                            print("No Deluxe rooms available.")
                            continue
                        print(f"The free rooms are: {available_rooms}")
                        room_no = min(available_rooms)
                        print(f"Allocating you: {room_no}")
                        return ['Deluxe', no_of_guests, check_in, check_out, room_no]
                        
                    else:
                        print("Thank you for visiting!! Bye")
                        break

                if no_of_guests == 4:
                    print("Instead, we can accomodate in Suite")
                    choice = input("You want us to fetch in suite rooms? (y/n): \n")
                    if choice == 'y':
                        available_rooms = db.check_availability(check_in, check_out, 'Suite')

                        if not available_rooms:
                            print("No Suite rooms available.")
                            continue
                        print(f"The free rooms are: {available_rooms}")
                        room_no = min(available_rooms)
                        print(f"Allocating you: {room_no}")
                        return ['Suite', no_of_guests, check_in, check_out, room_no]

                    else:
                        print("Thank you for visiting!! Bye")
                        break 
                

            elif room_type == 'Deluxe' and no_of_guests > 3:
                print("A deluxe room can only accomedate maximum of 3 guests.")
                print("Instead, we can accomodate in Suite")
                choice = input("You want us to fetch in suite rooms? (y/n): \n")
                if choice == 'y':
                    available_rooms = db.check_availability(check_in, check_out, 'Suite')
                    if not available_rooms:
                        print("No Suite rooms available.")
                        continue
                    print(f"The free rooms are: {available_rooms}")
                    room_no = min(available_rooms)
                    print(f"Allocating you: {room_no}")
                    return ['Suite', no_of_guests, check_in, check_out, room_no]
                else:
                    print("Thank you for visiting!! Bye")
                    break
            else:
                available_rooms = db.check_availability(check_in, check_out, room_type)
                if not available_rooms:
                    print("No rooms available.")
                    continue
                print(f"The available rooms are: {available_rooms}")
                room_no = min(available_rooms)
                print(f"Allocating you: {room_no}")
                return [room_type, no_of_guests, check_in, check_out, room_no]
        except Exception as e:
            print(f"Invalid input is given, try again.")


def create_booking(records):
    room_type = records[0]
    no_of_guests = records[1]
    check_in = records[2]
    check_out = records[3]
    room_no = records[4]

    available_rooms = db.check_availability(
    check_in, check_out, room_type)

    if room_no not in available_rooms:
        print("Sorry, this room is no longer available.")
        print("Please search for availability again.")
        return
    
    while True:
        try:
            breakfast_extra = False
            room_type = records[0]
            mobile_number = input("Enter the mobile number of guest: \n")
            if not db.is_newguest(mobile_number):
                print("Guest record is already present in database, lets proceed with booking.")

                guest_details = db.get_guest(mobile_number)
                guest_name = guest_details[0]
                email = guest_details[1]

                break

            guest_name = input("Enter the name of the guest: \n")
            email = input(f"Enter the email address of user {guest_name}: \n")
            if room_type == 'Standard':
                inpp = input("Do you want us to add breakfast(y/n): \n")
                if inpp == 'y':
                    breakfast_extra = True

            if guest_name == '':
                print("Guest name shouldnot be empty.")
            elif mobile_number == '':
                print("Mobile number shouldnot be empty.")
            elif not mobile_number.isdigit():
                print("Mobile number should not contain other than numbers.")
            elif email == '':
                print("Email cannot be empty.")
            elif len(mobile_number) != 10:
                print("Invalid mobile number, should have 10 digits.")
            elif mobile_number[0] not in ['6','7','8','9']:
                print("Invalid mobile number, should start with 6/7/8/9.")
            elif email[-10:] != '@gmail.com':
                print("Email should end with '@gmail.com'.")

            else:
                db.register_guest(mobile_number,guest_name, email)
                break


        except Exception as e:
            print(f"Guest registration error : {e}")

    print("Thanks are providing details. Let's proceed to booking.")

    cancellation_fees = 0
    status = 'CONFIRMED'


    pc.get_pricing(mobile_number, guest_name, email, room_no,  check_in, check_out, no_of_guests, room_type, db.is_loyal_customer(mobile_number), breakfast_extra, cancellation_fees, status)
    

def set_status():
    print("Hi, Welcome to stayeasy!")

    try:
        b_id = int(input("Please enter your booking ID: \n"))
    except ValueError:
        print("Invalid booking ID.")
        return

    booking = db.fetch_booking_by_id(b_id)

    if booking is None:
        print("Booking not found or booking is not confirmed.")
        return

    today = datetime.today().date().isoformat()
                                
    if booking[3] != today:
        print("Check-in is allowed only on the check-in date.")
        return

    if db.set_confirm(b_id):
        print("Checked-in successfully.")
    else:
        print("Unable to check in.")

        

def checkout_invoice():
    print("Hi, Welcome to stayeasy!")

    try:
        b_id = int(input("Please enter your booking ID: \n"))
    except ValueError:
        print("Invalid booking ID.")
        return

    booking = db.fetch_tocheckout_by_id(b_id)

    if booking is None:
        print("Booking not found or booking is not checked in.")
        return

    room_no = booking[1]
    room_type = booking[2]
    check_in = booking[3]
    check_out = booking[4]
    no_of_guests = booking[5]
    mob = booking[6]

    guest_details = db.get_guest(mob)
    guest_name = guest_details[0]
    email = guest_details[1]

    rows = db.get_invoice(mob, check_in)
    net_pay = db.get_netprice_invoice(mob, check_in)

    room_total = 0
    for row in rows:
        room_total += row[1]

    long_stay_discount = 0
    if (datetime.strptime(check_out, "%Y-%m-%d").date() -
            datetime.strptime(check_in, "%Y-%m-%d").date()).days >= 7:
        long_stay_discount = room_total * 0.10

    loyalty_discount = 0
    if db.is_loyal_customer(mob):
        loyalty_discount = (room_total - long_stay_discount) * 0.05

    total_discount = long_stay_discount + loyalty_discount

    total_gst = 0
    for row in rows:
        total_gst += row[5]

    os.makedirs("invoices", exist_ok=True)
    invoice_path = f"invoices/BK{b_id:04d}.txt"

    with open(invoice_path, 'w') as invoice:
        invoice.write("========== STAYEASY HOTEL INVOICE ==========\n\n")

        invoice.write(f"Booking ID: BK{b_id}\n")
        invoice.write(f"Guest Name: {guest_name}\n")
        invoice.write(f"Mobile Number: {mob}\n")
        invoice.write(f"Email: {email}\n")
        invoice.write(f"Room Number: {room_no}\n")
        invoice.write(f"Room Type: {room_type}\n")
        invoice.write(f"Number of Guests: {no_of_guests}\n")
        invoice.write(
            f"Check-in Date: "
            f"{datetime.strptime(check_in, '%Y-%m-%d').strftime('%d-%m-%Y')}\n"
        )
        invoice.write(
            f"Check-out Date: "
            f"{datetime.strptime(check_out, '%Y-%m-%d').strftime('%d-%m-%Y')}\n"
        )

        invoice.write("\n--------------- DAILY BREAKDOWN ---------------\n")

        for row in rows:
            date = datetime.strptime(row[0], "%Y-%m-%d").strftime("%d-%m-%Y")

            invoice.write(f"\nDate: {date}\n")
            invoice.write(f"Room Tariff: Rs. {row[1]:.2f}\n")
            invoice.write(f"Extra Guest Charge: Rs. {row[2]:.2f}\n")
            invoice.write(f"Breakfast Charge: Rs. {row[3]:.2f}\n")
            invoice.write(f"Day Bill: Rs. {row[4]:.2f}\n")
            invoice.write(f"GST: Rs. {row[5]:.2f}\n")
            invoice.write(f"Daily Total: Rs. {row[6]:.2f}\n")

        invoice.write("\n--------------- PAYMENT SUMMARY ---------------\n")
        invoice.write(f"Room Charges: Rs. {room_total:.2f}\n")
        invoice.write(f"Long-stay Discount: Rs. {long_stay_discount:.2f}\n")
        invoice.write(f"Loyalty Discount: Rs. {loyalty_discount:.2f}\n")
        invoice.write(f"Total Discount: Rs. {total_discount:.2f}\n")
        invoice.write(f"Total GST: Rs. {total_gst:.2f}\n")
        invoice.write(f"Final Amount Paid: Rs. {net_pay:.2f}\n")

        invoice.write("\nThank you for staying with StayEasy!\n")

    if db.set_checkedout(b_id):
        print(f"Checkout successful. Invoice generated: {invoice_path}")
    else:
        print("Invoice generated, but checkout status could not be updated.")

def cancel_booking():
    print("Hi, Welcome to stayeasy!")
    try:
        b_id = int(input("Please enter your booking ID: \n"))
    except ValueError:
        print("Invalid booking ID.")
        return
    if db.cancel_booking(b_id):
        print("Booking cancelled successfully.")
    else:
        print("Booking not found or cannot be cancelled.")

def get_booking():
    print("Hi, Welcome to stayeasy!")
    mob = input("Please enter your mobile number to validate: \n")
    if len(db.fetch_booking(mob)) == 0:
        print("Sorry, No active booking was found with this mobile number.")
    else:
        for row in db.fetch_booking(mob):
            print(f"Booking ID: {row[0]}, Room No: {row[1]}, Room Type: {row[2]}, Check-in date: {row[3]}, Check-out date: {row[4]}, Number of guests: {row[5]}")

def get_bookings_mob():
    print("Hi, Welcome to stayeasy!")
    mob = input("Please enter your mobile number to validate: \n")
    if len(db.fetch_booking_mob(mob)) == 0:
        print("Sorry, No  booking was found with this mobile number.")
    else:
        for row in db.fetch_booking_mob(mob):
            print(f"Booking ID: {row[0]}, Room No: {row[1]}, Room Type: {row[2]}, Check-in date: {row[3]}, Check-out date: {row[4]}, Number of guests: {row[5]}")
    
def occupancy_report():
    start = input("Enter the start date of the range to begin in DD-MM-YYYY format: \n")
    end =  input("Enter the end date of the range to begin in DD-MM-YYYY format: \n")
    start = datetime.strptime(start, "%d-%m-%Y").date()
    end = datetime.strptime(end, "%d-%m-%Y").date()
    if start > end:
        print("Start date cannot be after end date.")
        return
    
    day_count = 0
    day_avg = 0
    while start <= end:
        print(f"On {start}")
        print(f"The total number of rooms occupied: {db.occupy_report(start.isoformat())}")
        print(f"The total number of rooms: {len(list_of_objects)}")
        print(f"Occupancy report: {db.occupy_report(start.isoformat())*100/len(list_of_objects)}") 
        day_count += 1
        day_avg += db.occupy_report(start.isoformat())/len(list_of_objects)
        start += timedelta(days=1)   
    print(f"The Average Occupancy for the whole range: {day_avg/ day_count}")     

def revenue_report():
    db.get_revenue('Standard')
    db.get_revenue('Deluxe')
    db.get_revenue('Suite')






    
