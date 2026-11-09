# StayEasy – Hotel Reservation and Billing System

A console application for a small hotel's front desk. It searches room availability, takes bookings, checks guests in and out, handles cancellations with refunds, writes invoices, and reports occupancy and revenue. Rooms are loaded from a CSV file; guests and bookings are stored in a SQLite database so data is kept between runs.

## Requirements
- Python 3.8 or newer
- Standard library only (sqlite3, csv, datetime, abc). There are no packages to install.

## Setup

Windows PowerShell:
```powershell
python -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run
From the project root:
```
python stayeasy/menu.py
```
`menu.py` is the starting point. On startup the app switches to the `stayeasy/` folder, so it works from any location and all of its data files are created there.

## Menu
| # | Option | What it does |
|---|--------|--------------|
| 1 | Search room availability | Asks for room type, guests and dates, then allocates the lowest-numbered free room |
| 2 | Create booking | Takes guest details for the room found in option 1 and confirms the booking |
| 3 | Check in | Checks a guest in on their check-in date |
| 4 | Check out | Checks a guest out and writes a text invoice |
| 5 | Cancel booking | Cancels a confirmed booking and applies the refund rules |
| 6 | View booking details | Shows a guest's upcoming confirmed bookings |
| 7 | Guest stay history | Lists all bookings for a mobile number |
| 8 | Occupancy report | Rooms occupied per night and average occupancy for a date range |
| 9 | Revenue report | Completed stays, revenue, GST collected and cancellation income per room type |
| 10 | Export all bookings to CSV | Writes every booking to `bookings.csv` |
| 11 | Exit | Quits the program |

Dates are entered as `YYYY-MM-DD`. Search for availability (option 1) before creating a booking (option 2).

## Room types and rates
| Room type | Rate per night | Max guests | Breakfast |
|-----------|----------------|------------|-----------|
| Standard | ₹2,500 | 2 | Optional, ₹350 per guest per night |
| Deluxe | ₹4,000 | 3 | Included |
| Suite | ₹7,500 | 4 | Included |

## Business rules
- **Stay:** 1 to 30 nights. Check-in cannot be in the past or more than 180 days ahead. A room can be booked from the day another guest checks out.
- **Availability:** a room is blocked by any active booking that overlaps a night of the stay. Cancelled and checked-out bookings do not block a room.
- **Pricing:** Friday and Saturday nights are charged at the base rate + 20%. Deluxe and Suite rooms charge ₹800 per night for each guest beyond 2.
- **Discounts:** stays of 7 nights or more get 10% off room charges. Returning guests with 3 or more completed stays get 5% off.
- **GST:** 12% for nights where the room tariff is ₹7,500 or less, 18% above that.
- **Guests:** name, 10-digit mobile number starting with 6, 7, 8 or 9, email address, and number of guests. The mobile number identifies a returning guest.
- **Booking status:** a new booking is CONFIRMED. CONFIRMED can change to CHECKED_IN (on the check-in date) or CANCELLED. CHECKED_IN can change to CHECKED_OUT. Any other change is rejected.
- **Cancellation refund:** 7 or more days before check-in: 100%. 2 to 6 days: 50%. Less than 2 days: no refund.

### Worked example
Deluxe room, 3 guests, Thursday to Monday (4 nights):

| Night | Room tariff | Extra guest |
|-------|-------------|-------------|
| Thursday | ₹4,000 | ₹800 |
| Friday | ₹4,800 | ₹800 |
| Saturday | ₹4,800 | ₹800 |
| Sunday | ₹4,000 | ₹800 |

Room charges ₹17,600 + extra guest ₹3,200 = ₹20,800. GST at 12% = ₹2,496. **Total: ₹23,296.** Cancelled 5 days before check-in, the refund is ₹11,648.

## Project structure
```
HotelBooking/
├── README.md
├── requirements.txt
└── stayeasy/
    ├── __init__.py
    ├── menu.py                     # entry point and menu loop
    ├── models.py                   # abstract Room with Standard, Deluxe and Suite rooms; Guest; Booking
    ├── exceptions.py               # custom exceptions
    ├── pricing.py                  # nightly pricing, discounts and GST
    ├── database.py                 # SQLite access (guests, bookings, nightly pricing)
    ├── validations_functions.py    # input validation and booking workflow
    └── rooms.csv                   # room list loaded at startup
```

## Data and output files
All of these are created inside the `stayeasy/` folder:
- `rooms.csv` (input): columns `room_no room_type floor`, one room per line after a header line. Lines with an unknown room type are skipped and logged.
- `stayeasy.db`: SQLite database holding guests, bookings and nightly charges.
- `app.log`: reasons for rooms skipped while loading `rooms.csv`.
- `<booking_id>.txt`: text invoice written at check-out, with the night-by-night breakdown and net payable amount.
- `bookings.csv`: output of the export option.