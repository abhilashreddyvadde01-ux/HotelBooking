import sqlite3
import validations_functions as va
from datetime import datetime
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
        curr.execute("INSERT INTO pricings VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(mobile_number, name, email, room_no, check_in, check_out, no_of_guests, start_date, room_tariff, extra_guest, breakfast_cost, day_bill, gst_amount, total_perday_bill))
        conn.commit()

    def register_booking(mobile_number, room_no, room_type, check_in, check_out, no_of_guests, status, cancellation_fees, net_pay, net_gst):
        curr.execute("INSERT INTO bookings VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(mobile_number, room_no, room_type, check_in, check_out, no_of_guests, status, cancellation_fees, net_pay, net_gst))
        conn.commit()

    def is_loyal_customer(mobile_number):
        curr.execute("SELECT COUNT(*) FROM bookings WHERE guest_mobile = ?",(mobile_number, ))

        if int(curr.fetchall[0]) >= 3:
            return True
        else:
            return False

    def fetch_booking(mob):
        today = datetime.today().date()
        today = datetime.strptime(today, "%Y-%m-%d")
        curr.execute("SELECT booking_id, room_no, room_type, check_in, check_out, num_guests FROM bookings WHERE mobile_number = ? AND check_in >= ? AND status = 'CONFIRMED", (mob, today))
        res = curr.fetchall()
        return res

    def fetch_tocheckout(mob):
        today = datetime.today().date()
        today = datetime.strptime(today, "%Y-%m-%d")
        curr.execute("SELECT booking_id, room_no, room_type, check_in, check_out, num_guests FROM bookings WHERE mobile_number = ? AND check_in >= ? AND status = 'CHECKED-IN", (mob, today))
        res = curr.fetchall()
        return res
        

    def set_confirm(b_id):
        curr.execute("UPDATE bookings SET status = 'CHECKED-IN' WHERE booking_id = ?",(b_id, ))
        conn.commit

    def set_checkedout(b_id):
        curr.execute("UPDATE bookings SET status = 'CHECKED-OUT' WHERE booking_id = ?",(b_id, ))
        conn.commit()

    def get_invoice(mob, check_in):
        curr.execute("SELECT name, mail, room_no, no_of_guests, current_date, room_tariff, extra_guest, breakfast_cost, day_bill, gst_amount, total_perday_bill FROM pricings WHERE mobile_number = ? AND check_in = ? AND status = 'CHECKED-IN' ",(mob,check_in))
        rows = curr.fetchall()
        return rows

    def cancel_booking(mob, b_id):
        today = datetime.today().date()
        today = datetime.strptime(today, "%Y-%m-%d")
        curr.execute("SELECT check_in, total_amount FROM bookings WHERE mobile_number = ? AND booking_id = ?", (mob, b_id))
        check_in = curr.fetchall()[0]
        total_amount = curr.fetchall()[1]
        if check_in - today >= 7:
            cancellation_fee = 0
        elif check_in - today >= 2 and check_in - today <= 6:
            cancellation_fee = total_amount/2
        else:
            cancellation_fee = total_amount

        curr.execute("UPDATE bookings SET status = 'CANCELLED', cancellation_fees = ? WHERE mobile_number = ? AND booking_id = ?", (cancellation_fee, mob, b_id))

    def fetch_booking_mob(mob):
        curr.execute("SELECT booking_id, room_no, room_type, check_in, check_out, num_guests FROM bookings WHERE mobile_number = ? ", (mob, ))
        res = curr.fetchall()
        return res

    def occupy_report(date):
        curr.execute("SELECT COUNT(*) FROM bookings WHERE ? >= check_in AND ? < check_out",(date, date))
        num = curr.fetchall()[0]
        return num

    def get_revenue(room_type):
        curr.execute("SELECT COUNT(*), SUM(total_amount), SUM(gst_amount) FROM bookings WHERE room_type = ? AND status = 'CHECKED-OUT' ", (room_type, ))
        for row in curr.fetchall():
            print(f"From {room_type} the total completed stays are: {row[0]}, Total revenue: {row[1]}, Total GST collected: {row[2]}")
        curr.execute("SELECT SUM(cancellation_fees) FROM bookings WHERE room_type = ? AND status = 'CANCELLED' ", (room_type, ))
        print(f"Savings from cancellations are: {curr.fetchall()[0]}")

    def export_csv():
        bookings_csv = open("bookings.csv",'a+')
        curr.execute("SELECT * FROM bookings")
        bookings_csv.write("booking_id,mobile_number,room_no,room_type,check_in,check_out,num_guests,status,cancellation_fees,gst_amount,total_amount")
        for row in curr.fetchall():
            bookings_csv.write(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
            bookings_csv.write('\n')
        bookings_csv.close()
    conn.commit()



except Exception as e:
    print(f"The database error occured : {e}")


