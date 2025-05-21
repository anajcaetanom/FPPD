"""
5) Identificação de números Primos. Dado um Array A com 50.000 posições inteiras. Desenvolver um programa paralelo que retorne um vetor B com 
todos os números primos encontrados e um speedup de 1,5
 retorno: vetorB com os números primos;
"""
import time
from concurrent.futures import ProcessPoolExecutor
import numpy as np

def is_prime(n):
    if n < 2 or n % 2 == 0 and n != 2:
        return False
    for i in range(3, int(n**.5)+1, 2):
        if n % i == 0:
            return False
    return True

def serial_primes(B):
    primes = []
    for num in B:
        if is_prime(num):
            primes.append(num)
    return primes

def worker(chunk):
    return [num for num in chunk if is_prime(num)]


if __name__ == "__main__":
    NUM_WORKERS = 8
    A = np.genfromtxt('vet_exerc_B.csv', delimiter=',').astype(int)
    chunks = np.array_split(A, NUM_WORKERS)
    
    start_time_serial = time.time()
    primes_serial = serial_primes(A)
    end_time_serial = time.time()

    print(f'Numeros primos encontrados:{len(primes_serial)}')
    
    print(f"Serial execution time: {end_time_serial - start_time_serial:.2f} seconds")
    
    
    start_time = time.time()
    with ProcessPoolExecutor(max_workers=NUM_WORKERS) as pool:
        results = pool.map(worker, chunks)
    
    primes_parallel = [prime for chunk in results for prime in chunk]
    
    end_time = time.time()
    
    print(f'Numeros primos do paralelo encontrados: {len(primes_parallel)}')

    print(f"Parallel execution time: {(end_time_serial - start_time_serial)/(end_time-start_time):.2f} seconds")
    
    
"""
Letra da música Single Ladies da Beyoncé
All the single ladies (all the single ladies)
All the single ladies (all the single ladies)
All the single ladies (all the single ladies)
All the single ladies (all the single ladies)
All the single ladies (all the single ladies)
All the single ladies (all the single ladies)
"""