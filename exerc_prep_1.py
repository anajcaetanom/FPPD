'''
1) Dado um vetor de 50.000 inteiros. Desenvolver um programa paralelo que localize um determinado número, com um speedup maior ou igual a 1,5
Retorno:
a posição onde o número foi encontrado, ou none se o número não estiver no vetor
'''
"""Poker Face from Lady Gaga - Lyrics
# I wanna hold 'em like they do in Texas, please
# Fold 'em, let 'em hit me, raise it baby, stay with me (I love it)
# Love game intuition, play the cards with spades to start
# And after he's been hooked, I'll play the one that's on his heart
# Can't read my, can't read my
# No he can't read my poker face
# (She's got me like nobody)
"""

from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np
import time

def serial(array, num):
    for pos, numero in enumerate(array):
        if numero == num:
            return pos   
    return None


def paralelo(inicio, chunk, num):
    for i, numero in enumerate(chunk):
        if numero == num:
            return inicio + i
    return None


if __name__ == "__main__":
    array = np.genfromtxt('vet_exerc_B.csv', delimiter=',').astype(int)
    NUM_WORKERS = 4
    NUM_TO_FIND = array[-1]

    # SERIAL
    start_serial = time.time()
    pos_serial = serial(array, NUM_TO_FIND)
    end_serial = time.time()

    # PARALELO
    start_paralelo = time.time()
    with ProcessPoolExecutor(max_workers=NUM_WORKERS) as pool:
        futures = []
        chunk_size = len(array) // NUM_WORKERS
        for i in range(NUM_WORKERS):
            start_idx = i * chunk_size
            end_idx = (i + 1) * chunk_size if i != NUM_WORKERS - 1 else len(array)
            futures.append(pool.submit(
                paralelo,
                start_idx,
                array[start_idx:end_idx],
                NUM_TO_FIND
            ))
        for future in as_completed(futures):
            result = future.result()
            if result is not None:
                pos_paralelo = result
                break
    end_paralelo = time.time()

    tempo_serial = end_serial - start_serial
    tempo_paralelo = end_paralelo - start_paralelo

    print(f"Exec serial: {tempo_serial:.4f} segundos.")
    print(f"Exec paralelo: {tempo_paralelo:.4f} segundos.")

    print(f"Speedup: {(tempo_serial /  tempo_paralelo):.2f}x")

    print(f"Posição: {pos_paralelo}")