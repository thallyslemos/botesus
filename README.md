# Botesus - Seu Assistente de Saúde em Vitória da Conquista

## Descrição

O Botesus é um chatbot desenvolvido como parte da avaliação da disciplina de Inteligência Artificial do IFBA. O objetivo deste projeto é fornecer aos cidadãos de Vitória da Conquista, Bahia, informações úteis e de fácil acesso sobre os estabelecimentos de saúde pública disponíveis na cidade.

O robô utiliza a base de dados do OpenSUS, que contém informações detalhadas sobre os estabelecimentos de saúde em todo o Brasil. Para este projeto, focamos nos dados relevantes para Vitória da Conquista.

## Funcionalidades

O Botesus é treinado para responder a uma variedade de perguntas sobre os estabelecimentos de saúde, incluindo:

*   **Localização:** "Onde encontro um posto de saúde no bairro X?"
*   **Endereço:** "Qual o endereço da UPA?"
*   **Contato:** "Qual o telefone do Posto de Saúde Y?"
*   **Horário de Funcionamento:** "Qual o horário de atendimento do estabelecimento Z?"
*   **Serviços:** "O estabelecimento X atende pelo SUS?"
*   **Informações por Município:** "Quantos hospitais existem em Vitória da Conquista?"

## Como Usar

### Pré-requisitos

- Python 3.x
- Pip

### Instalação

1.  Clone o repositório:
    ```bash
    git clone <url-do-repositorio>
    cd botesus
    ```

2.  Crie e ative um ambiente virtual:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Baixe o modelo de linguagem para o Spacy:**
    O ChatterBot utiliza a biblioteca Spacy, que precisa de um modelo de linguagem específico para o português.
    ```bash
    python3 -m spacy download pt_core_news_sm
    ```

### Preparando os Dados e Treinando o Modelo

Para que o Botesus possa responder às perguntas, ele precisa ser treinado com os dados dos estabelecimentos de saúde.

1.  **Preparação dos Dados:**
    Execute o script `preparar_dados.py` para processar os dados brutos do OpenSUS (arquivos JSON na pasta `assets/`) e gerar os arquivos de conversação para o treinamento.
    ```bash
    python3 preparar_dados.py
    ```
    Este script irá gerar um novo arquivo de conversas em `conversas/estabelecimentos_saude.json`.

2.  **Treinamento:**
    Execute o script `treinamento.py` para treinar o chatbot com as conversas geradas.
    ```bash
    python3 treinamento.py
    ```

### Executando o Botesus

Você pode interagir com o Botesus de duas formas:

1.  **Via Terminal:**
    ```bash
    python3 robo.py
    ```

2.  **Via Serviço Web (API):**
    ```bash
    python3 servico.py
    ```
    O serviço estará disponível em `http://localhost:6000`. Você pode fazer requisições para o endpoint `/resposta/<sua-mensagem>`.