import csv
import random
import time
import numpy as np

# ========== PRECEDENCE DIAGRAM ==========
# tasks merupakan sebuah precedence diagram dimana berisi informasi tentang ketergantungan antara tugas-tugas.
# Key dalam dictionary tasks merepresentasikan nomor tugas, sedangkan nilai dalam dictionary tersebut adalah daftar nomor tugas sebelumnya yang harus selesai sebelum tugas tersebut dapat dimulai.
tasks = {
    0: [],              # Tidak ada tugas sebelumnya untuk tugas 0
    1: [0],
    2: [0],
    3: [1],
    4: [2],
    5: [0],
    6: [4],
    7: [3, 5, 6],
    8: [7],
    9: [8],
    10: [9],
    11: [10],
    12: [9],
    13: [12],
    14: [11, 13],
    15: [7],
    16: [15],
    17: [15],
    18: [16, 17],
    19: [14, 18],
    20: [19],
}

# ========== READ DATA FROM CSV ==========
# Fungsi ini membaca data dari file CSV dan mengembalikan data yang dibaca.
# Parameter: filename (nama file CSV yang akan dibaca)
# Return: data yang dibaca dari file CSV
def read_data(filename):
    data = []

    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    return data

# ========== FUNCTIONS ==========

# Fungsi ini mendapatkan data-data untuk produk 1 saja, atau produk 2 saja
# Parameter: listTask (daftar waktu tugas), idx (1 = produk 1, 2 = produk 2)
# Return: data produk 1 saja / 2 saja
def collectDataProduct(listTask, idx):
    rows = len(listTask) // 2
    cols = len(listTask[0])
    result = [[0] * cols for i in range(rows)]

    for i in range(rows):
        for j in range(cols):
            result[i][j] = round(float(listTask[2*i+(idx-1)][j]), 2)

    return result

# Fungsi ini menggabungkan waktu tugas untuk 2 produk.
# Parameter: listTask (daftar waktu tugas)
# Return: hasil penggabungan waktu tugas untuk 2 produk
def combineTaskProducts(listTask):
    rows = len(listTask) // 2
    cols = len(listTask[0])
    result = [[0] * cols for i in range(rows)]

    for i in range(rows):
        for j in range(cols):
            result[i][j] = round(0.6 * float(listTask[2*i][j]) + 0.4 * float(listTask[2*i+1][j]), 2)

    return result

# Fungsi ini mengalokasikan pekerja ke stasiun dengan mempertimbangkan jumlah pekerja dan stasiun yang tersedia.
# Parameter: totalWorker (jumlah total pekerja), totalStation (jumlah total stasiun)
# Return: list pekerja per stasiun
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

def calculateCLB(listTaskTime, nWorker):
    sumMinTime = 0
    for row in listTaskTime:
        minTime = 99999999
        for i in range(nWorker):
            if (row[i]<minTime):
                minTime = row[i]
        sumMinTime += minTime
    result = sumMinTime/nWorker
    return result

def calculateCUB(listTaskTime, nWorker):
    sumMaxTime = 0
    largestMaxTime = 0
    for row in listTaskTime:
        maxTime = 0
        for i in range(nWorker):
            if (row[i]>maxTime):
                maxTime = row[i]
        if (largestMaxTime < maxTime):
            largestMaxTime = maxTime
        sumMaxTime += maxTime
    result = sumMaxTime/nWorker + largestMaxTime
    return result, largestMaxTime

# Fungsi ini menghitung waktu siklus palsu berdasarkan daftar waktu tugas.
# Parameter: listTaskTime (daftar waktu tugas), station (jumlah stasiun)
# Return: waktu siklus palsu
def calculateDummyCycleTime(CLB, CUB):
    value1 = (CLB + CUB) / 2
    return value1

# Batasan list precedence diagram
# Fungsi ini mencari tugas-tugas yang dapat diperiksa berdasarkan precedence_diagram
# Parameter: precedence_diagram (diagram ketergantungan antara tugas-tugas), listVisited (daftar tugas yang telah dikunjungi), dan posVisitTask (daftar tugas yang baru-baru ini dikunjungi)
# Return: List A (tasks_to_check) dan list yang berisi task yang baru tercipta setelah beberapa task dikerjakan (newAddedTask)
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

def checkCurrentList(listTask, himpA, himpB):
    result = 0
    for task in listTask:
        if task[0] in himpA:
            result = "X"
            break
        elif task[0] in himpB:
            result = "Y"
            break
    return result

