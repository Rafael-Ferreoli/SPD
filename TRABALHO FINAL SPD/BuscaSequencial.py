import time

def buscaGenoma(linha, resultados):
    """
    Função que realiza a contagem das bases nucleotídicas em todas as linhas do genoma.
        linha (list): Lista de linhas do arquivo genômico.
        resultados (dict): Dicionário para armazenar as contagens das bases nucleotídicas.
    """

    for sequencia in linha: #Itera sobre cada elemento da lista linha, que representa as linhas do arquivo genômico.
        sequencia = sequencia.strip() #Remove espaços em branco extras no início e no final da sequência de nucleotídeos.
        if not sequencia.startswith('>'): #Verifica se a sequência não começa com o caractere '>', o que indica que é um cabeçalho de linha e não uma sequência de nucleotídeos.
            for base in sequencia: #Itera sobre cada caractere na sequência de nucleotídeos.
                base = base.upper() #Converte o caractere em maiúsculo para garantir a correspondência correta no dicionário resultados.
                if base in resultados: # Converte o caractere em maiúsculo para garantir a correspondência correta no dicionário resultados.
                    resultados[base] += 1 # Incrementa a contagem da base nucleotídica correspondente no dicionário resultados.

def exec():
    # Função principal que executa a contagem das bases nucleotídicas no arquivo genômico de forma sequencial.

    inicio = time.perf_counter()
    
    caminho = "./GCF_000001735.4_TAIR10.1_genomic.fna"
    linha = []
    with open(caminho) as f:
        linha = f.readlines()

    # Dicionário para armazenar as contagens das bases nucleotídicas
    resultados = {'A': 0, 'T': 0, 'C': 0, 'G': 0}

    buscaGenoma(linha, resultados)

    # Imprime as contagens das bases nucleotídicas
    print("A:", resultados['A'])
    print("T:", resultados['T'])
    print("C:", resultados['C'])
    print("G:", resultados['G'])
    
    # Imprime informações adicionais
    print("\nTotal de linhas:", len(linha))
    
    fim = time.perf_counter()
    tempo = fim - inicio
    print("\nTempo gasto: ", tempo, "segundos")

exec()
