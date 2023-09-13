import time
from mpi4py import MPI

def count_bases(linhas):
    resultados = {'A': 0, 'T': 0, 'C': 0, 'G': 0}

    for linha in linhas:
        sequencia = linha.strip()
        if not sequencia.startswith('>'):
            for base in sequencia:
                base = base.upper()
                if base in resultados:
                    resultados[base] += 1

    return resultados

def reduce_results(resultados):
    resultado_final = {'A': 0, 'T': 0, 'C': 0, 'G': 0}

    for resultado in resultados:
        for base in resultado:
            resultado_final[base] += resultado[base]

    return resultado_final

def exec():
    inicio_execucao = time.time()

    caminho = "./GCF_000001735.4_TAIR10.1_genomic.fna"
    linha = []
    with open(caminho) as f:
        linha = f.readlines()

    comm = MPI.COMM_WORLD
    num_processos = comm.Get_size()
    rank = comm.Get_rank()

    num_linhas = len(linha)
    linhas_por_processo = num_linhas // num_processos

    # Divisão das linhas entre os processos
    inicio = rank * linhas_por_processo
    fim = (rank + 1) * linhas_por_processo

    # O último processo pode ter algumas linhas adicionais
    if rank == num_processos - 1:
        fim = num_linhas

    linhas_processo = linha[inicio:fim]

    # Contagem das bases nucleotídicas para cada processo
    resultados_local = count_bases(linhas_processo)

    # Redução dos resultados de cada processo
    resultados_globais = comm.gather(resultados_local, root=0)

    if rank == 0:
        # Processo raiz combina os resultados finais
        resultado_final = reduce_results(resultados_globais)

        # Imprime os resultados finais
        print("A:", resultado_final['A'])
        print("T:", resultado_final['T'])
        print("C:", resultado_final['C'])
        print("G:", resultado_final['G'])

        print("\nTotal de linhas:", num_linhas)
        print("Linhas por processo:", linhas_por_processo)

        fim_execucao = time.time()
        tempo_execucao = fim_execucao - inicio_execucao
        print("\nTempo gasto: {:.5f} segundos".format(tempo_execucao))

if __name__ == "__main__":
    exec()

#mpiexec /np 16 python "BuscaMPI.py"