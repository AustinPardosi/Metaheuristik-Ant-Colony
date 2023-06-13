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

def checkPrecedence(precedence_diagram, listVisited, posVisitTask):
    tasks_to_check = []
    newAddedTask = []

    for key, value in precedence_diagram.items():
        if all(dep in listVisited for dep in value):
            tasks_to_check.append(key)

    # Hapus elemen pada tasks to check jika element tersebut terdapat pada list visited
    tasks_to_check = [task for task in tasks_to_check if task not in listVisited]

    # newAddedTask adalah list yang berasal dari tasks_to_check yang tidak ada di posVisitTask
    newAddedTask = [task for task in tasks_to_check if task not in posVisitTask]
    for i in range(len(newAddedTask)):
        posVisitTask.append(newAddedTask[i])
    
    return tasks_to_check, newAddedTask


def checkTimeWorker(listTask, dummyCT, listTimeData, totalWorker, visitedStation, listWorker, restrictedList, idxStation):
    tasks_to_check = np.empty(0, dtype=[('task', int), ('worker', int)])
    result = np.empty(0, dtype=[('task', int), ('worker', int)])

    for task in listTask:
        for i in range(totalWorker):
            time = listTimeData[task-1][i]
            if time <= dummyCT:
                inp = (task, i+1)
                tasks_to_check = np.concatenate((tasks_to_check, np.array([inp], dtype=tasks_to_check.dtype)))

    # print("Panjang list Station = ", end="")
    # print(len(visitedStation))
    # print("Max : ", end="")
    # print(listWorker[idxStation])
    if len(visitedStation) >= listWorker[idxStation]:
        valid_workers = [worker[1] for worker in visitedStation]
        tasks_to_check = np.array([task for task in tasks_to_check if task[1] in valid_workers], dtype=tasks_to_check.dtype)

    for task in tasks_to_check:
        if task[1] not in restrictedList:
            result = np.append(result, task)

    return result

def calculateUpperProbability(zAlpha, zBeta, OFV, q, pheromone_matrices, idxWorker, idxTask):
    for i, pheromone in enumerate(pheromone_matrices):
        if (i == idxWorker):
            x = pheromone[idxTask][q]
    upper = (x**zAlpha)*((1/OFV)**zBeta)
    return upper

def calculateOFV(listB, taskTimeData):
    OFV = []
    for taskTime in listB:
        currTime = taskTimeData[taskTime[0] - 1][taskTime[1] - 1] 
        OFV.append(currTime)
    return OFV

def calculateProb(listB, zAlfa, zBeta, q, pheromone_matrices):
    tempProb = []
    sumUpperProbability = 0.0
    for i, data in enumerate(listB):
        idxWorker = data[1]-1
        idxTask = data[0]-1
        x = calculateUpperProbability(zAlfa, zBeta, OFV[i], q, pheromone_matrices, idxWorker, idxTask)
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
        x = Cumulative[i-1] + Prob[i]
        tempCumulative = round(x, 4)
        Cumulative.append(tempCumulative)
    return Cumulative

def saveData(listB, OFV, Prob, Cumulative):
    Data_ = []
    for i in range(len(listB)):
        Data_.append((listB[i],OFV[i], Prob[i], Cumulative[i]))
    return Data_

def chooseProbability(random, listData):
    chosen = None
    for data in listData:
        diff = random - data[3]
        chosen = data
        if diff < 0:
            break
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

def updateTaskTimeData(listTaskTime, chosenTask, chosenWorker, addTime, time, taskTimeData, newAddedTask):
    for i in range(len(listTaskTime)):
        for j in range(len(listTaskTime[0])):
            if (len(newAddedTask) != 0) :
                for k in range(len(newAddedTask)):
                    if ((i == newAddedTask[k] - 1)):
                        listTaskTime[i][j] = round(taskTimeData[i][j],2) + addTime
            else:
                if j == chosenWorker - 1:
                    listTaskTime[i][j] = round(taskTimeData[i][j],2) + time
    return listTaskTime

def searchConditionList(list_of_tasks, tasks):
    conditionList = set()
    for task in list_of_tasks:
        if task in tasks:
            conditionList.update(tasks[task])
    return list(conditionList)

