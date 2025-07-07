from chatterbot.logic import LogicAdapter
import json

class AdaptadorBotesus(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.estabelecimentos = self._carregar_estabelecimentos()

    def _carregar_estabelecimentos(self):
        with open('conversas/estabelecimentos_saude.json', 'r', encoding='utf-8') as f:
            return json.load(f)['conversas']

    def can_process(self, statement):
        # Por enquanto, vamos tentar processar todas as mensagens
        # A lógica de decisão pode ser mais sofisticada depois
        return True

    def process(self, input_statement, additional_response_selection_parameters):
        from chatterbot.conversation import Statement

        nome_estabelecimento_pesquisado = input_statement.text.strip()

        melhor_correspondencia = None
        maior_confianca = 0.0

        # Busca por uma correspondência exata (ou quase exata) no nome fantasia
        for est in self.estabelecimentos:
            # A "pergunta" é o nome do estabelecimento
            pergunta = est["mensagens"][0] 
            
            if nome_estabelecimento_pesquisado.lower() == pergunta.lower():
                melhor_correspondencia = est
                maior_confianca = 1.0
                break # Encontrou correspondência exata

        if melhor_correspondencia:
            resposta = Statement(text=melhor_correspondencia['resposta'])
            resposta.confidence = maior_confianca
            return resposta
        else:
            # Se não encontrar, retorna uma resposta com confiança zero
            resposta = Statement(text="")
            resposta.confidence = 0.0
            return resposta
