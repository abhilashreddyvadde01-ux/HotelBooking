import database as db
from datetime import timedelta
def get_pricing(mobile_number, name, email, room_no,  check_in, check_out, no_of_guests, room_type, is_loyal_customer, breakfast_extra, cancellation_fees, status):
    net_pay = 0
    net_gst = 0
    start_date = check_in
    end_date = check_out

    while start_date < end_date:
        room_tariff = 0
        extra_guest = 0
        breakfast_cost = 0
        day_bill = 0
        gst_amount = 0
        total_perday_bill = 0
        day_name = start_date.strftime("%A")
        if room_type == 'Standard':
            room_tariff += 2500
        if room_type == 'Deluxe':
            room_tariff += 4000
        if room_type == 'Suite':
            room_tariff += 7500
        if no_of_guests > 2:
            extra_guest += (no_of_guests-2)*800 
        if day_name in ['Friday', 'Saturday']:
            room_tariff = room_tariff*1.2
        if breakfast_extra:
            breakfast_cost = 350* no_of_guests
        else:
            breakfast_cost = 0
        day_bill = room_tariff + extra_guest + breakfast_cost
        if day_bill <= 7500:
            gst_amount = day_bill * 1.12
        else:
            gst_amount = day_bill * 1.18
        total_perday_bill = day_bill + gst_amount
        net_gst += gst_amount 
        net_pay += total_perday_bill
        db.register_pricings(mobile_number, name, email, room_no, check_in, check_out, no_of_guests, start_date, room_tariff, extra_guest, breakfast_cost, day_bill, gst_amount, total_perday_bill)
        start_date += timedelta(days=1)

    if check_out - check_in > 7:
        net_pay = net_pay * 0.9
    if is_loyal_customer:
        net_pay = net_pay * 0.95

    db.register_booking(mobile_number, room_no, room_type, check_in, check_out, no_of_guests, status, cancellation_fees, net_pay, net_gst)
    print("Booking confirmed ")
    print(f"The net payable amount is : {net_pay}")

    

            