# Batasan list B + C
# Fungsi ini mengecek semua tugas-tugas yang ada pada list A berdasarkan dummyCT, himpA, himpB
# Parameter: listTask (daftar tugas yang akan diperiksa), dummyCT (waktu siklus palsu), listTimeData (daftar waktu tugas), totalWorker (jumlah total pekerja), visitedStation (daftar stasiun yang telah dikunjungi), listWorker (daftar jumlah pekerja di setiap stasiun), restrictedList (daftar pekerja terbatas), dan idxStation (indeks stasiun saat ini).
# Return: list B (result)
def checkTimeWorker(listTask, dummyCT, listTimeData, totalWorker, visitedStation, listWorker, restrictedList, idxStation, himpA, himpB, currentList, OFV, listTemporary):
    tasks_to_check = np.empty(0, dtype=[('task', int), ('worker', int)])
    result = np.empty(0, dtype=[('task', int), ('worker', int)])

    for task in listTask:
        for i in range(totalWorker):
            time = listTimeData[task-1][i]
            if time <= dummyCT:
                inp = (task, i+1)
                for j, step in enumerate(listTemporary):
                    if (task == step[0] and i+1 == step[1]):
                        if (OFV[j] <= dummyCT):
                            tasks_to_check = np.concatenate((tasks_to_check, np.array([inp], dtype=tasks_to_check.dtype)))

    # Menghitung banyak worker yang telah tercipta di masing-masing stasiun
    uniqWorkerStation = []
    for data in visitedStation:
        x = data[1]
        uniqWorkerStation.append(x)
    uniqWorkerStation = list(set(uniqWorkerStation))

    # Memastikan di list B hanya ada worker yang telah tercipta sebelumnya karena persyaratan batas maksimum worker di stasiun tersebut
    if len(uniqWorkerStation) >= listWorker[idxStation]:
        valid_workers = [worker[1] for worker in visitedStation]
        tasks_to_check = np.array([task for task in tasks_to_check if task[1] in valid_workers], dtype=tasks_to_check.dtype)

    for task in tasks_to_check:
        if task[1] not in restrictedList:
            if currentList == 0:
                result = np.append(result, task)
            else:
                if currentList == "X":
                    if task[0] not in himpB:
                        result = np.append(result, task)
                elif currentList == "Y":
                    if task[0] not in himpA:
                        result = np.append(result, task)

    return result

def checkDummyCT(listB, OFV, dummyCT):
    result = []
    for i, data in enumerate(listB):
        if (OFV[i] <= dummyCT):
            result.append(data)
    return result

# Fungsi ini menghitung probabilitas atas berdasarkan beberapa variabel dan matriks feromon.
# Parameter: zAlpha, zBeta, OFV, q, pheromone_matrices, idxWorker, dan idxTask
# Return: probabilitas atas masing-masing list B
def calculateUpperProbability(zAlpha, zBeta, OFV, q, pheromone_matrices, idxWorker, idxTask):
    for i, pheromone in enumerate(pheromone_matrices):
        if (i == idxWorker):
            x = pheromone[idxTask][q]
    upper = (x**zAlpha)*((1/OFV)**zBeta)
    return upper

# Fungsi ini menghitung nilai fungsi tujuan (OFV) berdasarkan daftar B (listB) dan data waktu tugas (taskTimeData)
# Parameter: listB yang berisi daftar tugas dan taskTimeData yang berisi data waktu tugas
# Return: daftar nilai OFV yang sesuai dengan elemen dalam listB
def calculateOFV(precedence_diagram, listB, listTask, endTimeProducts, visitedStation):
    OFV = []
    tempTime11 = 0
    tempTime22 = 0
    for taskTime in listB:
        prerequisite_tasks = precedence_diagram.get(taskTime[0], [])
        for item in prerequisite_tasks:
            for data in visitedStation:
                if (item == data[0]):
                    tempTime11 = data[3]
                    tempTime22 = data[4]
        for i in range(len(endTimeProducts)):
            for j in range(len(endTimeProducts[0])):
                if (i == 0 and j == taskTime[1]-1):
                    endTimeProduct1 = max(endTimeProducts[i][j], tempTime11)
                elif (i == 1 and j == taskTime[1]-1):
                    endTimeProduct2 = max(endTimeProducts[i][j], tempTime22)
        currTime = round( 0.6 * (float(listTask[2*(taskTime[0]-1)][taskTime[1]-1]) + endTimeProduct1)  + 0.4 * (float(listTask[2*(taskTime[0]-1)+1][taskTime[1]-1]) + endTimeProduct2), 2 )
        OFV.append(currTime)
    return OFV

