import numpy as np
import threading
import time

def multiply_matrices(matrices, start, end):
    for i in range(start, end):
        A, B = matrices[i]
        '''
        # Exibindo as matrizes geradas
        print(f"\nMatriz A do par {i+1}:")
        print(A)
        print(f"Matriz B do par {i+1}:")
        print(B)
        '''
        # Checando se as matrizes podem ser multiplicadas
        if A.shape[1] != B.shape[0]:
            print("As matrizes não podem ser multiplicadas.")
            continue

        # Multiplicando as matrizes
        C = np.dot(A, B)
        
        # Exibindo o resultado da multiplicação
        print(f"Matriz resultante do par {i+1}:")
        print(np.around(C, decimals=3))
        
def multiply_matrices_threaded(matrices):
    # Número de matrizes a serem multiplicadas
    num_matrices = len(matrices)

    # Dividindo o trabalho em duas threads, cada uma responsável por 10 iterações
    thread1 = threading.Thread(target=multiply_matrices, args=(matrices, 0, 10))
    thread2 = threading.Thread(target=multiply_matrices, args=(matrices, 10, 20))

    # Iniciando as threads
    thread1.start()
    thread2.start()

    # Esperando as threads terminarem
    thread1.join()
    thread2.join()

# Tamanho das matrizes
n1 = int(input("Digite o número de colunas da matriz A: "))
m1 = int(input("Digite o número de linhas da matriz A: "))
n2 = int(input("Digite o número de colunas da matriz B: "))
m2 = int(input("Digite o número de linhas da matriz B: "))

# Lista para armazenar as matrizes
matrizes = []

# Gerando as matrizes aleatórias
low, high = -9, 9
for i in range(20):
    A = np.random.randint(low=low, high=high+1, size=(m1, n1))
    B = np.random.randint(low=low, high=high+1, size=(m2, n2))
    matrizes.append((A, B))

# Multiplicando as matrizes e medindo o tempo de execução
elapsed_times = []

start_time = time.time()

# Multiplicando as matrizes usando threads
multiply_matrices_threaded(matrizes)

# Calculando e armazenando o tempo de execução
end_time = time.time()
elapsed_time = end_time - start_time
elapsed_times.append(elapsed_time)
print(f"Tempo de execução: {elapsed_time} segundos\n")

# Calculando e exibindo a soma, média, maior e menor tempo de execução
total_elapsed_time = sum(elapsed_times)
average_elapsed_time = total_elapsed_time /20

print(f"Soma dos tempos de execução: {total_elapsed_time} segundos")
print(f"Média dos tempos de execução: {average_elapsed_time} segundos")


# Aguardando input para finalizar o programa
input("Pressione ENTER para finalizar o programa.")
