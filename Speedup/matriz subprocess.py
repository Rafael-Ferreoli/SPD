import subprocess
import numpy as np
import time

def random_matrix(n, m):
    # Função que gera uma matriz aleatória de tamanho n x m com valores inteiros entre -9 e 9
    return np.random.randint(low=-9, high=10, size=(n, m))

def multiply_matrices(a, b):
    # Função que multiplica duas matrizes a e b usando a função dot() do numpy
    return np.dot(a, b)

def test_execution_time():
    # Solicita ao usuário as dimensões das matrizes
    m1 = int(input("Digite o número de colunas da primeira matriz: "))
    n1 = int(input("Digite o número de linhas da primeira matriz: "))
    m2 = int(input("Digite o número de colunas da segunda matriz: "))
    n2 = int(input("Digite o número de linhas da segunda matriz: "))

    # Gera duas matrizes aleatórias com as dimensões especificadas pelo usuário
    A = random_matrix(n1, m1)
    B = random_matrix(n2, m2)

    # Verifica se as matrizes podem ser multiplicadas
    if m1 != n2:
        print("Erro: as matrizes não podem ser multiplicadas.")
        return

    # Inicia o timer
    start_time = time.time()

    # Executa a multiplicação usando um subprocesso
    # O comando executa o código Python inline que importa a função multiply_matrices e as matrizes A e B geradas anteriormente,
    # realiza a multiplicação e imprime o resultado. O resultado é capturado e impresso no final da função.
    command = f"python -c \"import numpy as np; from __main__ import multiply_matrices; A = np.array({A.tolist()}); B = np.array({B.tolist()}); C = multiply_matrices(A, B); print('Matriz resultante:'); print(C);\""
    subprocess.run(command, shell=True)

    # Finaliza o timer e imprime o tempo decorrido
    elapsed_time = time.time() - start_time
    print(f"Tempo de execução: {elapsed_time:.4f} segundos")

test_execution_time()

# Aguardando input para finalizar o programa
input("Pressione ENTER para finalizar o programa.")