import numpy
import multiprocessing
import time

vetor = numpy.random.randint(0, 100, size=6000000)

def eh_primo(numero):
    if numero <= 1:
        return False
    for i in range(2, int(numero ** 0.5) + 1):
        if numero % i == 0:
            return False
    
    return True

###### SERIAL ######
inicio = time.time()
primos = []
for number in vetor:
    if eh_primo(number):
        primos.append(int(number))

final = time.time()

# print(primos)
print(f"Tempo de execução SERIAL: {final - inicio:.4f} segundos")

##### PARALELO (2) #####
executables = []
inicio = time.time()
for i in range (2):
    