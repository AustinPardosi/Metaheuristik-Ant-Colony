import csv
import random
import time
import networkx as nx
import matplotlib.pyplot as plt

tasks = {
    0: [],
    1: [0],
    2: [0],
    3: [0],
    4: [0],
    5: [1, 2, 3, 4],
    6: [5],
    7: [5],
    8: [6, 7],
    9: [8],
    10: [9],
    11: [10],
    12: [11],
    13: [12],
    14: [0],
    15: [14],
    16: [15],
    17: [16],
    18: [17],
    19: [0],
    20: [18, 19],
    21: [20],
    22: [21],
    23: [21],
    24: [22, 23],
    25: [0],
    26: [24, 25],
    27: [26],
    28: [27],
    29: [28],
    30: [29],
    31: [24],
    32: [31],
    33: [32],
    34: [32],
    35: [33, 34],
    36: [35],
    37: [30, 36],
    38: [37],
    39: [38],
    40: [39],
    41: [40],
    42: [13, 41],
    43: [42],
    44: [42],
    45: [43, 44],
    46: [45],
    47: [46],
    48: [47],
    49: [48],
    50: [49],
    51: [50],
    52: [51],
    53: [50],
    54: [50],
    55: [53, 54],
    56: [55],
    57: [56],
    58: [56],
    59: [56],
    60: [56],
    61: [0],
    62: [57, 58, 59, 60],
    63: [0],
    64: [56, 61, 63],
    65: [52, 64],
    66: [65],
    67: [62],
    68: [67, 69],
    69: [66],
    70: [68],
    71: [70],
    72: [68],
    73: [68],
    74: [68],
    75: [68],
    76: [68],
    77: [68],
    78: [71, 72, 73, 74, 75, 76, 77],
    79: [78],
}

# Create a directed graph
graph = nx.DiGraph()

# Add nodes for each task
for task in tasks:
    graph.add_node(task)

# Add edges for task dependency
for task, dependencies in tasks.items():
    for dependency in dependencies:
        graph.add_edge(dependency, task)

def read_data(filename):
    data = []

    with open(filename, 'r') as file:
        reader = csv.reader(file)
        # Skip first row
        next(reader)
        for row in reader:
            # Skip first column
            row_data = row[1:]
            data.append(row_data)
    return data

def combineTaskProducts(listTask):
    rows = len(listTask) // 2
    cols = len(listTask[0])
    result = [[0] * cols for i in range(rows)]

    for i in range(rows):
        for j in range(cols):
            result[i][j] = round((100/150) * float(listTask[2*i][j]) + (50/150) * float(listTask[2*i+1][j]), 2)
    
    return result

def assignWorkerToStation(totalWorker, totalStation):
    # Initialize the workerPerStationList
    if totalWorker >= totalStation:
        workerPerStationList = [totalWorker // totalStation] * totalStation
        remainingWorkers = totalWorker % totalStation
    else:
        workerPerStationList = [0] * totalStation
        remainingWorkers = totalWorker

    # Distribute remaining workers random but even
    for i in range(remainingWorkers):
        randomInt = random.randint(0, totalStation - 1)
        workerPerStationList[randomInt] += 1

    return workerPerStationList

def printInfoWorker(workerList):
    print()
    for i in range (len(workerList)):
        print("Stasiun {} ada {} pekerja".format(i+1, workerList[i]))
    print()

# Constant
Task = 9
Worker = 5
Station = 3

fileName = input("Masukkan nama file: ")
Data = read_data(fileName)

# Combine task time for 2 produk
taskTimeData = combineTaskProducts((Data))

# Assign jumlah worker ke stasiun
listWorker = assignWorkerToStation(Worker, Station)


# Tetapkan parameter
colony = int(input("Masukkan jumlah koloni: "))
iteration = int(input("Masukkan jumlah iterasi: "))
globalFeromon = int(input("Masukkan jumlah global feromon: "))
zAlpha = 0.7
zBeta = 0.4

# printInfoWorker(listWorker)
# Alokasi Task dan Resource
startTime = time.perf_counter()
# -- Process


endTime = time.perf_counter()


# Print Hasil
for i in range (Station):
    print()
    print("========== STASIUN {} ==========".format(i+1))
    print("Task             : ")
    print("Resource         : ")
    print("Waktu model 1    : ")
    print("Waktu model 2    : ")
    print("Total waktu      : ")
    print("Cycle time       : ")

print()
print("Cycle time solusi terbaik adalah ")
print("Biaya total solusi terbaik adalah USD ")

print()
print("Waktu untuk run program: {} detik".format(endTime-startTime))