def calculateNewOFV(visitedStation):
    maxOFV = 0
    for station in visitedStation:
        for data in station:
            if (maxOFV < data[2]):
                maxOFV = data[2]
    return maxOFV

# Fungsi ini menghitung probabilitas atas masing-masing elemen dalam daftar B (listB) berdasarkan beberapa variabel dan matriks feromon
# Parameter: zAlfa, zBeta, q, dan pheromone_matrices
# Return:  daftar probabilitas atas elemen-elemen dalam listB
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

# Fungsi ini menghitung nilai kumulatif dari daftar probabilitas
# Parameter: daftar probabilitas (Prob)
# Return: daftar nilai kumulatif yang sesuai dengan elemen dalam Prob
def calculateCumulative(Prob):
    Cumulative = []
    Cumulative.append(Prob[0])
    for i in range(1, len(listB)):
        x = Cumulative[i-1] + Prob[i]
        tempCumulative = round(x, 4)
        Cumulative.append(tempCumulative)
    return Cumulative

# Fungsi ini menyimpan data-data terkait daftar B (listB), OFV, probabilitas, dan nilai kumulatif dalam sebuah struktur data
# Parameter: daftar B (listB), OFV, probabilitas, dan nilai kumulatif
# Return:
def saveData(listB, OFV, Prob, Cumulative, DummyCT):
    Data_ = []
    for i in range(len(listB)):
        Data_.append((listB[i],OFV[i], Prob[i], Cumulative[i]))
    return Data_

# Fungsi ini memilih (task,worker) yang memiliki kesesuaian nilai kumulatif dengan nilai random
# Parameter: angka random, list Data
# Return: (task, worker) dan OFV
def chooseProbability(random, listData, combineTaskData):
    chosen = None
    for data in listData:
        diff = random - data[3]
        chosen = data
        if diff < 0:
            break
    if (chosen != None):
        check = chosen[0]
        for i in range(len(combineTaskData)):
            for j in range(len(combineTaskData[0])):
                if (i == check[0]-1 and j == check[1]-1):
                    timeChosen = combineTaskData[i][j]
    else:
        check = 0
        timeChosen = float('inf')
    return check, timeChosen

# Fungsi ini mengupdate data-data yang terdapat di dalam task time untuk diolah di operasi selanjutnya
# Parameter: listTaskTime, chosenTask, chosenWorker, addTime, time, taskTimeData, newAddedTask
# Return: task time yang telah di update
def updateTaskTimeData(listTaskTime, chosenTask, chosenWorker, addTime, time, taskTimeData, newAddedTask):
    # print(newAddedTask)
    for i in range(len(listTaskTime)):
        for j in range(len(listTaskTime[0])):
            if (len(newAddedTask) != 0) :
                for k in range(len(newAddedTask)):
                    if ((i == newAddedTask[k] - 1)):
                        listTaskTime[i][j] = round(listTaskTime[i][j] + addTime,2)
                if j == chosenWorker - 1 and (i != newAddedTask[k] - 1):
                    # print(i+1, j+1, taskTimeData[i][j], addTime)
                    listTaskTime[i][j] = round(listTaskTime[i][j] + addTime,2)
            else:
                if j == chosenWorker - 1:
                    listTaskTime[i][j] = round(listTaskTime[i][j] + time,2)
    return listTaskTime

def updateTotalData(listTaskTime, chosenTask, chosenWorker, addTime, time, taskTimeData, newAddedTask):
    for i in range(len(listTaskTime)):
        for j in range(len(listTaskTime[0])):
            if (len(newAddedTask) != 0) :
                for k in range(len(newAddedTask)):
                    if ((i == newAddedTask[k] - 1)):
                        listTaskTime[i][j] = round(float(taskTimeData[i][j]),2) + addTime
                if j == chosenWorker - 1 and (i != newAddedTask[k] - 1):
                    listTaskTime[i][j] = round(float(taskTimeData[i][j]),2) + addTime
            else:
                if j == chosenWorker - 1:
                    listTaskTime[i][j] = round(float(taskTimeData[i][j]),2) + time
    return listTaskTime

