import unittest
from robo import *

class TesteSaudacoes(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.inicializado, self.robo = inicializar()

    def testar_00_inicializado(self):
        self.assertTrue(self.inicializado)

    def testar_01_oi_ola(self):
        saudacoes = ["oi", "olá", "oi, tudo bem?"]

        for saudacao in saudacoes:
            print(f"testando a saudação: {saudacao}")

            resposta, confianca = get_resposta(self.robo, saudacao)
            self.assertGreaterEqual(confianca, CONFIANCA_MINIMA)
            self.assertIn("sou o IFBABot, robô de atendimento do IFBA", resposta)

    def testar_02_variabilidades(self):
        saudacoes = ["como vai?", "olá, como vai?", "olá, tudo bem?", "tudo bem?"]

        for saudacao in saudacoes:
            print(f"testando: {saudacao}")

            resposta, confianca = get_resposta(self.robo, saudacao)
            self.assertGreaterEqual(confianca, CONFIANCA_MINIMA)
            self.assertIn("sou o IFBABot, robô de atendimento do IFBA", resposta)

class TesteInformacoesBasicas(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.inicializado, self.robo = inicializar()

    def testar_00_inicializado(self):
        self.assertTrue(self.inicializado)

    def testar_01_localizacao(self):

        mensagens = [ "onde o ifba está localizado?", "onde vocês estão localizados?", "onde vocês funcionam?" ]

        for mensagem in mensagens:
            print(f"testando: {mensagem}")

            resposta = self.robo.get_response(mensagem)
            self.assertGreaterEqual(resposta.confidence, CONFIANCA_MINIMA)
            self.assertIn("o ifba fica localizado na avenida sérgio vieira de mello", resposta.text.lower())

    def testar_02_horarios_de_funcionamento(self):
        mensagens = [ "qual é o horário de funcionamento?", "que horas o ifba fica aberto?", "que horas o ifba funciona?" ]

        for mensagem in mensagens:
            print(f"testando: {mensagem}")

            resposta = self.robo.get_response(mensagem)
            self.assertGreaterEqual(resposta.confidence, CONFIANCA_MINIMA)          

class TesteSistemasDeInformacao(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.inicializado, self.robo = inicializar()

    def testar_00_inicializado(self):
        self.assertTrue(self.inicializado)

    def testar_01_sobre_o_curso(self):
        mensagens = [ "o que é o curso?", "como é o curso?" ]

        for mensagem in mensagens:
            print(f"testando: {mensagem}")

            resposta = self.robo.get_response(mensagem)
            self.assertGreaterEqual(resposta.confidence, CONFIANCA_MINIMA)
            self.assertIn("o curso serve para formar profissionais capazes de administrar o fluxo de informações geradas e distribuídas por redes de computadores dentro e fora de uma organização", resposta.text.lower())

    def testar_02_duracao_do_curso(self):
        mensagens = [ "quanto tempo dura o curso?", "quanto tempo o curso dura" ]

        for mensagem in mensagens:
            print(f"testando: {mensagem}")

            resposta = self.robo.get_response(mensagem)
            self.assertGreaterEqual(resposta.confidence, CONFIANCA_MINIMA)
            self.assertIn("o curso dura 4 anos ou 8 semestres", resposta.text.lower())


if __name__ == "__main__":
    unittest.main()