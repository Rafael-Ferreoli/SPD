import Pyro4  # importa o módulo Pyro4 para criar um servidor de objetos distribuídos
import os  # importa o módulo os para executar comandos do sistema operacional
import time  # importa o módulo time para controlar o tempo de espera
import tempfile  # importa o módulo tempfile para criar arquivos temporários
from gtts import gTTS  # importa a classe gTTS da biblioteca gtts para converter texto em áudio
import threading  # importa o módulo threading para gerenciar threads de execução concorrente

# define uma classe para representar uma solicitação de conversão de texto em áudio
@Pyro4.expose
class Request:
    def __init__(self, username, text):
        self.username = username  # nome de usuário que fez a solicitação
        self.text = text  # texto a ser convertido em áudio
        
    def process(self):
        # converte o texto em áudio usando a biblioteca gTTS
        tts = gTTS(self.text, lang='pt-br')
        # salva o áudio em um arquivo temporário
        tts.save('audio.mp3')
        # reproduz o áudio usando o player padrão do sistema operacional
        os.startfile('audio.mp3', 'play')
        # espera um segundo para garantir que o áudio seja reproduzido completamente antes de remover o arquivo temporário
        time.sleep(1)
        # remove o arquivo temporário
        os.remove('audio.mp3')

# define uma classe para representar o servidor de conversão de texto em áudio
@Pyro4.expose
class TextToSpeech:

    def __init__(self):
        # armazena a lista de usuários autenticados
        self.authenticated_users = set()
        # armazena a lista de solicitações pendentes de conversão de texto em áudio
        self.requests = []
        # cria um objeto de bloqueio para garantir acesso exclusivo à lista de solicitações
        self.request_lock = threading.Lock()
        # cria uma thread separada para processar as solicitações pendentes em segundo plano
        self.request_thread = threading.Thread(target=self.process_requests)
        self.request_thread.start()

    def authenticate(self, username, password):
        # verifica se o nome de usuário e a senha fornecidos correspondem a um usuário válido
        # retorna True se a autenticação for bem-sucedida, caso contrário, False
        if username == "rafael" and password == "rafael123":
            # adiciona o usuário autenticado à lista de usuários autenticados
            self.authenticated_users.add(username)
            return True
        else:
            return False

    def convert_text_to_speech(self, username, text):
        # verifica se o usuário está autenticado
        if username in self.authenticated_users:
            # cria um novo objeto Request com as informações do usuário e do texto
            request = Request(username, text)
            # adiciona o objeto Request à lista de solicitações pendentes
            with self.request_lock:
                self.requests.append(request)
            return True
        else:
            return False

    def process_requests(self):
        # Executa um loop infinito para processar as solicitações de conversão de texto em fala.
        while True:
            # verifica se há solicitações pendentes
            with self.request_lock:
                if len(self.requests) == 0:
                    time.sleep(1)
                    continue
                # obtém a próxima solicitação na lista de solicitações
                request = self.requests[0]
                del self.requests[0]
            # processa a solicitação
            request.process()


daemon = Pyro4.Daemon()
tts = TextToSpeech()
uri = Pyro4.Daemon.serveSimple(
    {
        TextToSpeech: "text_to_speech"
    }, ns=False, daemon=daemon)
print(f"URI do servidor: {uri}")
daemon.requestLoop()