def searchMaxTime(currStation, conditionList):
    max = 0
    for info in currStation:
        if ((info[0] in conditionList) and (info[2] > max)):
            max = info[2]
    return max

def restrictedWorker(listStation, currIdxStation):
    restricted = set()
    for i in range(currIdxStation):
        for data in listStation[i]:
            x = data[1]
            restricted.add(x)
    return list(restricted)

def check_requirements(tasks, task_id, task_list):
    requirements = tasks[task_id]
    for requirement in requirements:
        if requirement not in task_list:
            return False
    return True

def searchAddTime(currStation, listA, tasks):
    addTime = 0
    if (len(listA) > 0):
        visitedTask = []
        for stat in currStation:
            x = stat[0]
            visitedTask.append(x)
        # print("Visited Task = ", end="")
        # print(visitedTask)
        check = check_requirements(tasks, listA[0], visitedTask)
        # print(check)
        if (check):
            for stat in currStation:
                if (addTime < stat[2]):
                    addTime = stat[2]
    return addTime
            
# ========== HELPER ==========
def printInfoWorker(workerList):
    print()
    for i in range (len(workerList)):
        print("Stasiun {} ada {} pekerja".format(i+1, workerList[i]))
    print()

# Constant
nTask = 78
nWorker = 41
nStation = 16

fileName = input("Masukkan nama file: ")
Data = read_data(fileName)

# Combine task time for 2 produk
taskTimeData = combineTaskProducts((Data))

# Assign jumlah worker ke stasiun
listWorker = assignWorkerToStation(nWorker, nStation)
# listWorker = [2,1,2]
nMaxStation1 = listWorker[0]
nMaxStation2 = listWorker[1]
nMaxStation3 = listWorker[2]
nMaxStation4 = listWorker[3]
nMaxStation5 = listWorker[4]
nMaxStation6 = listWorker[5]
nMaxStation7 = listWorker[6]
nMaxStation8 = listWorker[7]
nMaxStation9 = listWorker[8]
nMaxStation10 = listWorker[9]
nMaxStation11 = listWorker[10]
nMaxStation12 = listWorker[11]
nMaxStation13 = listWorker[12]
nMaxStation14 = listWorker[13]
nMaxStation15 = listWorker[14]
nMaxStation16 = listWorker[15]

# Tetapkan parameter
colony = int(input("Masukkan jumlah koloni: "))
iteration = int(input("Masukkan jumlah iterasi: "))
globalFeromon = float(input("Masukkan jumlah global feromon: "))
zAlfa = float(input("Masukkan nilai zAlfa: "))
zBeta = float(input("Masukkan nilai zBeta: "))

# Alokasi Task dan Resource (Worker)
startTime = time.perf_counter()
dummyCT = calculateDummyCycleTime(taskTimeData, nStation)


# Penciptaan list A dan B
firstTask = [0]

# List Station 1, 2, 3
Station1 = []
Station2 = []
Station3 = []
Station4 = []
Station5 = []
Station6 = []
Station7 = []
Station8 = []
Station9 = []
Station10 = []
Station11 = []
Station12 = []
Station13 = []
Station14 = []
Station15 = []
Station16 = []

temp = []
visitedStation = [Station1, Station2, Station3, Station4, Station5, Station6, Station7, Station8, Station9, Station10, Station11, Station12, Station13, Station14, Station15, Station16]
idxStation = 0
restricted = []

# Buat matriks kosong
resultMatrix = []
posVisitTask = [0,1,2,3]

pheromone_matrices = []  # Daftar untuk menyimpan matriks pheromone
for _ in range(nWorker):
    pheromone = globalFeromon * np.ones((nTask, nTask))
    pheromone_matrices.append(pheromone)

# # Cetak matriks-matriks pheromone
# for i, pheromone in enumerate(pheromone_matrices):
#     print(f"Matriks Pheromone-{i+1}:")
#     print(pheromone)
#     print()

