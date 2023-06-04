import csv
import random
import time
import networkx as nx
import numpy as np
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

    # Distribute remaining workers randomly
    availableStations = list(range(totalStation))  # List of available stations
    random.shuffle(availableStations)  # Shuffle the station indices randomly

    # Distribute remaining workers evenly among available stations
    for i in range(remainingWorkers):
        stationIndex = availableStations[i % len(availableStations)]
        workerPerStationList[stationIndex] += 1

    # Random for the second time
    random.shuffle(workerPerStationList)

    return workerPerStationList

def calculateDummyCycleTime(listTaskTime, station):
    # Find the maximum time in list
    maxValue = listTaskTime[0][0]
    for i in range(len(listTaskTime)):
        for j in range(len(listTaskTime[0])):
            if (maxValue < listTaskTime[i][j]):
                maxValue = listTaskTime[i][j]
    val1 = (2 * maxValue) / station
    if (val1 > maxValue) :
        return val1
    else :
        return maxValue

def calculateProbabilityCumulative(globalFeromon, zAlfa, OFV, zBeta):
    arrProbability = []
    arrCumulative = []

    for i in range():
        for j in range():
            arrProbability[i][j] = ((globalFeromon**zAlfa) * ((1/OFV[i][[j]])**0.4))


    return arrProbability, arrCumulative

def checkPrecedence(precedence_diagram, listVisited):
    tasks_to_check = []

    for key, value in precedence_diagram.items():
        if all(dep in listVisited for dep in value):
            tasks_to_check.append(key)

    # Hapus elemen pada tasks to check jika element tersebut terdapat pada list visited
    tasks_to_check = [task for task in tasks_to_check if task not in listVisited]

    return tasks_to_check

def checkTimeWorker(listTask, dummyCT, listTimeData, totalWorker):
    tasks_to_check = np.empty(0, dtype=[('task', int), ('worker', int)])
    totalTime = 0

    for task in listTask:
        for i in range(totalWorker):
            print(totalTime)
            time = listTimeData[task][i]
            if (time + totalTime <= dummyCT):
                inp = (task, i+1)
                tasks_to_check = np.concatenate((tasks_to_check, np.array([inp], dtype=tasks_to_check.dtype)))
        totalTime += time

    return tasks_to_check

# ====== HELPER ======
def printInfoWorker(workerList):
    print()
    for i in range (len(workerList)):
        print("Stasiun {} ada {} pekerja".format(i+1, workerList[i]))
    print()

# Constant
Task = 9
Worker = 10
Station = 3

fileName = input("Masukkan nama file: ")
Data = read_data(fileName)

# Combine task time for 2 produk
taskTimeData = combineTaskProducts((Data))

# Assign jumlah worker ke stasiun
listWorker = assignWorkerToStation(Worker, Station)

# Tetapkan parameter
# colony = int(input("Masukkan jumlah koloni: "))
# iteration = int(input("Masukkan jumlah iterasi: "))
# globalFeromon = int(input("Masukkan jumlah global feromon: "))
# zAlfa = float(input("Masukkan nilai zAlfa: "))
# zBeta = float(input("Masukkan nilai zBeta: "))

# Alokasi Task dan Resource (Worker)
startTime = time.perf_counter()
dummyCT = calculateDummyCycleTime(taskTimeData, Station)


# Penciptaan list A dan B
firstTask = [0]
listA = checkPrecedence(tasks, firstTask)
listB = checkTimeWorker(listA, dummyCT, taskTimeData, Worker) # List B + Worker
# Tercipta di dalam looping

# # ------------------------------------BELUM MASIH DEVELOPMENT---------------------
# # Time[i] = taskTimeData[i][j]
# # OFW = waktu mulai + Time

# # for i in range (iteration):
# #     for m in range (colony):
# #         for q in range (task):
# #             # Pengisian array time
# #             Time = []
# #             for i in range ()
            
random_number = random.random()

endTime = time.perf_counter()

# ----------------------------------------------------------------------------------


# Print Hasil
for i in range (Station):
    print()
    print("========== STASIUN {} ==========".format(i+1))
    print("Task             : ")
    print("Worker         : ")
    print("Waktu model 1    : ")
    print("Waktu model 2    : ")
    print("Total waktu      : ")
    print("Cycle time       : ")

print()
print("Cycle time solusi terbaik adalah ")

print()
print("Waktu untuk run program: {} detik".format(endTime-startTime))