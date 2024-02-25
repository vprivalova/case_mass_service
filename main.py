import random
import math


prices = {'АИ-80': 32, 'АИ-92': 49, 'АИ-95': 52, 'АИ-98': 65}


with open('initial_data.txt', 'r', encoding='utf-8') as f_data:
    stations = []
    for line in f_data:
        line = line.rstrip()
        line = line.split(' ')
        station = {'c_number': int(line[0]), 'max_queue': int(line[1]), 'petrol_types': line[2:], 'current_queue': 0}
        stations.append(station)

print(stations)

with open('input.txt', 'r', encoding='utf-8') as f_cars:
    data = []
    for line1 in f_cars:
        line1 = line1.rstrip().split(' ')
        time_table = line1[0]
        time = line1[0].split(':')
        hour = int(time[0])
        minute = int(time[1])
        line1[0] = hour * 60 + minute
        line1[1] = int(line1[1])
        line1.append(time_table)
        data.append(line1)

print(data)

not_satisfied = 0

for minute in range(1441):
    if minute == data[0][0]:

        possible_options = []
        for elem in stations:
            if data[0][2] in elem.get('petrol_types'):
                if elem.get('current_queue') < elem.get('max_queue'):
                    possible_options.append([elem.get('c_number'), elem.get('current_queue')])

        if len(possible_options) > 0:
            result_option = sorted(possible_options, key=lambda item: item[1])[0]
            column = result_option[0]

            for elem2 in stations:
                if elem2.get('c_number') == column:
                    elem2['current_queue'] += 1

            operation_time = math.ceil(data[0][1] / 10)

            addition = random.randint(-1, 1)

            if operation_time + addition > 0:
                operation_time = operation_time + addition

            print(f'В {data[0][3]} новый клиент: {data[0][3]} {data[0][2]} {data[0][1]} '
                  f'{operation_time} встал в очередь к автомату №{column}')
            for i in range(1, len(stations) + 1):
                print(f'Автомат №{i} максимальная очередь: {stations[i - 1].get("max_queue")} Марки бензина: '
                      f'{" ".join(stations[i - 1].get("petrol_types"))} ->{"*" * stations[i - 1].get("current_queue")}')

        else:
            not_satisfied += 1
            print(f'В {data[0][3]} новый клиент: {data[0][3]} {data[0][2]} {data[0][1]} '
                  f'{operation_time} не смог заправить автомобиль и покинул АЗС')
            for i in range(1, len(stations) + 1):
                print(f'Автомат №{i} максимальная очередь: {stations[i - 1].get("max_queue")} Марки бензина: '
                      f'{" ".join(stations[i - 1].get("petrol_types"))} ->{"*" * stations[i - 1].get("current_queue")}')

        if len(data) > 1:
            data = data[1:]
        else:
            break