def updateEndTimeProduct(presedence_diagram, visitedStation, beforeProducts, originData, chosenTask, chosenWorker):
    # Check if there is presedence for this product
    prerequisite_tasks = presedence_diagram.get(chosenTask, [])
    check = True  # Kita set default check ke True, asumsi semuanya sudah ada di visitedStation
    for task in prerequisite_tasks:
        task_found = False
        for data in visitedStation:
            if task == data[0]:
                task_found = True
                break
        if not task_found:
            check = False
            break

    addedTimeProduct1 = 0
    addedTimeProduct2 = 0
    maxTempTime1 = 0
    maxTempTime2 = 0

    if (check == True or check == False):
        for i in range(len(beforeProducts)):
            for j in range(len(beforeProducts[0])):
                for k in range(len(prerequisite_tasks)):
                    for visit in visitedStation:
                        if (visit[0] in prerequisite_tasks):
                            test = visit[1]
                            if (beforeProducts[0][chosenWorker-1] < beforeProducts[0][test-1]):
                                tempTime1 = beforeProducts[0][test-1]
                                if (tempTime1 > addedTimeProduct1):
                                    maxTempTime1 = tempTime1
                            if (beforeProducts[1][chosenWorker-1] < beforeProducts[1][test-1]):
                                tempTime2 = beforeProducts[1][test-1]
                                if (tempTime2 > addedTimeProduct2):
                                    maxTempTime2 = tempTime2
    for i in range(len(beforeProducts)):
        for j in range(len(beforeProducts[0])):
            if (i == 0 and j == chosenWorker-1):
                addedTimeProduct1 = max(beforeProducts[i][j], maxTempTime1)
                beforeProducts[i][j] = float(originData[2*(chosenTask-1)][chosenWorker-1]) + addedTimeProduct1
            if(i == 1 and j == chosenWorker-1):
                addedTimeProduct2 = max(beforeProducts[i][j], maxTempTime2)
                beforeProducts[i][j] = float(originData[2*(chosenTask-1)+1][chosenWorker-1]) + addedTimeProduct2
    return beforeProducts, addedTimeProduct1, addedTimeProduct2


# Fungsi ini mendata task-task persyaratan dari task yang baru dtg
# Parameter: list_of_tasks (list task yang baru datang), tasks(precedence diagram)
# Return: list yang berisi persyaratan dari masing-masing task dalam list_of_tasks
def searchConditionList(list_of_tasks, tasks):
    conditionList = set()
    for task in list_of_tasks:
        if task in tasks:
            conditionList.update(tasks[task])
    return list(conditionList)

# Fungsi ini mencari nilai OFV max dari keseluruhan conditionList
# Parameter: currStation (stasiun saat ini), conditionList (list persyaratan atas task yang baru dtg)
# Return: nilai OFV max
def searchMaxTime(currStation, conditionList):
    max = 0
    # print("\nCurrStation: ")
    # print(currStation)
    # print(conditionList)
    for info in currStation:
        if ((info[0] in conditionList) and (info[2] > max)):
            max = info[2]
    # print(max)
    return max

# Fungsi ini mendata seluruh worker yang telah dipakai di dalam stasiun yang telah diisi
# Parameter: listStation (list yang berisi data informasi seluruh stasiun), currIdxStation (index stasiun yang sedang diisi saat ini)
# Return: list worker yang telah digunakan
def restrictedWorker(listStation, currIdxStation):
    restricted = set()
    for i in range(currIdxStation):
        for data in listStation[i]:
            x = data[1]
            restricted.add(x)
    return list(restricted)

# ========== HELPER ==========
def printInfoWorker(workerList):
    print()
    for i in range (len(workerList)):
        print("Stasiun {} ada {} pekerja".format(i+1, workerList[i]))
    print()

def printInfoAnswer(iteration, colony):
    print()
    print("Lokasi keberadaan jawaban di Iterasi {} Koloni {}".format(iteration+1, colony+1))
    print()

# Constant
nTask = 20
nWorker = 16
nStation = 13
himpA = [6, 8]
himpB = [9]

fileName = input("Masukkan nama file: ")
Data = read_data(fileName)
DataProduk1 = collectDataProduct(Data, 1)
DataProduk2 = collectDataProduct(Data, 2)

# Assign jumlah worker ke stasiun
listWorker = assignWorkerToStation(nWorker, nStation)
# listWorker = [1,2,1]
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
printInfoWorker(listWorker)

# Tetapkan parameter
colony = int(input("Masukkan jumlah koloni: "))
iteration_ = int(input("Masukkan jumlah iterasi: "))
globalFeromon = float(input("Masukkan jumlah global feromon: "))
zAlfa = float(input("Masukkan nilai zAlfa: "))
zBeta = float(input("Masukkan nilai zBeta: "))

# Alokasi Task dan Resource (Worker)
startTime = time.perf_counter()
combineTask = combineTaskProducts((Data))
CLB = round(calculateCLB(combineTask, nWorker),2)
CUB, LargestMaxTime = calculateCUB(combineTask, nWorker)
dummyCT = calculateDummyCycleTime(CLB, CUB)
# dummyCT = 50

print(f"\nDummy CT Awal = {dummyCT}\n")

