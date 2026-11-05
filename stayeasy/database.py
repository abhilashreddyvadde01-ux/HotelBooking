import sqlite3
import validations_functions as v
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
        booking_id TEXT PRIMARY KEY AUTOINCREMENT,
        guest_mobile TEXT REFERENCES guests(mobile),
        room_no TEXT,
        room_type TEXT,
        check_in TEXT,
        check_out TEXT,
        num_guests INTEGER,
        status TEXT,
        cancellation_fees INTEGER,
        gst_amount INTEGER,
        total_amount INTEGER)""")

    def check_availability(check_in, check_out, room_type):
        result = []
        curr.execute("""
            SELECT room_no FROM bookings
            WHERE check_in < ?
            AND check_out > ?
            AND room_type = ?
            AND status NOT IN ('CANCELLED', 'CHECKED_OUT')""", (check_out, check_in, room_type))
        
        occupied_rooms = curr.fetchall()

        for room in v.list_of_objects:
            if room.room_no not in occupied_rooms:
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


except Exception as e:
    print(f"The database error occured : {e}")



conn.close()