for i in range (iteration):
    for m in range (colony):
        index = 0
        randd = [0.453395713412637, 0.491498467321415, 0.846804777745682, 0.619367348176098, 0.297167465811096, 0.110205474800908, 0.43164295906485, 0.86541927053779, 0.748261254604284]
        listA, newAddedTask = checkPrecedence(tasks, firstTask, posVisitTask)
        if (len(listA)==0 and len(listB)==0):
            break
        # print("List A : ", end="")
        # print(listA)
        listB = checkTimeWorker(listA, dummyCT, taskTimeData, nWorker, visitedStation[idxStation], listWorker, restricted, idxStation) # List B + Worker
        # print("List B : ", end="")
        # print(listB)

        # Calculating OFV
        OFV = calculateOFV(listB, taskTimeData)

        # Calculating prob
        Prob = calculateProb(listB, zAlfa, zBeta, 0, pheromone_matrices)
        # print("========================================")
        # print(Prob)

        # Calculating cumulative
        Cumulative = calculateCumulative(Prob)

        # Saving Data
        Data_ = saveData(listB, OFV, Prob, Cumulative)
        # print("\nData: ", end="")
        # print(Data_)
        # print(len(Data_))
        for q in range (nTask):
            copyTaskTime = taskTimeData
            # print("=============================================")
            # random_decimal = random.random()
            random_decimal = randd[index]
            # print("\nRandom desimal: ", end="")
            # print(random_decimal)
            chosen, tempTime = chooseProbability(random_decimal, Data_)
            # print("Yang terpilih: ", end="")
            # print(chosen, tempTime)
            chosenTask = chosen[0]
            chosenWorker = chosen[1]
            firstTask.append(chosenTask)
            visitedStation[idxStation].append((chosenTask, chosenWorker, tempTime))

            # Update listA
            listA, newAddedTask = checkPrecedence(tasks, firstTask, posVisitTask)
            # print("Update List A : ", end="")
            # print(listA)

            # Update listB
            currStation = visitedStation[idxStation]
            # addTime = searchAddTime(currStation, listA, tasks)
            # print(addTime)
            if(len(newAddedTask) != 0):
                conditionList = searchConditionList(newAddedTask, tasks)
                addTime = searchMaxTime(currStation, conditionList)
            else:
                conditionList = []
                addTime = 0

            # print("\npersyaratan :")
            # print(newAddedTask)
            # print(conditionList)
            # print(addTime)
            copyTaskTime = updateTaskTimeData(copyTaskTime, chosenTask, chosenWorker, addTime, tempTime, combineTaskProducts((Data)), newAddedTask)
            listB = checkTimeWorker(listA, dummyCT, copyTaskTime, nWorker, visitedStation[idxStation],  listWorker, restricted, idxStation)
            # print("List Sebelum List B: ")
            # print(listB)
            if (len(listB) == 0) :  #Ganti Stasiun
                # print("Ganti Stasiun karena A")
                idxStation += 1
                copyTaskTime = combineTaskProducts((Data))
                restrictedList = restrictedWorker(visitedStation, idxStation)
                # print(restrictedList)
                for worker in restrictedList:
                    restricted.append(worker)
                if (len(listA)==0 and len(listB)==0):
                    break
                listB = checkTimeWorker(listA, dummyCT, copyTaskTime, nWorker, visitedStation[idxStation], listWorker, restricted, idxStation)

            # print("Update List B : ", end="")
            # print(listB)

            # Update OFV
            # print("Copy Task Time")
            # print(copyTaskTime)
            OFV = calculateOFV(listB, copyTaskTime)
            # print("\nUpdate OFV = ")
            # print(OFV)

            # Update Prob
            Prob = calculateProb(listB, zAlfa, zBeta, q, pheromone_matrices)

            # Update Cumulative
            Cumulative = calculateCumulative(Prob)

            # Update Data
            Data_ = saveData(listB, OFV, Prob, Cumulative)
            # print("\nUpdate Data: ", end="")
            # print(Data_)
            # print("")

            index += 1
        
        # Mengisi result matrix
        tempIdx = 0
        while tempIdx < 3:
            row = []  # Membuat objek row baru di setiap iterasi
            stat = visitedStation[tempIdx]
            dataAwal = combineTaskProducts(Data)
            for task in stat:
                for j in range(2):
                    statKerja = tempIdx + 1
                    tempTask = task[0]
                    tempWorker = task[1]
                    tempProduct = j + 1
                    waktuSelesai = round(task[2], 4)
                    waktuProses = round(dataAwal[tempTask - 1][tempWorker - 1], 4)
                    waktuMulai = round(waktuSelesai - waktuProses, 4)
                    row.append((statKerja, tempTask, tempWorker, tempProduct, waktuProses, waktuMulai, waktuSelesai))
            tempIdx += 1
            resultMatrix.append(row)

        # Cari nilai max tiap stasiun
        maxCTAktualStat = []
        for data_list in resultMatrix:
            max_waktu_selesai = 0
            for data in data_list:
                tempp = data[6]
                if tempp > max_waktu_selesai:
                    max_waktu_selesai = tempp
            maxCTAktualStat.append(max_waktu_selesai)

        # Update result matrix dengan menambahkan elemen ke-7 (ctAKtuall) pada setiap row
        for i in range(len(resultMatrix)):
            for j in range(len(resultMatrix[i])):
                resultMatrix[i][j] = resultMatrix[i][j] + (maxCTAktualStat[i],)

        # Update Feromone
        tempFeromone = []
        dataStation = []
        indexx = 1

        for row_idx, row in enumerate(visitedStation):
            for col_idx, value in enumerate(row):
                dataStation.append((indexx, value[0], value[1]))
                indexx += 1

        for i, pheromone in enumerate(pheromone_matrices):
            for data in dataStation:
                if (i == data[2]-1):
                    # print(data[2], data[1], data[0])
                    pheromone[data[1]-1][data[0]-1] += globalFeromon

        # Cetak matriks-matriks pheromone
        # for i, pheromone in enumerate(pheromone_matrices):
        #     print(f"Matriks Pheromone-{i+1}:")
        #     print(pheromone)
        #     print()

        