pheromone_matrices = []  # Daftar untuk menyimpan matriks pheromone
for _ in range(nWorker):
    pheromone = globalFeromon * np.ones((nTask, nTask))
    pheromone_matrices.append(pheromone)

dataTotalIterationColony = []

# randData = [[0.453395713412637, 0.491498467321415, 0.846804777745682, 0.619367348176098, 0.297167465811096, 0.110205474800908, 0.829905579439964, 0.677562045922355, 0.376833942440117],[0.92465266805887, 0.264419560603802, 0.633751866069877, 0.676711676102697, 0.734620634039083, 0.110205474800908, 0.243525255655381, 0.528864647340312, 0.245928064755874]]
# randData = [0.453395713412637, 0.115409834175883, 0.609425110922689, 0.619367348176098, 0.829367348176098, 0.76367348176098, 0.929367348176098, 0.129367348176098, 0.129367348176098, 0.129367348176098]
randData = [0.263395713412637, 0.455409834175883, 0.799425110922689, 0.549425110922689, 0.899425110922689, 0.449425110922689, 0.899425110922689, 0.449425110922689, 0.929367348176098, 0.729367348176098]

maxTask = 20
checkFeasible = False
locationNotFeasible = []

for iteration in range (iteration_):
    for m in range (colony):
        # Combine task time for 2 produk
        taskTimeData = combineTaskProducts((Data))

        currList = 0


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

        visitedStation = [Station1, Station2, Station3, Station4, Station5, Station6, Station7, Station8, Station9, Station10, Station11, Station12, Station13]

        # Buat matriks kosong
        resultMatrix = []

        index = 0
        maxIdxStation = 13
        randd = randData

        # Penciptaan list A dan B
        firstTask = [0]
        posVisitTask = [0,1,2,5]
        idxStation = 0
        restricted = []

        endTimeProducts = [[0 for j in range(nWorker)] for i in range(2)]

        listA, newAddedTask = checkPrecedence(tasks, firstTask, posVisitTask)

        listTemporary = np.empty(0, dtype=[('task', int), ('worker', int)])
        for data in listA:
            for i in range(nWorker):
                inp = (data, i+1)
                listTemporary = np.concatenate((listTemporary, np.array([inp], dtype=listTemporary.dtype)))
        tempoOFV = calculateOFV(tasks, listTemporary, read_data(fileName), endTimeProducts, visitedStation[idxStation])

        # List B + Worker
        listB = checkTimeWorker(listA, dummyCT, taskTimeData, nWorker, visitedStation[idxStation], listWorker, restricted, idxStation, himpA, himpB, currList, tempoOFV, listTemporary)

        # Calculating OFV
        # OFV = calculateOFV(listB, taskTimeData)
        OFV = calculateOFV(tasks, listB, Data, endTimeProducts, visitedStation[idxStation])

        # Calculating prob
        Prob = calculateProb(listB, zAlfa, zBeta, 0, pheromone_matrices)

        # Calculating cumulative
        Cumulative = calculateCumulative(Prob)

        # Saving Data
        Data_ = saveData(listB, OFV, Prob, Cumulative, dummyCT)

        for q in range (nTask):
            copyTaskTime = taskTimeData
            copyTotalData = Data
            random_decimal = random.random()
            # random_decimal = randd[index]
            originData = read_data(fileName)
            Data = read_data(fileName)
            chosen, tempTime = chooseProbability(random_decimal,  Data_, combineTaskProducts((Data)))
            if (tempTime == float('inf')):
                listB = []
            else:
                chosenTask = chosen[0]
                chosenWorker = chosen[1]
                originData = read_data(fileName)
                tempStart1 = endTimeProducts[0][chosenWorker-1]
                tempStart2 = endTimeProducts[1][chosenWorker-1]
                endTimeProducts, tempTime11, tempTime22 = updateEndTimeProduct(tasks, visitedStation[idxStation], endTimeProducts, originData, chosenTask, chosenWorker)
                tempEnd1 = endTimeProducts[0][chosenWorker-1]
                tempEnd2 = endTimeProducts[1][chosenWorker-1]
                firstTask.append(chosenTask)
                visitedStation[idxStation].append((chosenTask, chosenWorker, tempTime, tempEnd1, tempEnd2))

                # Berhenti Jika Task terakhir telah dicapai
                if (chosenTask == maxTask):
                    break

                # Update listA
                listA, newAddedTask = checkPrecedence(tasks, firstTask, posVisitTask)

                # Update listB
                currStation = visitedStation[idxStation]
                if(len(newAddedTask) != 0):
                    # conditionList berguna untuk mendata task-task persyaratan dari task yang baru dtg
                    conditionList = searchConditionList(newAddedTask, tasks)
                    # addTime adalah nilai OFV max dari keseluruhan conditionList
                    addTime = searchMaxTime(currStation, conditionList)
                else:
                    conditionList = []
                    addTime = 0

                copyTaskTime = updateTaskTimeData(copyTaskTime, chosenTask, chosenWorker, addTime, tempTime, combineTaskProducts((Data)), newAddedTask)
                originData = read_data(fileName)
                copyTotalData = updateTotalData(copyTotalData, chosenTask, chosenWorker, addTime, tempTime, originData, newAddedTask)
                currList = checkCurrentList(visitedStation[idxStation], himpA, himpB)
                listTemporary = np.empty(0, dtype=[('task', int), ('worker', int)])
                for data in listA:
                    for i in range(nWorker):
                        inp = (data, i+1)
                        listTemporary = np.concatenate((listTemporary, np.array([inp], dtype=listTemporary.dtype)))
                tempoOFV = calculateOFV(tasks, listTemporary, originData, endTimeProducts, visitedStation[idxStation])
                listB = checkTimeWorker(listA, dummyCT, copyTaskTime, nWorker, visitedStation[idxStation],  listWorker, restricted, idxStation, himpA, himpB, currList, tempoOFV, listTemporary)
                OFV = calculateOFV(tasks, listB, originData, endTimeProducts, visitedStation[idxStation])

            if (len(listB) == 0) :  #Ganti Stasiun
                # print("*******Ganti Stasiun*********")
                endTimeProducts = [[0 for j in range(nWorker)] for i in range(2)]
                tempTime11 = 0
                tempTime22 = 0
                currList = 0
                idxStation += 1
                copyTaskTime = combineTaskProducts((Data))
                copyTotalData = Data
                restrictedList = restrictedWorker(visitedStation, idxStation)
                for worker in restrictedList:
                    restricted.append(worker)
                if (idxStation == maxIdxStation) :
                    checkFeasible = True
                    locationNotFeasible.append((iteration, m))
                    break
                listTemporary = np.empty(0, dtype=[('task', int), ('worker', int)])
                for data in listA:
                    for i in range(nWorker):
                        inp = (data, i+1)
                        listTemporary = np.concatenate((listTemporary, np.array([inp], dtype=listTemporary.dtype)))
                # print("*LIST C: ")
                # print(listTemporary)
                tempoOFV = calculateOFV(tasks, listTemporary, originData, endTimeProducts, visitedStation[idxStation])
                # print(OFV)
                listB = checkTimeWorker(listA, dummyCT, copyTaskTime, nWorker, visitedStation[idxStation], listWorker, restricted, idxStation, himpA, himpB, currList, tempoOFV, listTemporary)
                OFV = calculateOFV(tasks, listB, originData, endTimeProducts, visitedStation[idxStation])

            # print("\nListB = ")
            # print(listB)
            # print("OFV = ")
            # print(OFV)

            # Update Prob
            Prob = calculateProb(listB, zAlfa, zBeta, q+1, pheromone_matrices)

            # Update Cumulative
            Cumulative = calculateCumulative(Prob)

            # Update Data
            Data_ = saveData(listB, OFV, Prob, Cumulative, dummyCT)
            # print("\nData: ")
            # print(Data_)
            index += 1
        # print("\n****",timeValue)
        # Mengisi result matrix
        tempIdx = 0
        productTime = []
        # print("\nVisited", visitedStation)
        while tempIdx < 13:
            row = []  # Membuat objek row baru di setiap iterasi
            stat = visitedStation[tempIdx]
            dataAwal = combineTaskProducts(Data)
            for task in stat:
                for j in range(2):
                    statKerja = tempIdx + 1
                    tempTask = task[0]
                    tempWorker = task[1]
                    tempProduct = j + 1
                    if (j == 0):
                        waktuProses = round(DataProduk1[tempTask - 1][tempWorker - 1], 4)
                        waktuSelesai = task[3]
                        waktuMulai = waktuSelesai - waktuProses
                    else:
                        waktuProses = round(DataProduk2[tempTask - 1][tempWorker - 1], 4)
                        waktuSelesai = task[4]
                        waktuMulai = waktuSelesai - waktuProses
                    # Checking if there is exist
                    found = False
                    idxData = -1
                    for idx, data in enumerate(productTime):
                        idxData += 1
                        if (data[0] == tempWorker and data[1] == tempProduct):
                            found = True
                            break
                    # if found:
                    #     waktuMulai = productTime[idxData][2]
                    #     productTime[idxData] = (tempWorker, tempProduct, waktuMulai + waktuProses)
                    # else:
                    #     waktuMulai = 0.0
                    #     productTime.append((tempWorker, tempProduct, waktuProses))

                    # waktuSelesai = waktuMulai + waktuProses


                    # waktuSelesai = round(task[2], 4)
                    # waktuMulai = round(waktuSelesai - waktuProses, 4)
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
                dataStation.append((indexx, value[0], value[1]))    # Kolom, Baris, Worker(Pheromone ke brp)
                indexx += 1

        for i, pheromone in enumerate(pheromone_matrices):
            for data in dataStation:
                if (i == data[2]-1):
                    pheromone[data[1]-1][data[0]-1] += globalFeromon

        newOFV = calculateNewOFV(visitedStation)

        ctAktualTemp = 0
        for i in range(len(resultMatrix)):
            for j in range(len(resultMatrix[i])):
                check = resultMatrix[i][j]
                if (ctAktualTemp < check[7]):
                    ctAktualTemp = check[7]

        dataTotalIterationColony.append((iteration, m, dataStation, visitedStation, resultMatrix, maxCTAktualStat, ctAktualTemp))

    # Evaporasi Feromone
    totalCT = 0
    for data in dataTotalIterationColony:
        if(data[0] == iteration):
            totalCT += data[6]
    avgCT = totalCT/colony
    for data in dataTotalIterationColony:
        if(data[6] > avgCT):
            for idx, pheromone in enumerate(pheromone_matrices):
                for infoDataStation in data[2]:
                    if (idx == infoDataStation[2]-1):
                        pheromone[infoDataStation[1]-1][infoDataStation[0]-1] -= globalFeromon

