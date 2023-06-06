import csv
import random
import time
import numpy as np

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
}

# ========== READ DATA FROM CSV ==========
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

# ========== FUNCTIONS ==========
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

def checkPrecedence(precedence_diagram, listVisited):
    tasks_to_check = []

    for key, value in precedence_diagram.items():
        if all(dep in listVisited for dep in value):
            tasks_to_check.append(key)

    # Hapus elemen pada tasks to check jika element tersebut terdapat pada list visited
    tasks_to_check = [task for task in tasks_to_check if task not in listVisited]

    return tasks_to_check

def checkTimeWorker(listTask, dummyCT, listTimeData, totalWorker, visitedStation1, station2, station3, listWorker):
    tasks_to_check = np.empty(0, dtype=[('task', int), ('worker', int)])

    for task in listTask:
        for i in range(totalWorker):
            time = listTimeData[task][i]
            if time <= dummyCT:
                inp = (task, i+1)
                tasks_to_check = np.concatenate((tasks_to_check, np.array([inp], dtype=tasks_to_check.dtype)))

    if len(visitedStation1) >= listWorker[0]:
        valid_workers = [worker[1] for worker in visitedStation1]
        tasks_to_check = np.array([task for task in tasks_to_check if task[1] in valid_workers], dtype=tasks_to_check.dtype)

    return tasks_to_check



# def updateListB(listB, chosenTask):
#     updatedListB = []
#     for item in listB:
#         if (item[0] != chosenTask) :
#             updatedListB.append(item)
#     return updatedListB

def calculateUpperProbability(gf, zAlpha, zBeta, OFV):
    upper = (gf**zAlpha)*((1/OFV)**zBeta)
    return upper

def chooseProbability(random, listData):
    min_diff = 1
    chosen = None
    for item in listData:
        if (abs(item[3] - random) < min_diff):
            min_diff = abs(item[3] - random)
            chosen = item[0]
    time = item[1]
    return chosen, time

def calculateOFV(listB, taskTimeData, sumTime):
    OFV = []
    for taskTime in listB:
        currTime = taskTimeData[taskTime[0] - 1][taskTime[1] - 1] + sumTime
        OFV.append(currTime)
    return OFV

def calculateProb(listB, globalFeromon, zAlfa, zBeta):
    tempProb = []
    sumUpperProbability = 0.0
    for i in range(len(listB)):
        x = calculateUpperProbability(globalFeromon, zAlfa, zBeta, OFV[i])
        x = round(x, 4)
        tempProb.append(x)
        sumUpperProbability += x
    Prob = []
    for i in range(len(listB)):
        x = tempProb[i]/sumUpperProbability
        x = round(x, 4)
        Prob.append(x)
    return Prob

def calculateCumulative(Prob):
    Cumulative = []
    Cumulative.append(Prob[0])
    for i in range(1, len(listB)):
        tempCumulative = Cumulative[i-1] + Prob[i]
        Cumulative.append(tempCumulative)
    return Cumulative

def saveData(listB, OFV, Prob, Cumulative):
    Data_ = []
    for i in range(len(listB)):
        Data_.append((listB[i],OFV[i], Prob[i], Cumulative[i]))
    return Data_

def chooseProbability(random, listData):
    minDiff = 1
    chosen = None
    for data in listData:
        diff = abs(data[3] - random)
        if diff < minDiff:
            minDiff = diff
            chosen = data
    return chosen[0], chosen[1]

def updateData(listData, chosenTask, chosenWorker, time):
    updatedData = []
    for data in listData :
        check = data[0]
        if (check[0] != chosenTask) :
            if (check[1] == chosenWorker) :
                newOFV = data[1] + time
            else :
                newOFV = data[1]
            updatedData.append((check, newOFV, data[2], data[3]))
    return updatedData

def updateTaskTimeData(listTaskTime, chosenWorker, time):
    for i in range(len(listTaskTime)):
        for j in range(len(listTaskTime[0])):
            if (j == chosenWorker - 1):
                listTaskTime[i][j] += time

def checkStation(Station1, Station2, Station3, listWorker):
    result = 0
    if (len(Station1) < listWorker[0]):
        result = 1
    elif (len(Station2) < listWorker[1]):
        result = 2
    elif (len(Station3) < listWorker[2]):
        result = 3
    return result



# ========== HELPER ==========
def printInfoWorker(workerList):
    print()
    for i in range (len(workerList)):
        print("Stasiun {} ada {} pekerja".format(i+1, workerList[i]))
    print()

