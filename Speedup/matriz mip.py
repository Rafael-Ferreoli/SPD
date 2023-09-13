import numpy as np
from mpi4py import MPI
import time

def multiply_matrices(matrices, rank, size):
    num_matrices = len(matrices) #calcula o numero total de matrizes na lista
    chunk_size = num_matrices // size #calcula o tamanho do bloco de matrizes, divide o total de matrizes pelo numero de processos
    start = rank * chunk_size #determina o indice inicial do bloco que o processoal atual será responsavel por processar
    end = (rank + 1) * chunk_size #determina o indice final do bloco de matrizes

    for i in range(start, end):
        A, B = matrices[i]

        # Checando se as matrizes podem ser multiplicadas
        if A.shape[1] != B.shape[0]:
            print("As matrizes nao podem ser multiplicadas.")
            continue

        # Multiplicando as matrizes
        C = np.dot(A, B)

        # Exibindo o resultado da multiplicação
        print(f"Matriz resultante do par {i+1} no processo {rank}:")
        print(np.around(C, decimals=3))

if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Tamanho das matrizes
    n1, m1, n2, m2 = None, None, None, None

    if rank == 0:
        n1 = int(input("Digite o numero de colunas da matriz A: "))
        m1 = int(input("Digite o numero de linhas da matriz A: "))
        n2 = int(input("Digite o numero de colunas da matriz B: "))
        m2 = int(input("Digite o numero de linhas da matriz B: "))

    # Transmitir os tamanhos das matrizes para todos os outros processos
    n1 = comm.bcast(n1, root=0)
    m1 = comm.bcast(m1, root=0)
    n2 = comm.bcast(n2, root=0)
    m2 = comm.bcast(m2, root=0)

    # Lista para armazenar as matrizes
    matrizes = []

    # Gerando as matrizes aleatórias em um único processo
    if rank == 0: #evita diferentes conjuntos de matrizes e a duplicação de esforço pois a geração acontece só uma vez
        low, high = -9, 9
        for _ in range(20):
            A = np.random.randint(low=low, high=high+1, size=(m1, n1))
            B = np.random.randint(low=low, high=high+1, size=(m2, n2))
            matrizes.append((A, B)) #adiciona o par de matrizes na listra de matrizes i = 1 [a,b], i = 2 [a,b]...

    # Distribuindo as matrizes para todos os processos
    matrizes = comm.bcast(matrizes, root=0)

    # Multiplicando as matrizes usando MPI
    start_time = time.time()
    multiply_matrices(matrizes, rank, size)
    end_time = time.time()

    # Calculando o tempo de execução
    elapsed_time = end_time - start_time

    if rank == 0:
        average_elapsed_time = elapsed_time / 20
        print(f"Tempo de execucao: {elapsed_time} segundos\n")
        print(f"Media dos tempos de execucao: {average_elapsed_time} segundos")

    # Aguardando todos os processos finalizarem
    comm.Barrier()

    # Finalizando o programa
    if rank == 0:
        comm.send(None, dest=1, tag=1)  # Envia um sinal para o próximo processo

        for i in range(1, size):
            comm.recv(source=i, tag=2)  # Espera receber sinal de todos os outros processos

        print("Pressione ENTER para finalizar o programa.")
        input()
    else:
        comm.send(None, dest=(rank + 1) % size, tag=1)  # Envia um sinal para o próximo processo
        comm.recv(source=(rank - 1) % size, tag=1)  # Espera receber sinal do processo anterior
        comm.send(None, dest=0, tag=2)  # Envia sinal para o processo raiz


#mpiexec /np 5 python "matriz mip.py"