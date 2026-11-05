def get_pricing(start_date, end_date, no_of_guests, room_type, is_loyal_customer, breakfast_extra):
    net_price = 0
    date_wise_bills = {}


    while start_date < end_date:
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
        

            
