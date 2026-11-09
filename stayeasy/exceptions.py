
class HotelException(Exception):
    pass


class InvalidDateError(HotelException):
    pass


class RoomUnavailableError(HotelException):
    pass


class InvalidStatusChangeError(HotelException):
    pass


class BookingNotFoundError(HotelException):
    pass