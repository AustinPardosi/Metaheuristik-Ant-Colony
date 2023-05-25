import csv
import random

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

# Constant
Task = 9
Worker = 5
Station = 3

fileName = input("Masukkan nama file: ")
taskTimeData = read_data(fileName)

# Tetapkan parameter
colony = int(input("Masukkan jumlah koloni: "))
iteration = int(input("Masukkan jumlah iterasi: "))
globalFeromon = int(input("Masukkan jumlah global feromon: "))
zAlpha = 0.7
zBeta = 0.4

listWorker = assignWorkerToStation(Worker, Station)
print(listWorker)