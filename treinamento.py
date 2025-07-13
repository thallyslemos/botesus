from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.languages import POR

import json
import os

NOME_ROBO = "Botesus"

# Apenas as conversas relevantes para o Botesus
CONVERSAS = [
    "./conversas/saudacoes.json", 
    "./conversas/informacoes_basicas.json",
    "./conversas/estabelecimentos_saude.json"
]

def inicializar():
    inicializado, treinador = False, None

    try:
        robo = ChatBot(name=NOME_ROBO, tagger_language=POR)
        treinador = ListTrainer(robo)

        inicializado = True
    except Exception as e:
        print(f"Ocorreu um erro ao inicializar o treinador: {str(e)}")

    return inicializado, treinador

def carregar_conversas():
    carregadas, conversas = False, []

    try:
        for arquivo_conversas in CONVERSAS:
            if not os.path.exists(arquivo_conversas):
                print(f"Aviso: Arquivo de conversa não encontrado: {arquivo_conversas}. Pulando.")
                continue

            with open(arquivo_conversas, "r", encoding="utf-8") as arquivo:
                print(f"Carregando conversas de: {arquivo_conversas}")
                conversas_para_treinamento = json.load(arquivo)
                conversas.append(conversas_para_treinamento["conversas"])
                arquivo.close()

        carregadas = True
    except Exception as e:
        print(f"Ocorreu um erro carregando as conversas: {str(e)}")

    return carregadas, conversas

def treinar(treinador, conversas):
    total_treinado = 0
    for conversa in conversas:
        for mensagens_resposta in conversa:
            mensagens = mensagens_resposta["mensagens"]
            resposta = mensagens_resposta["resposta"]

            for mensagem in mensagens:
                # print(f"Treinando o par: {mensagem} -> {resposta}")
                treinador.train([mensagem.lower(), resposta])
                total_treinado += 1
    print(f"Total de {total_treinado} pares de mensagem/resposta treinados.")
    

if __name__ == "__main__":
    print("Iniciando o processo de treinamento...")
    inicializado, treinador = inicializar()
    if inicializado:
        carregadas, conversas = carregar_conversas()

        if carregadas and conversas:
            treinar(treinador, conversas)
            print("Treinamento concluído com sucesso!")
        else:
            print("Nenhuma conversa para treinar. Verifique os arquivos em ./conversas/")