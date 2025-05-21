'''
 4) Dado um Array A com 50.000 posições inteiras, desenvolva um programa paralelo que retorne um vetor B com a soma doa
 prefixos(B[i]= Somatória A[i-1 : i]), com speedup  maior ou igual a 1,5
 retorno: vetor com a soma de prefixos B com 50 mil posições;
'''
import numpy as np
from itertools import accumulate
from multiprocessing.pool import ThreadPool
import time

def partial_prefix(chunk):
    """Calcula o prefixo parcial de um chunk."""
    return list(accumulate(chunk))

def prefix_sum_threadpool(arr, num_threads=2):
    """Calcula o prefix sum usando um pool de threads."""
    n = len(arr)
    chunk_size = (n + num_threads - 1) // num_threads  # Divide o array em blocos

    # Divide em chunks
    chunks = [arr[i:i+chunk_size] for i in range(0, n, chunk_size)]

    # Cria um pool de threads
    with ThreadPool(processes=num_threads) as pool:
        partial_results = pool.map(partial_prefix, chunks)

    # Corrige os resultados parciais
    result = []
    offset = 0
    for partial in partial_results:
        corrected = [x + offset for x in partial]
        result.extend(corrected)
        offset = result[-1]  # Último valor do bloco atual vira offset do próximo

    return result

def prefix_sum_serial(arr):
    """Calcula o prefix sum de forma serial."""
    return list(accumulate(arr))


if __name__ == "__main__":
    # Exemplo de uso
    A = np.genfromtxt("vet_exerc_B.csv", delimiter=",")
    print(f"Array original: {A}")
    num_threads = 20  # Número de threads

    # Medir tempo para execução paralela
    start_parallel = time.time()
    P_parallel = prefix_sum_threadpool(A, num_threads=num_threads)
    end_parallel = time.time()

    # Medir tempo para execução serial
    start_serial = time.time()
    P_serial = prefix_sum_serial(A)
    end_serial = time.time()

    # Verificar se os resultados são iguais
    assert P_parallel == P_serial, "Os resultados não coincidem!"

    # Exibir tempos
    np.save("prefix_sum_parallel", P_parallel)
    print(f"Tempo (paralelo, {num_threads} threads): {end_parallel - start_parallel:.4f} segundos")
    print(f"Tempo (serial): {end_serial - start_serial:.4f} segundos")