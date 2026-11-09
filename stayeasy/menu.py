import os
from pathlib import Path

os.chdir(Path(__file__).resolve().parent)

import database as db
import validations_functions as va
import models as m
flag = False
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
        choice = int(input("Enter your choice from menu: \n"))
        if choice == 1:
            records = va.validation_and_check()
            flag = records is not None
        elif choice == 2:
            if flag:
                va.create_booking(records)
            else:
                print("Check for availability first.")
        elif choice == 3:
            va.set_status()
        elif choice == 4:
            va.checkout_invoice()
        elif choice == 5:
            va.cancel_booking()
        elif choice == 6:
            va.get_booking()
        elif choice == 7:
            va.get_bookings_mob()
        elif choice == 8:
            va.occupancy_report()
        elif choice == 9:
            va.revenue_report()
        elif choice == 10:
            db.export_bookings()
        elif choice == 11:
            print("Thanks!! Visit again.")
            break
        else:
            print("Enter your selection from menu in the range of 1-11.")

    except:
        print("Enter valid input.")
        
