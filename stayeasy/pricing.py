
import database as db
from datetime import timedelta
import models as m

def get_pricing(mobile_number, name, email, room_no, check_in, check_out, no_of_guests, room_type, is_loyal_customer, breakfast_extra, cancellation_fees, status):
    net_pay = 0
    net_gst = 0
    room_total = 0
    start_date = check_in
    end_date = check_out

    if room_type == 'Standard':
        room_obj = m.StandardRoom(room_no, 0, room_type)
    elif room_type == 'Deluxe':
        room_obj = m.DeluxeRoom(room_no, 0, room_type)
    elif room_type == 'Suite':
        room_obj = m.SuiteRoom(room_no, 0, room_type)

    
    base_rate = room_obj.get_base_rate()
    extra_guest_rate = room_obj.extra_guest_charge()

    while start_date < end_date:
        room_tariff = base_rate
        extra_guest = 0
        breakfast_cost = 0
        day_bill = 0
        gst_amount = 0
        total_perday_bill = 0

        day_name = start_date.strftime("%A")

        if no_of_guests > 2:
            extra_guest = (no_of_guests - 2) * extra_guest_rate
        if day_name in ['Friday', 'Saturday']:
            room_tariff = room_tariff * 1.2
        if breakfast_extra:
            breakfast_cost = 350 * no_of_guests
        day_bill = room_tariff + extra_guest + breakfast_cost

        if room_tariff <= 7500:
            gst_amount = day_bill * 0.12
        else:
            gst_amount = day_bill * 0.18

        total_perday_bill = day_bill + gst_amount

        room_total += room_tariff
        net_gst += gst_amount
        net_pay += total_perday_bill

        db.register_pricings(
            mobile_number, name, email, room_no, check_in, check_out,
            no_of_guests, start_date, room_tariff, extra_guest,
            breakfast_cost, day_bill, gst_amount, total_perday_bill
        )

        start_date += timedelta(days=1)

    discount = 0

    if (check_out - check_in).days >= 7:
        discount = room_total * 0.10

    discounted_room_total = room_total - discount

    if is_loyal_customer:
        loyalty_discount = discounted_room_total * 0.05
        discount += loyalty_discount

    net_pay = net_pay - discount
    net_pay = round(net_pay, 2)
    net_gst = round(net_gst, 2)

    db.register_booking(
        mobile_number, room_no, room_type, check_in, check_out,
        no_of_guests, status, cancellation_fees, net_pay, net_gst
    )

    print("Booking confirmed ")
    print(f"The net payable amount is : {net_pay}")
