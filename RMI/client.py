import Pyro4
import time
import sys

uri = input("Entre com a URI do servidor: ")
username = input("Entre com o nome de usuário: ")
password = input("Entre com a senha: ")

tts = None
for i in range(3):
    try:
        tts = Pyro4.Proxy(uri)
        break
    except Pyro4.errors.CommunicationError as e:
        print(f"Tentativa {i+1} de conexão falhou: {e}")
        time.sleep(5)
    except Pyro4.errors.PyroError as e:
        print(f"URI inválido: {e}")
        sys.exit()

if tts is None:
    print("Não foi possível conectar ao servidor.")
else:
    try:
        if tts.authenticate(username, password):
            while True:
                text = input("Entre com o texto que deseja converter em áudio ou digite 'exit' para sair: ")
                if text == "exit":
                    break
                if tts.convert_text_to_speech(username, text):
                    print("Áudio gerado com sucesso!")
                else:
                    print("Não foi possível gerar o áudio.")
        else:
            print("Falha na autenticação!")
    except Pyro4.errors.ConnectionClosedError:
        print("Conexão com o servidor perdida durante a autenticação.")
    except Pyro4.errors.CommunicationError as e:
        if "WinError 10061" in str(e):
            print("Não foi possível conectar ao servidor. Certifique-se de que o serviço Pyro4 está em execução no endereço especificado.")
        else:
            print(f"Erro de comunicação: {e}")
