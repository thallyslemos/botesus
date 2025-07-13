from chatterbot import ChatBot
from chatterbot.languages import POR

NOME_ROBO = "Botesus"
CONFIANCA_MINIMA = 0.85

def inicializar():
    inicializado, robo = False, None

    try:
        robo = ChatBot(NOME_ROBO, read_only=True, logic_adapters=[{
            "import_path": "chatterbot.logic.BestMatch"
        }])

        inicializado = True
    except Exception as e:
        print(f"Erro ao inicializar o {NOME_ROBO}: {str(e)}")
        
    return inicializado, robo

# 🤖👤
def get_resposta(robo, mensagem):
    resposta = robo.get_response(mensagem.lower().strip())

    return resposta.text, resposta.confidence


def executar_robo(robo):
    print("Olá, sou o Botesus, seu assistente do cadastro nacional de estabelecimentos de saúde, deseja saber algo?")

    while True:
        try:
            mensagem = input("👤 ")
            resposta, confianca = get_resposta(robo, mensagem)

            if confianca >= CONFIANCA_MINIMA:
                print(f"🤖 {resposta} [confiança: {confianca}]")
            else:
                print(f"🤖 Desculpe, não encontrei uma resposta para isso. [confiança: {confianca}]")
        except (KeyboardInterrupt, EOFError, SystemExit):
            break


if __name__ == "__main__":
    inicializado, robo = inicializar()
    if inicializado:
        executar_robo(robo)