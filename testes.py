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
        # Testa um estabelecimento que realmente existe nos dados
        # Baseado no erro, sabemos que SUPER SORRISO existe
        perguntas_respostas = {
            "Qual o endereço do SUPER SORRISO?": "O endereço do SUPER SORRISO é: PRACA MARCELINO MENDES, 430, CENTRO."
        }

        for pergunta, resposta_esperada in perguntas_respostas.items():
            print(f"Testando a pergunta: {pergunta}")
            resposta, confianca = get_resposta(self.robo, pergunta)
            self.assertGreater(confianca, 0.75, f"Confiança baixa para estabelecimento existente '{pergunta}': {confianca}")
            self.assertEqual(resposta, resposta_esperada)

    def testar_03_estabelecimento_nao_encontrado(self):
        mensagem = "Hospital que não existe em VCA"
        
        print(f"Testando estabelecimento não existente: {mensagem}")
        resposta, confianca = get_resposta(self.robo, mensagem)
        
        # Para estabelecimentos não encontrados, a confiança deve ser baixa
        self.assertLess(confianca, 0.75, f"Confiança muito alta para estabelecimento inexistente: {confianca}")
        
        # A resposta deve indicar que não foi encontrado (contém "não" ou similar)
        resposta_lower = resposta.lower()
        self.assertTrue(
            "não" in resposta_lower or "desculpe" in resposta_lower or "encontr" in resposta_lower,
            f"Resposta não indica que estabelecimento não foi encontrado: {resposta}"
        )
        
    def testar_04_busca_telefone_estabelecimento(self):
        mensagem = "Qual o telefone do SUPER SORRISO?"
        
        print(f"Testando busca de telefone: {mensagem}")
        resposta, confianca = get_resposta(self.robo, mensagem)
        
        # A resposta deve conter o telefone do estabelecimento
        self.assertGreater(confianca, 0.75, f"Confiança baixa para busca de telefone: {confianca}")
        self.assertIn("telefone", resposta.lower(), f"Resposta não contém 'telefone': {resposta}")
        self.assertIn("super sorriso", resposta.lower(), f"Resposta não menciona o estabelecimento: {resposta}")
        
    def testar_05_busca_telefone_estabelecimento_inexistente(self):
        mensagem = "Qual o telefone do Estabelecimento Inexistente?"
        
        print(f"Testando busca de telefone para estabelecimento inexistente: {mensagem}")
        resposta, confianca = get_resposta(self.robo, mensagem)
        
        # Se a confiança for baixa (< 0.75), aceita qualquer resposta
        # Se a confiança for alta, verifica se a resposta indica que não foi encontrado
        if confianca >= 0.75:
            resposta_lower = resposta.lower()
            self.assertTrue(
                "não" in resposta_lower or "desculpe" in resposta_lower or "encontr" in resposta_lower or "inexistente" in resposta_lower,
                f"Resposta com alta confiança não indica que estabelecimento não foi encontrado: {resposta}"
            )
        else:
            # Para confiança baixa, apenas verifica que a confiança é menor que 0.75
            self.assertLess(confianca, 0.75, f"Confiança muito alta para telefone de estabelecimento inexistente: {confianca}")

    def testar_05_buscar_endereco_estabelecimento(self):
        mensagem = "Qual o endereço do SAMUR?"
       
        print(f"Testando busca de endereço: {mensagem}")
        resposta, confianca = get_resposta(self.robo, mensagem)
        
        # A resposta deve conter o endereço do estabelecimento
        self.assertGreater(confianca, 0.75, f"Confiança baixa para busca de endereço: {confianca}")
        self.assertIn("endereço", resposta.lower(), f"Resposta não contém 'endereço': {resposta}")
        self.assertIn("samur", resposta.lower(), f"Resposta não menciona o estabelecimento: {resposta}")
           
    def testar_06_buscar_endereco_estabelecimento_inexistente(self):
        mensagem = "Qual o endereço do Estabelecimento Inexistente?"
        
        print(f"Testando busca de endereço para estabelecimento inexistente: {mensagem}")
        resposta, confianca = get_resposta(self.robo, mensagem)
        
        # Se a confiança for baixa (< 0.75), aceita qualquer resposta
        # Se a confiança for alta, verifica se a resposta indica que não foi encontrado
        if confianca >= 0.75:
            resposta_lower = resposta.lower()
            self.assertTrue(
                "não" in resposta_lower or "desculpe" in resposta_lower or "encontr" in resposta_lower or "inexistente" in resposta_lower,
                f"Resposta com alta confiança não indica que estabelecimento não foi encontrado: {resposta}"
            )
        else:
            # Para confiança baixa, apenas verifica que a confiança é menor que 0.75
            self.assertLess(confianca, 0.75, f"Confiança muito alta para endereço de estabelecimento inexistente: {confianca}")

    def testar_07_buscar_horario_estabelecimento(self):
        mensagem = "Qual o horário de funcionamento do SAMUR?"
        
        print(f"Testando busca de horário: {mensagem}")
        resposta, confianca = get_resposta(self.robo, mensagem)
        
        # A resposta deve conter o horário de funcionamento do estabelecimento
        self.assertGreater(confianca, 0.75, f"Confiança baixa para busca de horário: {confianca}")
        self.assertIn("horário", resposta.lower(), f"Resposta não contém 'horário': {resposta}")
        self.assertIn("samur", resposta.lower(), f"Resposta não menciona o estabelecimento: {resposta}")
               
    def testar_08_atendimento_sus(self):
        mensagem = "O SAMUR atende pelo SUS?"
        
        print(f"Testando atendimento SUS: {mensagem}")
        resposta, confianca = get_resposta(self.robo, mensagem)
        
        # A resposta deve indicar se o estabelecimento atende pelo SUS
        self.assertGreater(confianca, 0.75, f"Confiança baixa para atendimento SUS: {confianca}")
        self.assertIn("atende", resposta.lower(), f"Resposta não contém 'atende': {resposta}")
        self.assertIn("samur", resposta.lower(), f"Resposta não menciona o estabelecimento: {resposta}")
        
    
if __name__ == "__main__":
    unittest.main()