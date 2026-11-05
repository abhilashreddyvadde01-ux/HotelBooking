from abc import ABC, abstractmethod

class Room(ABC):
    def __init__(self, room_no, floor):
        self.room_no = room_no
        self.floor = floor

    @abstractmethod
    def get_base_rate(self):
        pass

    @abstractmethod
    def get_max_guests(self):
        pass

    @abstractmethod
    def extra_guest_charge(self):
        pass

    @abstractmethod
    def display(self):
        pass

    @abstractmethod
    def is_breakfast_included(self):
         pass

class StandardRoom(Room):
    def __init__(self, room_no, floor):
        super().__init__(room_no, floor)
    
    def get_base_rate(self):
        return 2500

    def get_max_guests(self):
        return 2

    def is_breakfast_included(self):
         return False

    def extra_guest_charge(self):
         return 0

    def display(self):
         pass

class DeluxeRoom(Room):
    def __init__(self, room_no, floor):
        super().__init__(room_no, floor)
    
    def get_base_rate(self):
        return 4000
    
    def get_max_guests(self):
        return 3
        
    def extra_guest_charge(self):
        return 800
        
    def is_breakfast_included(self):
        return True

    def display(self):
             pass

class SuiteRoom(Room):
    def __init__(self, room_no, floor):
        super().__init__(room_no, floor)
        
    def get_base_rate(self):
            return 7500
        
    def get_max_guests(self):
            return 4
            
    def extra_guest_charge(self):
            return 800

    def is_breakfast_included(self):
         return True
            
    def display(self):
            pass

class Guest():
    def __init__(self, name, mobile, email):
        self.__name = name
        self.__mobile = mobile
        self.__email = email

 
class Booking():
    def __init__(self, booking_id, guest, room, check_in, check_out, num_guests, status, total_amount, payment):
        self.booking_id = booking_id
        self.guest = guest
        self.room = room
        self.check_in = check_in
        self.check_out = check_out
        self.num_guests = num_guests
        self.status = status
        self.total_amount = total_amount
        self.payment = payment

