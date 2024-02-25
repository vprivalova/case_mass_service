import random

prices = {'АИ-80': 32, 'АИ-92': 49, 'АИ-95': 52, 'АИ-98': 65}


with open('initial_data.txt', 'r', encoding='utf-8') as f_data:
    stations = []
    for line in f_data:
        line = line.rstrip()
        line = line.split(' ')
        station = {'c_number': int(line[0]), 'max_queue': int(line[1]), 'petrol_types': line[2:], 'current_queue': 0}
        stations.append(station)

print(stations)

with open('input.txt', 'r') as f_cars:
    hour = 0
    minute = 0
    liters = 0
    for minutes in range(1441):


