prices = {'АИ-80': 32, 'АИ-92': 49, 'АИ-95': 52, 'АИ-98': 65}


with open('initial_data.txt', 'r', encoding='utf-8') as f_data:
    stations = []
    for line in f_data:
        line = line.rstrip()
        line = line.split(' ')
        station = {'c_number': line[0], 'max_queue': line[1], 'petrol_types': line[2:]}
        stations.append(station)

print(stations)

#with open('input.txt', 'r') as f_:

