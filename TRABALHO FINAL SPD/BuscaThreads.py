import time
import threading

def buscaGenoma(numThread, numLinhas, linha, resultados, lock):
    """
    Função que realiza a contagem das bases nucleotídicas em um intervalo específico de linhas do genoma.
        numThread (int): Número da thread atual.
        numLinhas (int): Número de linhas que cada thread deve processar.
        linha (list): Lista de linhas do arquivo genômico.
        resultados (dict): Dicionário compartilhado para armazenar as contagens das bases nucleotídicas.
        lock (Lock): Objeto de bloqueio para garantir exclusão mútua durante a atualização dos resultados.
    """

    contador = {'A': 0, 'T': 0, 'C': 0, 'G': 0}

    inicio = numThread * numLinhas
    fim = min((numThread + 1) * numLinhas, len(linha))

    # Percorre o intervalo de linhas atribuído à thread
    for i in range(inicio, fim):
        sequencia = linha[i].strip()
        if not sequencia.startswith('>'):
            # Conta as bases nucleotídicas na sequência atual
            for base in sequencia:
                base = base.upper()
                if base in contador:
                    contador[base] += 1

    # Atualiza os resultados globais com as contagens da thread atual
    with lock:
        resultados['A'] += contador['A']
        resultados['T'] += contador['T']
        resultados['C'] += contador['C']
        resultados['G'] += contador['G']

def exec():
    # Função principal que executa a contagem das bases nucleotídicas no arquivo genômico usando várias threads.

    inicio = time.perf_counter()
    
    qtdThread = 16

    caminho = "./GCF_000001735.4_TAIR10.1_genomic.fna"
    linha = []
    with open(caminho) as f:
        linha = f.readlines()

    # Calcula o número de linhas que cada thread deve processar
    numLinhas = (len(linha) + qtdThread - 1) // qtdThread

    # Dicionário compartilhado para armazenar as contagens das bases nucleotídicas
    resultados = {'A': 0, 'T': 0, 'C': 0, 'G': 0}
    
    # Objeto de bloqueio para garantir exclusão mútua ao atualizar os resultados
    lock = threading.Lock()

    threads = []
    for i in range(qtdThread):
        # Cria e inicia as threads para processar diferentes intervalos de linhas
        t = threading.Thread(target=buscaGenoma, args=(i, numLinhas, linha, resultados, lock))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # Imprime as contagens das bases nucleotídicas
    print("A:", resultados['A'])
    print("T:", resultados['T'])
    print("C:", resultados['C'])
    print("G:", resultados['G'])
    
    # Imprime informações adicionais
    print("\nTotal de linhas:", len(linha))
    print("Linhas por thread:", numLinhas)
    
    fim = time.perf_counter()
    tempo = fim - inicio
    print("\nTempo gasto: ", tempo, "segundos")

exec()
