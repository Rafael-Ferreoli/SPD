import numpy as np
import time

def second_largest_smallest(lst):
    # Ordenando a lista em ordem crescente
    sorted_lst = sorted(lst)
    # Retornando o segundo menor e segundo maior valor
    return sorted_lst[1], sorted_lst[-2]

# Tamanho das matrizes
n1 = int(input("Digite o número de colunas da matriz A: "))
m1 = int(input("Digite o número de linhas da matriz A: "))
n2 = int(input("Digite o número de colunas da matriz B: "))
m2 = int(input("Digite o número de linhas da matriz B: "))

# Lista para armazenar as matrizes
matrizes = []

# Gerando as matrizes aleatórias
low, high = -9, 9
A = np.random.randint(low=low, high=high+1, size=(m1, n1))
B = np.random.randint(low=low, high=high+1, size=(m2, n2))

# Armazenando as matrizes na lista
matrizes.append((A, B))

# Multiplicando as matrizes e medindo o tempo de execução
elapsed_times = []

for i in range(20):
    start_time = time.time()

    for j in range(len(matrizes)):
        A, B = matrizes[j]
        
        # Exibindo as matrizes geradas
        print(f"\nMatriz A do par {j+1}:")
        print(A)
        print(f"Matriz B do par {j+1}:")
        print(B)
        
        # Checando se as matrizes podem ser multiplicadas
        if A.shape[1] != B.shape[0]:
            print("As matrizes não podem ser multiplicadas.")
            continue

        # Multiplicando as matrizes
        C = np.dot(A, B)

        # Exibindo o resultado da multiplicação
        print(f"Matriz resultante do par {j+1}:")
        print(np.around(C, decimals=3))

    # Calculando e armazenando o tempo de execução da iteração
    end_time = time.time()
    elapsed_time = end_time - start_time
    elapsed_times.append(elapsed_time)
    print(f"Tempo de execução da iteração {i+1}: {elapsed_time} segundos\n")

# Calculando e exibindo a soma, média, maior e menor tempo de execução
total_elapsed_time = sum(elapsed_times)
average_elapsed_time = total_elapsed_time / 20
max_elapsed_time = max(elapsed_times)
min_elapsed_time = min(elapsed_times)
average_elapsed_time_min_max = (total_elapsed_time - max_elapsed_time - min_elapsed_time) / 18
second_min_elapsed_time, second_max_elapsed_time = second_largest_smallest(elapsed_times)

print(f"Soma dos tempos de execução: {total_elapsed_time} segundos")
print(f"Média dos tempos de execução: {average_elapsed_time} segundos")
print(f"Média dos tempos de execução sem Min e Max: {average_elapsed_time_min_max} segundos")
print(f"Maior tempo de execução: {max_elapsed_time} segundos")
print(f"Segundo maior tempo de execução: {second_max_elapsed_time} segundos")
print(f"Menor tempo de execução: {min_elapsed_time} segundos")
print(f"Segundo menor tempo de execução: {second_min_elapsed_time} segundos")


# Aguardando input para finalizar o programa
input("Pressione ENTER para finalizar o programa.")
