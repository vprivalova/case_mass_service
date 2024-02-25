import random
import math
import datetime


prices = {'АИ-80': 32, 'АИ-92': 49, 'АИ-95': 52, 'АИ-98': 65}
sold = {'АИ-80': 0, 'АИ-92': 0, 'АИ-95': 0, 'АИ-98': 0}


with open('initial_data.txt', 'r', encoding='utf-8') as f_data:
    stations = []
    for line in f_data:
        line = line.rstrip()
        line = line.split(' ')
        station = {'c_number': int(line[0]), 'max_queue': int(line[1]), 'petrol_types': line[2:], 'current_queue': 0, 'leave_time': []}

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
    for elem0 in stations:
        if len(elem0.get('leave_time')) > 0:
            if minute == (elem0.get('leave_time'))[0][0]:
                counter = 0
                for j in range(len(elem0.get('leave_time'))):
                    if elem0.get('leave_time')[j][0] == minute:
                        counter += 1
                for n in range(counter):
                    elem0['current_queue'] -= 1
                    past_time = (elem0.get("leave_time"))[0][1]
                    petrol_type = (elem0.get("leave_time"))[0][2]

                    litres = (elem0.get("leave_time"))[0][3]
                    sold[petrol_type] += litres

                    past_operation = (elem0.get("leave_time"))[0][4]
                    print(f'В {str(datetime.time(minute//60, minute%60))[:5]} клиент {past_time} {petrol_type} {litres} {past_operation} заправил свой автомобиль и покинул АЗС.')
                    elem0["leave_time"] = elem0["leave_time"][1:]

                    for i in range(1, len(stations) + 1):
                        print(f'Автомат №{i} максимальная очередь: {stations[i - 1].get("max_queue")} Марки бензина: '
                              f'{" ".join(stations[i - 1].get("petrol_types"))} ->{"*" * stations[i - 1].get("current_queue")}')

    if minute == data[0][0]:

        possible_options = []
        for elem in stations:
            if data[0][2] in elem.get('petrol_types'):
                if elem.get('current_queue') < elem.get('max_queue'):
                    possible_options.append([elem.get('c_number'), elem.get('current_queue')])

        if len(possible_options) > 0:
            result_option = sorted(possible_options, key=lambda item: item[1])[0]
            column = result_option[0]

            operation_time = math.ceil(data[0][1] / 10)

            addition = random.randint(-1, 1)

            if operation_time + addition > 0:
                operation_time = operation_time + addition

            for elem2 in stations:
                if elem2.get('c_number') == column:
                    elem2['current_queue'] += 1
                    elem2['leave_time'].append([minute + operation_time, data[0][3], data[0][2], data[0][1], operation_time])
                    elem2['leave_time'].sort(key=lambda item: item[0])



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



print(f'Уехавших недовольных - {not_satisfied}')

for p_type0 in sold:
    print(f'Продано за сутки по марке {p_type0} - {sold[p_type0]} литров')

revenue = 0
for p_type in sold:
    revenue += sold[p_type] * prices[p_type]

print(f'Общая сумма продаж за день - {revenue}')