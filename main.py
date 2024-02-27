import random
import math
import datetime
import ru_local as ru


prices = {ru.AI80: 32, ru.AI92: 49, ru.AI95: 52, ru.AI98: 65}
sold = {ru.AI80: 0, ru.AI92: 0, ru.AI95: 0, ru.AI98: 0}


with open('initial_data.txt', 'r', encoding='utf-8') as f_data:
    stations = []
    for line in f_data:
        line = line.rstrip()
        line = line.split(' ')
        station = {'c_number': int(line[0]), 'max_queue': int(line[1]), 'petrol_types': line[2:],
                   'current_queue': 0, 'leave_time': []}

        stations.append(station)


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
                    print(f'{ru.IN} {str(datetime.time(minute//60, minute%60))[:5]} {ru.CLIENT} {past_time} '
                          f'{petrol_type} {litres} {past_operation} {ru.FUELING_DONE}.')
                    elem0["leave_time"] = elem0["leave_time"][1:]

                    for i in range(1, len(stations) + 1):
                        print(f'{ru.AUTOMAT} №{i} {ru.MAX_QUEUE}: {stations[i-1].get("max_queue")} {ru.PETROL_TYPES}: '
                              f'{" ".join(stations[i - 1].get("petrol_types"))} '
                              f'->{"*" * stations[i - 1].get("current_queue")}')

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
                    elem2['leave_time'].append([minute + operation_time, data[0][3], data[0][2],
                                                data[0][1], operation_time])
                    elem2['leave_time'].sort(key=lambda item: item[0])

            print(f'{ru.IN} {data[0][3]} {ru.NEW_CLIENT}: {data[0][3]} {data[0][2]} {data[0][1]} '
                  f'{operation_time} {ru.JOIN_QUEUE} №{column}')
            for i in range(1, len(stations) + 1):
                print(f'{ru.AUTOMAT} №{i} {ru.MAX_QUEUE}: {stations[i - 1].get("max_queue")} {ru.PETROL_TYPES}: '
                      f'{" ".join(stations[i - 1].get("petrol_types"))} ->{"*" * stations[i - 1].get("current_queue")}')

        else:
            not_satisfied += 1
            print(f'{ru.IN} {data[0][3]} {ru.NEW_CLIENT}: {data[0][3]} {data[0][2]} {data[0][1]} '
                  f'{operation_time} {ru.FUELING_NOT_DONE}')
            for i in range(1, len(stations) + 1):
                print(f'{ru.AUTOMAT} №{i} {ru.MAX_QUEUE}: {stations[i - 1].get("max_queue")} {ru.PETROL_TYPES}: '
                      f'{" ".join(stations[i - 1].get("petrol_types"))} ->{"*" * stations[i - 1].get("current_queue")}')

        if len(data) > 1:
            data = data[1:]
        else:
            break


print(f'{ru.LEFT_UNSATISFIED} - {not_satisfied}')

for p_type0 in sold:
    print(f'{ru.SOLD_FOR_TYPE} {p_type0} - {sold[p_type0]} {ru.LITRES}')

revenue = 0
for p_type in sold:
    revenue += sold[p_type] * prices[p_type]

print(f'{ru.REVENUE_PER_DAY} - {revenue}')
