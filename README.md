# StayEasy – Hotel Reservation and Billing System
Console app for a small hotel: search rooms, book, check in/out, cancel with refunds, invoices, occupancy and revenue reports.

## Requirements
- Python 3.[x], standard library only (sqlite3, csv, datetime, logging)

## Setup (Windows PowerShell)
```
python -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run
```
python main.py              # uses default database [default name]
python main.py stayeasy.db  # custom database file
```

## Features (menu)
Search availability · Create booking · Check in · Check out (invoice) · Cancel · View booking · Guest history · Occupancy report · Revenue report · Export CSV · Exit

## Project structure
[main.py + stayeasy/: models, exceptions, pricing, database, reports, menu, validations]

## Data and output files
- `rooms.csv` (room_no, room_type, floor): loaded at startup; invalid lines are skipped and logged to `app.log`
- `invoices/BKxxxx.txt`: created on check-out (folder auto-created)
- `bookings_export.csv`: output of the export option

## Business rules
Room rates and guest limits, Fri/Sat +20%, ₹800 per extra guest (Deluxe/Suite), 7+ nights 10% off, loyalty 5%, GST 12%/18%, refund 100% / 50% / 0%, status flow CONFIRMED → CHECKED_IN → CHECKED_OUT, CONFIRMED → CANCELLED
