import sqlite3
from datetime import datetime
import exceptions as ex
import csv
conn = sqlite3.Connection('stayeasy.db')
curr = conn.cursor()

try:
    curr.execute("""
    CREATE TABLE IF NOT EXISTS guests(
        mobile_number TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL )""")

    curr.execute("""
    CREATE TABLE IF NOT EXISTS bookings(
        booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
        mobile_number TEXT REFERENCES guests(mobile_number),
        room_no TEXT,
        room_type TEXT,
        check_in TEXT,
        check_out TEXT,
        num_guests INTEGER,
        status TEXT,
        cancellation_fees INTEGER,
        gst_amount INTEGER,
        total_amount INTEGER)""")

    curr.execute("""
        CREATE TABLE IF NOT EXISTS pricings(
        mobile_number TEXT,
        name TEXT,
        email TEXT,
        room_no TEXT,
        check_in TEXT,
        check_out TEXT,
        no_of_guests INTEGER,
        current_date TEXT,
        room_tariff INTEGER,
        extra_guest INTEGER,
        breakfast_cost INTEGER, 
        day_bill INTEGER, 
        gst_amount INTEGER, 
        total_perday_bill INTEGER)""")
    

    def check_availability(check_in, check_out, room_type):
        import validations_functions as va
        result = []
        occupied_rooms_list = []
        curr.execute("""
            SELECT room_no FROM bookings
            WHERE check_in < ?
            AND check_out > ?
            AND room_type = ?
            AND status NOT IN ('CANCELLED', 'CHECKED_OUT')""", (check_out, check_in, room_type))
        
        occupied_rooms = curr.fetchall()
        for item in occupied_rooms:
            occupied_rooms_list.append(item[0])
        for room in va.list_of_objects:
            if room.room_type == room_type:
                if room.room_no not in occupied_rooms_list:
                    result.append(int(room.room_no))
        return result

    def is_newguest(mobile_number):
        curr.execute("SELECT name FROM guests WHERE mobile_number == ?",(mobile_number, ))
        flag = curr.fetchall()
        if len(flag) == 0:
            return True
        else:
            return False
        
    def register_guest(mobile_number, guest_name, email):
        curr.execute("INSERT OR IGNORE INTO guests VALUES(?,?,?)", (mobile_number, guest_name, email))
        conn.commit()

    def register_pricings(mobile_number, name, email, room_no, check_in, check_out, no_of_guests, start_date, room_tariff, extra_guest, breakfast_cost, day_bill, gst_amount, total_perday_bill):
        curr.execute("""INSERT INTO pricings VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (mobile_number, name, email, room_no, check_in, check_out,
        no_of_guests, start_date, room_tariff, extra_guest,
        breakfast_cost, day_bill, gst_amount, total_perday_bill))
        
    def register_booking(mobile_number, room_no, room_type, check_in, check_out, no_of_guests, status, cancellation_fees, net_pay, net_gst):
        curr.execute("""INSERT INTO bookings (mobile_number, room_no, room_type, check_in,check_out, num_guests, status, cancellation_fees, gst_amount, total_amount)VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (mobile_number, room_no, room_type, check_in, check_out,
      no_of_guests, status, cancellation_fees, net_gst, net_pay))
        conn.commit()

    def is_loyal_customer(mobile_number):
        curr.execute("""
            SELECT COUNT(*) FROM bookings
            WHERE mobile_number = ? AND status = 'CHECKED_OUT'""", (mobile_number,))

        result = curr.fetchone()

        if result[0] >= 3:
            return True
        else:
            return False

    def get_guest(mobile_number):
        curr.execute(
            "SELECT name, email FROM guests WHERE mobile_number = ?",
            (mobile_number,)
        )
        return curr.fetchone()

    def fetch_booking(mob):
        today = datetime.today().date().isoformat()

        curr.execute("SELECT booking_id, room_no, room_type, check_in, check_out, num_guests FROM bookings WHERE mobile_number = ? AND check_in >= ? AND status = 'CONFIRMED' ", (mob, today))
        
        return curr.fetchall()

    def fetch_booking_by_id(b_id):
        curr.execute("""
            SELECT booking_id, room_no, room_type, check_in,
                check_out, num_guests
            FROM bookings
            WHERE booking_id = ? AND status = 'CONFIRMED'
        """, (b_id,))

        return curr.fetchone()


    def fetch_tocheckout_by_id(b_id):
        curr.execute("""
            SELECT booking_id, room_no, room_type, check_in,
                check_out, num_guests, mobile_number
            FROM bookings
            WHERE booking_id = ? AND status = 'CHECKED_IN'
        """, (b_id,))

        return curr.fetchone()

    def fetch_tocheckout(mob):

        curr.execute("""SELECT booking_id, room_no, room_type, check_in, check_out, num_guests
    FROM bookings WHERE mobile_number = ? AND status = 'CHECKED_IN'
    """, (mob,))
        
        return curr.fetchall()
        

    def set_confirm(b_id):
        curr.execute(
            "UPDATE bookings SET status = 'CHECKED_IN' WHERE booking_id = ? AND status = 'CONFIRMED'",(b_id,))
        if curr.rowcount == 0:
            raise ex.InvalidStatusChangeError(
                f"Booking {b_id} cannot be checked in."
            )

        conn.commit()
        return True

    def set_checkedout(b_id):
        curr.execute("UPDATE bookings SET status = 'CHECKED_OUT' WHERE booking_id = ? AND status = 'CHECKED_IN'",(b_id, ))
        conn.commit()

        return curr.rowcount > 0

    def get_invoice(mob, check_in):
        curr.execute("""
            SELECT "current_date", room_tariff, extra_guest,breakfast_cost, day_bill, gst_amount,total_perday_bill
            FROM pricings
            WHERE mobile_number = ? AND check_in = ?
        """, (mob, check_in))

        return curr.fetchall()

    def get_netprice_invoice(mob, check_in):
        curr.execute("SELECT total_amount FROM bookings WHERE mobile_number = ? AND check_in = ?",(mob, check_in))

        return curr.fetchall()[0][0]
    
    def cancel_booking(b_id):
        today = datetime.today().date()

        curr.execute("""
            SELECT check_in, total_amount
            FROM bookings
            WHERE booking_id = ? AND status = 'CONFIRMED'
        """, (b_id,))

        row = curr.fetchone()

        if row is None:
            raise ex.BookingNotFoundError(f"Booking {b_id} was not found or cannot be cancelled.")

        check_in = datetime.strptime(row[0], "%Y-%m-%d").date()
        total_amount = row[1]
        days = (check_in - today).days

        if days >= 7:
            cancellation_fee = 0
        elif days >= 2:
            cancellation_fee = total_amount / 2
        else:
            cancellation_fee = total_amount

        curr.execute("""
            UPDATE bookings
            SET status = 'CANCELLED', cancellation_fees = ?
            WHERE booking_id = ? AND status = 'CONFIRMED'
        """, (cancellation_fee, b_id))

        conn.commit()
        return curr.rowcount > 0
    

    def fetch_booking_mob(mob):
        curr.execute("SELECT booking_id, room_no, room_type, check_in, check_out, num_guests FROM bookings WHERE mobile_number = ? ", (mob, ))
        res = curr.fetchall()
        return res

    def occupy_report(date):
        curr.execute("SELECT COUNT(*) FROM bookings WHERE ? >= check_in AND ? < check_out AND status NOT IN ('CANCELLED')",(date, date))
        num = curr.fetchone()
        return num[0]

    def get_revenue(room_type):
        curr.execute("SELECT COUNT(*), SUM(total_amount), SUM(gst_amount) FROM bookings WHERE room_type = ? AND status = 'CHECKED_OUT' ", (room_type, ))
        for row in curr.fetchall():
            print(f"From {room_type} the total completed stays are: {row[0]}, Total revenue: {row[1]}, Total GST collected: {row[2]}")
        curr.execute("SELECT SUM(cancellation_fees) FROM bookings WHERE room_type = ? AND status = 'CANCELLED' ", (room_type, ))
        print(f"Savings from cancellations are: {curr.fetchall()[0]}")

    def export_bookings():
        curr.execute("SELECT * FROM bookings")

        rows = curr.fetchall()
        headers = [column[0] for column in curr.description]

        with open("bookings_export.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(rows)

        print("Bookings exported successfully to bookings_export.csv")



except Exception as e:
    print(f"The database error occured : {e}")



