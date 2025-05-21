''' 
A) Multiplicação de duas Matrizes  A 3.000X3.000 e B 3.000X3.000;

retorno: Matrix C com o resultado da multiplicação
'''

from concurrent.futures import ProcessPoolExecutor
import numpy as np
import time

def cria_matriz_resultado(matriz_A, matriz_B):
    if (len(matriz_A[0]) != len(matriz_B)):
        print("nao da")
        return None

    # Matriz resultado preenchida com zeros
    return np.zeros((len(matriz_A), len(matriz_B[0])))

def multiplicarMatrizserial(matriz_A, matriz_B, matriz_C):
    num_row = len(matriz_A)
    num_col = len(matriz_B[0])
    
    # Cálculo de cada elemento da matriz resultante
    for i in range(num_row):
        for j in range(num_col):
            soma = 0
            for k in range (len(matriz_B)):
                soma += matriz_A[i][k] * matriz_B[k][j]
            matriz_C[i][j] = soma

    return matriz_C


def main():
    NUM_WORKERS = 4
    
    matriz_C = cria_matriz_resultado(matriz_A, matriz_B)

    startSerial = time.time()
    matriz_resultante = multiplicarMatrizserial(matriz_A, matriz_B, matriz_C)
    endSerial = time.time()
    
    print(f"Tempo de execução serial: {endSerial - startSerial:.4f} segundos")
 

def worker(args): # lembrando, n podiamos usar o C como prametro pq ele COPIA (ficava tudo zerado)
    A, B, lin = args
    result_row = []
    for col in range(len(B[0])):
        result = 0
        for i in range(len(A[0])):
            result += A[lin][i] * B[i][col]
        result_row.append(result)
    return result_row

def main2():
    QBRANDO_PC_DA_ANJU = 4

    NUM_LINHAS = 1000
    NUM_COLUNAS = 1000
    matriz_A = np.arange(NUM_LINHAS*NUM_COLUNAS).reshape(NUM_LINHAS,NUM_COLUNAS)
    matriz_B = matriz_A.copy()

    with ProcessPoolExecutor(max_workers=QBRANDO_PC_DA_ANJU) as pool:
        results = pool.map(
            worker, 
            [(matriz_A, matriz_B, linha) for linha in range(matriz_A.shape[0])]
        )

    C = np.zeros((matriz_A.shape[0], matriz_B.shape[1]))
    for i, result in enumerate(results):
        C[i] = result


if __name__ == "__main__":
    main()
    start_time = time.time()
    main2()
    end_time = time.time()
    print(f"Tempo total de execução 2: {end_time - start_time:.4f} segundos")