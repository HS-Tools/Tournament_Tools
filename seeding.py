import csv
import random
from statistics import mean

SIMULATION_COUNT = 1000000

mapping = {}

def read_csv(file_name, battletag_col_location, mmr_col_location):
    with open(file_name, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        #skip header
        next(reader)

        for row in reader:
            mapping[row[battletag_col_location]] = int(row[mmr_col_location])

def seed(mapping, group_num, group_size):
    assert group_num * group_size == len(mapping)

    tuple_list = [(k, v) for k, v in mapping.items()]
    
    mmr_avg = mean(mapping.values())
    closest_delta = 99999
    closest_groups = []

    for _ in range(SIMULATION_COUNT):
        total_delta = 0
        groups_list = []
        random.shuffle(tuple_list)

        start = 0
        while start < len(mapping):
            groups_list.append(tuple_list[start: start + group_size])
            start += group_size

        for group in groups_list:
            group_total = 0
            for tup in group:
                group_total = group_total +  tup[1]

            group_avg = group_total / group_size
            total_delta += abs(mmr_avg - group_avg)

        if total_delta < closest_delta:
            closest_delta = total_delta
            closest_groups = groups_list

    print(f'How far away a group was on average to the total average MMR of the competitors: {closest_delta/group_num}')
    print(printGroups(closest_groups))

def printGroups(groups_list):
    s = ''
    for index, group in enumerate(groups_list):
        s += f'Group {index + 1}: {group} \n'

    return s

read_csv('Players.csv', 2, 3)
seed(mapping, 6, 8)