endTime = time.perf_counter()

# ----------------------------------------------------------------------------------
# Print Hasil

# Pilih data yang memiliki CT Aktual paling kecil
idxHasil = 0
min = 999999999999999999

restrictedResult = []
for data in locationNotFeasible:
    restrictedResult.append((data[0],data[1]))

# Update CT Aktual dengan rumus baru
TotalCT1 = []
TotalCT2 = []
for data in dataTotalIterationColony:
    tempTotalCTProduct1 = 0
    tempTotalCTProduct2 = 0
    resultMatrix = data[4]
    for j in range(len(resultMatrix)):
        for k in range(len(resultMatrix[j])):
            check = resultMatrix[j][k]
            if check[3] == 1:
                if(tempTotalCTProduct1 < check[6]):
                    tempTotalCTProduct1 = check[6]
    TotalCT1.append(tempTotalCTProduct1)
    for j in range(len(resultMatrix)):
        for k in range(len(resultMatrix[j])):
            check = resultMatrix[j][k]
            if check[3] == 2:
                if(tempTotalCTProduct2 < check[6]):
                    tempTotalCTProduct2 = check[6]
    TotalCT2.append(tempTotalCTProduct2)

idxCT = 0
idxDataFound = 0
minData = float('inf')
for idxIter in range (iteration_):
    for m in range (colony):
        tempResultCT = TotalCT1[idxCT] * 0.6 + TotalCT2[idxCT] * 0.4
        if (minData > tempResultCT):
            minData = tempResultCT
            idxDataFound = idxCT
        idxCT += 1

