from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.languages import POR

import json

NOME_ROBO = "IFBABot"

CONVERSAS = [
    "./conversas/sistemas_de_informacao.json", 
    "./conversas/saudacoes.json", 
    "./conversas/informacoes_basicas.json"
]

def inicializar():
    inicializado, treinador = False, None

    try:
        robo = ChatBot(name=NOME_ROBO, tagger_language=POR)
        treinador = ListTrainer(robo)

        inicializado = True
    except Exception as e:
        print(f"ocorreu um erro inicializando o treinador: {str(e)}")

    return inicializado, treinador

def carregar_conversas():
    carregadas, conversas = False, []

    try:
        for arquivo_conversas in CONVERSAS:
            with open(arquivo_conversas, "r", encoding="utf-8") as arquivo:
                conversas_para_treinamento = json.load(arquivo)
                conversas.append(conversas_para_treinamento["conversas"])

                arquivo.close()


        carregadas = True
    except Exception as e:
        print(f"ocorreu um erro carregando as conversas: {str(e)}")

    return carregadas, conversas

def treinar(treinador, conversas):
    for conversa in conversas:
        for mensagens_resposta in conversa:
            mensagens = mensagens_resposta["mensagens"]
            resposta = mensagens_resposta["resposta"]

            for mensagem in mensagens:
                print(f"treinando o par mensagem/resposta: {mensagem} - {resposta}")

                treinador.train([mensagem.lower(), resposta])
    

if __name__ == "__main__":
    inicializado, treinador = inicializar()
    if inicializado:
        carregadas, conversas = carregar_conversas()

        if carregadas:
            if treinador and conversas:
                treinar(treinador, conversas)