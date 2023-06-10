import numpy as np

nTask = 9
n = 5  # Jumlah matriks pheromone yang ingin dibuat
nilai_input = int(input("Masukkan nilai pheromone: "))  # Input nilai pheromone

pheromone_matrices = []  # Daftar untuk menyimpan matriks pheromone

for _ in range(n):
    pheromone = nilai_input * np.ones((nTask, nTask))
    pheromone_matrices.append(pheromone)

# Cetak matriks-matriks pheromone
for i, pheromone in enumerate(pheromone_matrices):
    print(f"Matriks Pheromone-{i+1}:")
    print(pheromone)
    print()