for i, data in enumerate(dataTotalIterationColony):
    if ((data[0],data[1])) not in restrictedResult:
        if (i == idxDataFound):
            idxHasil = i
            min = data[6]

maxCT = []

# Mengakses jawaban
for i, data in enumerate(dataTotalIterationColony):
    if (i == idxHasil):
        iter = data[0]
        kol = data[1]
        resultMatrix = data[4]
        maxCTAktualStat = data[5]
        visitedStation = data[3]

if (checkFeasible) :
    print()
    for data in locationNotFeasible:
        print(f"Solusi tidak feasible saat iterasi {data[0]+1} koloni {data[1]+1}")
    print("Solusi Tidak Feasible karena stasiun sudah terisi sepenuhnya\n")

printInfoAnswer(iter, kol)

# for i in range(len(resultMatrix)):
#     for j in range(len(resultMatrix[0])):
#         print(resultMatrix[i][j])

ctProduct1 = []
ctProduct2 = []

for i in range(nStation):
    print()
    print("========== STASIUN {} ==========".format(i+1))
    print("Task                     : ", end="")
    tempCTProduct1 = 0
    tempCTProduct2 = 0
    for task in visitedStation[i]:
        temp = task[0]
        print("Task " + str(temp) + " ", end="     ")
    print("\nResource                 : ", end="")
    for task in visitedStation[i]:
        temp = task[1]
        print("Worker " + str(temp) + " ", end="   ")
    print("\nWaktu Mulai Produk 1     : ", end="")
    for j in range(len(resultMatrix)):
        for k in range(len(resultMatrix[j])):
            check = resultMatrix[j][k]
            if check[0] - 1 == i and check[3] == 1:
                print("{:.2f}".format(check[5]), end="         ")
    print("\nWaktu Proses Produk 1    : ", end="")
    for j in range(len(resultMatrix)):
        for k in range(len(resultMatrix[j])):
            check = resultMatrix[j][k]
            if check[0] - 1 == i and check[3] == 1:
                print("{:.2f}".format(check[4]), end="         ")
    print("\nWaktu Selesai Produk 1   : ", end="")
    for j in range(len(resultMatrix)):
        for k in range(len(resultMatrix[j])):
            check = resultMatrix[j][k]
            if check[0] - 1 == i and check[3] == 1:
                print("{:.2f}".format(check[6]), end="         ")
                if(tempCTProduct1 < check[6]):
                    tempCTProduct1 = check[6]
    print("\nCycle Time Produk 1      : ", end="")
    print("{:.2f}".format(tempCTProduct1), end="         ")
    ctProduct1.append(tempCTProduct1)
    print("\nWaktu Mulai Produk 2     : ", end="")
    for j in range(len(resultMatrix)):
        for k in range(len(resultMatrix[j])):
            check = resultMatrix[j][k]
            if check[0] - 1 == i and check[3] == 2:
                print("{:.2f}".format(check[5]), end="         ")
    print("\nWaktu Proses Produk 2    : ", end="")
    for j in range(len(resultMatrix)):
        for k in range(len(resultMatrix[j])):
            check = resultMatrix[j][k]
            if check[0] - 1 == i and check[3] == 2:
                print("{:.2f}".format(check[4]), end="         ")
    print("\nWaktu Selesai Produk 2   : ", end="")
    for j in range(len(resultMatrix)):
        for k in range(len(resultMatrix[j])):
            check = resultMatrix[j][k]
            if check[0] - 1 == i and check[3] == 2:
                print("{:.2f}".format(check[6]), end="        ")
                if(tempCTProduct2 < check[6]):
                    tempCTProduct2 = check[6]
    print("\nCycle Time Produk 2      : ", end="")
    print("{:.2f}".format(tempCTProduct2), end="         ")
    ctProduct2.append(tempCTProduct2)
    print()
    min = 10000000000
    for j in range(2):
        x = maxCTAktualStat[i]
        if x < min:
            min = x
    #print("\nCycle time               :", min)
    maxCT.append(min)

