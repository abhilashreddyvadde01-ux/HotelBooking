import database as db
import validations_functions as va
import models as m

while True:
    try:
        print("""
            1. Search room availability
            2. Create booking
            3. Check in
            4. Check out (generate invoice)
            5. Cancel booking
            6. View booking details
            7. Guest stay history (by mobile number)
            8. Occupancy report (for a date range)
            9. Revenue report (by room type)
            10. Export all bookings to CSV
            11. Exit
        """)
        print()
        choice = int(input("Enter your choice from menu."))
        if choice == 1:
            records = va.validation_and_check()
        elif choice == 2:
            create_booking(records)
        elif choice == 3:
            pass
        elif choice == 4:
            pass
        elif choice == 5:
            pass
        elif choice == 6:
            pass
        elif choice == 7:
            pass
        elif choice == 8:
            pass
        elif choice == 9:
            pass
        elif choice == 10:
            pass
        elif choice == 11:
            print("Thanks!! Visit again.")
        else:
            print("Enter your selection from menu in the range of 1-11.")

    except:
        print("Enter valid input.")