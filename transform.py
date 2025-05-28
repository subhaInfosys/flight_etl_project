
def transform_data(raw_data):
    transformed = []
    for flight in raw_data:
        transformed.append({
            'airline': flight['airline']['name'],
            'flight_number': flight['flight']['number'],
            'departure_airport': flight['departure']['airport'],
            'arrival_airport': flight['arrival']['airport'],
            'departure_time': flight['departure']['scheduled'],
            'arrival_time': flight['arrival']['scheduled'],
            'status': flight['flight_status']
        })
    return transformed