# Constant
nTask = 9
nWorker = 5
nStation = 3

fileName = input("Masukkan nama file: ")
Data = read_data(fileName)

# Combine task time for 2 produk
taskTimeData = combineTaskProducts((Data))

# Assign jumlah worker ke stasiun
listWorker = assignWorkerToStation(nWorker, nStation)
nMaxStation1 = listWorker[0]
nMaxStation2 = listWorker[1]
nMaxStation3 = listWorker[2]

# Tetapkan parameter
colony = int(input("Masukkan jumlah koloni: "))
iteration = int(input("Masukkan jumlah iterasi: "))
globalFeromon = float(input("Masukkan jumlah global feromon: "))
zAlfa = float(input("Masukkan nilai zAlfa: "))
zBeta = float(input("Masukkan nilai zBeta: "))

# Alokasi Task dan Resource (Worker)
startTime = time.perf_counter()
dummyCT = calculateDummyCycleTime(taskTimeData, nStation)
# print("Dummy CT :", dummyCT)


# Penciptaan list A dan B
firstTask = [0]

# # ------------------------------------BELUM MASIH DEVELOPMENT---------------------
# List Station 1, 2, 3
Station1 = []
Station2 = []
Station3 = []

# --- update
temp = []
for i in range (iteration):
    for m in range (colony):
        sumTime = 0
        index = 0
        randd = [0.453395713412637, 0.491498467321415, 0.846804777745682, 0.619367348176098, 0.297167465811096, 0.110205474800908, 0.43164295906485, 0.86541927053779, 0.748261254604284]
        listA = checkPrecedence(tasks, firstTask)
        print("List A : ", end="")
        print(listA)
        listB = checkTimeWorker(listA, dummyCT, taskTimeData, nWorker, Station1, Station2, Station3, listWorker) # List B + Worker
        print("List B : ", end="")
        print(listB)

        # Calculating OFV
        OFV = calculateOFV(listB, taskTimeData, sumTime)

        # Calculating prob
        Prob = calculateProb(listB, globalFeromon, zAlfa, zBeta)

        # Calculating cumulative
        Cumulative = calculateCumulative(Prob)

        # Saving Data
        Data_ = saveData(listB, OFV, Prob, Cumulative)
        for q in range (nTask):
            copyTaskTime = taskTimeData
            print("=============================================")
            print("\nData: ", end="")
            print(Data_)
            print(len(Data_))
            # random_decimal = random.random()
            random_decimal = randd[index]
            print("\nRandom desimal: ", end="")
            print(random_decimal)
            chosen, tempTime = chooseProbability(random_decimal, Data_)
            print("Yang terpilih: ", end="")
            print(chosen)
            chosenTask = chosen[0]
            chosenWorker = chosen[1]
            firstTask.append(chosenTask)
            Station1.append((chosenTask, chosenWorker, tempTime))

            # Update listA
            listA = checkPrecedence(tasks, firstTask)
            print("Update List A : ", end="")
            print(listA)

            # Update listB
            updateTaskTimeData(copyTaskTime, chosenWorker, tempTime)
            listB = checkTimeWorker(listA, dummyCT, copyTaskTime, nWorker, Station1, Station2, Station3, listWorker)
            print("Update List B : ", end="")
            print(listB)
            Data_ = updateData(Data_, chosenTask, chosenWorker, tempTime)
            print("Update Data: ")
            print(Data_)

            # Update OFV
            OFV = calculateOFV(listB, copyTaskTime, sumTime)

            # Update Prob
            Prob = calculateProb(listB, globalFeromon, zAlfa, zBeta)

            # Update Cumulative
            Cumulative = calculateCumulative(Prob)

            # Update Data
            # Data_ = saveData(listB, OFV, Prob, Cumulative)

            index += 1

print("\nStation: ")
print(Station1)
print(Station2)
print(Station3)
# ---
rute = np.zeros((colony, nTask))
print(rute)

pheromone = globalFeromon*np.ones((nTask, nTask))
print(pheromone)

random_number = random.random()

endTime = time.perf_counter()

# ----------------------------------------------------------------------------------


# Print Hasil
for i in range (nStation):
    print()
    print("========== STASIUN {} ==========".format(i+1))
    print("Task             : ")
    print("Worker           : ")
    print("Waktu model 1    : ")
    print("Waktu model 2    : ")
    print("Total waktu      : ")
    print("Cycle time       : ")

print()
print("Cycle time solusi terbaik adalah ")

print()
print("Waktu untuk run program: {} detik".format(endTime-startTime))