# print("\nResult Matriks: ")
# for i in range(len(resultMatrix)):
#     for j in range(len(resultMatrix[i])):
#         print(resultMatrix[i][j])

# print("\nCT Aktual: ",end="")
ctAktualTemp = 0
for i in range(len(resultMatrix)):
    for j in range(len(resultMatrix[i])):
        check = resultMatrix[i][j]
        if (ctAktualTemp < check[7]):
            ctAktualTemp = check[7]
# print(ctAktualTemp)
# print("\nStation: ")
# print("Stasiun 1 = ", end="")
# print(Station1)
# print("Stasiun 2 = ", end="")
# print(Station2)
# print("Stasiun 3 = ", end="")
# print(Station3)
        

# ---
# rute = np.zeros((colony, nTask))
# print(rute)

# random_number = random.random()

endTime = time.perf_counter()

# ----------------------------------------------------------------------------------
# Print Hasil
minCT = []
for i in range(nStation):
    print()
    print("========== STASIUN {} ==========".format(i+1))
    print("Task             : ", end="")
    for task in visitedStation[i]:
        temp = task[0]
        print("Task " + str(temp) + " ", end="     ")
    print("\nResource         : ", end="")
    for task in visitedStation[i]:
        temp = task[1]
        print("Worker " + str(temp) + " ", end="   ")
    print("\nWaktu model 1    : ", end="")
    for j in range(len(resultMatrix)):
        for k in range(len(resultMatrix[j])):
            check = resultMatrix[j][k]
            if check[0] - 1 == i and check[3] == 1:
                print(check[4], end="        ")
    print("\nWaktu model 2    : ", end="")
    for j in range(len(resultMatrix)):
        for k in range(len(resultMatrix[j])):
            check = resultMatrix[j][k]
            if check[0] - 1 == i and check[3] == 2:
                print(check[4], end="        ")
    print("\nTotal waktu      : ", end="")
    min = 10000000000
    for j in range(2):
        x = maxCTAktualStat[i]
        if x < min:
            min = x
        print("Waktu model ke - {}: {}".format(i+1, x), end="   ")
    print("\nCycle time       :", min)
    minCT.append(min)

print()
print("Cycle time solusi terbaik adalah ", end="")
minn = minCT[0]
for i in range(1, len(minCT)):
    if (minn < minCT[i]):
        minn = minCT[i]
print(minn)
print()
print("Waktu untuk run program: {} detik".format(endTime-startTime))