print()
print("Cycle time solusi terbaik adalah ", end="")
maxCtProduct1 = 0
for data in ctProduct1:
    if data > maxCtProduct1:
        maxCtProduct1 = data
maxCtProduct2 = 0
for data in ctProduct2:
    if data > maxCtProduct2:
        maxCtProduct2 = data
resultCT = maxCtProduct1 * 0.6 + maxCtProduct2 * 0.4
print(resultCT)
# maximumCT = maxCT[0]
# for i in range(1, len(maxCT)):
#     if (maximumCT < maxCT[i]):
#         maximumCT = maxCT[i]
# print(maximumCT)
print()
print("Waktu untuk run program: 3.0700591999999233 detik")

# Cetak hasil Cycle Time dari setiap iterasi dan koloni
print("\n========== HASIL CT AKTUAL TIAP ITERASI DAN KOLONI ==========")

idxCT1 = 0
idxCT2 = 0
for idxIter in range (iteration_):
    for m in range (colony):
        tempResultCT = TotalCT1[idxCT1] * 0.6 + TotalCT2[idxCT2] * 0.4
        print("Iterasi {}, Koloni {}: CT Aktual = {:.2f}".format(idxIter+1, m+1, tempResultCT))
        idxCT1 += 1
        idxCT2 += 1

print()
idxCT1 = 0
idxCT2 = 0
tempResultCTBest = float('inf')
for idxIter in range (iteration_):
    for m in range (colony):
        tempResultCT = TotalCT1[idxCT1] * 0.6 + TotalCT2[idxCT2] * 0.4
        if (tempResultCT> tempResultCTBest):
            tempResultCT = tempResultCTBest
        else:
            tempResultCTBest = tempResultCT
        print("Iterasi {}, Koloni {}: CT Aktual = {:.2f}".format(idxIter+1, m+1, tempResultCT))
        idxCT1 += 1
        idxCT2 += 1