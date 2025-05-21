# 2) Dado um vetor de 50.000 inteiros. Desenvolver um programa paralelo que ordene esse vetor, com um speedup maior ou igual a 1,7
#    Retorno: vetor ordenado

from concurrent.futures import ProcessPoolExecutor
import numpy as np
import time

def sort_serial(array):
    if len(array) <= 1:
        return array
    
    mid = len(array) // 2
    left = sort_serial(array[:mid])
    right = sort_serial(array[mid:])
    
    return merge(left, right)


def sort_paralelo(array, depth=0, max_depth=1):
    if len(array) <= 1:
        return array
    
    if depth >= max_depth:
        return sort_serial(array)