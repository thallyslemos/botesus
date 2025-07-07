import unittest
import json
from robo import *

# Carrega as conversas para usar nos testes
with open('conversas/estabelecimentos_saude.json', 'r', encoding='utf-8') as f:
    ESTABELECIMENTOS = json.load(f)['conversas']

with open('conversas/saudacoes.json', 'r', encoding='utf-8') as f:
    SAUDACOES = json.load(f)['conversas']

class TesteBotesus(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.inicializado, cls.robo = inicializar()

    def testar_00_inicializado(self):
        self.assertTrue(self.inicializado)

    def testar_01_saudacoes(self):
        # Testa a primeira saudação de cada bloco no JSON
        for bloco in SAUDACOES:
            saudacao = bloco["mensagens"][0]
            resposta_esperada = bloco["resposta"]
            
            print(f"Testando a saudação: {saudacao}")
            resposta, confianca = get_resposta(self.robo, saudacao)
            self.assertGreaterEqual(confianca, CONFIANCA_MINIMA, f"Confiança baixa para '{saudacao}'")
            self.assertEqual(resposta, resposta_esperada)

    def testar_02_estabelecimentos_encontrados(self):
        # Testa alguns estabelecimentos para garantir que o adaptador lógico os encontre
        estabelecimentos_para_testar = ESTABELECIMENTOS[:3] # Testa os 3 primeiros

        for est in estabelecimentos_para_testar:
            nome_estabelecimento = est["mensagens"][0]
            resposta_esperada = est["resposta"]

            print(f"Testando o estabelecimento: {nome_estabelecimento}")
            resposta, confianca = get_resposta(self.robo, nome_estabelecimento)
            self.assertEqual(confianca, 1.0, f"O adaptador lógico deveria retornar confiança 1.0 para '{nome_estabelecimento}'")
            self.assertEqual(resposta, resposta_esperada)

    def testar_03_estabelecimento_nao_encontrado(self):
        mensagem = "Hospital que não existe em VCA"
        resposta_esperada = "Desculpe, não entendi. Poderia repetir a pergunta?" # Resposta padrão do BestMatch

        print(f"Testando estabelecimento não existente: {mensagem}")
        resposta, confianca = get_resposta(self.robo, mensagem)
        # A confiança será baixa, e a resposta será a padrão
        self.assertLess(confianca, 0.90)
        self.assertEqual(resposta, resposta_esperada)

if __name__ == "__main__":
    unittest.main()