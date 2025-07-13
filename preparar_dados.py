import json
import os
import argparse
import time

# --- Constantes ---
ARQUIVOS_DADOS_ENTRADA = [
    "./assets/cnes_estabelecimentos_00001.json",
    "./assets/cnes_estabelecimentos_00002.json"
]
# Usaremos o arquivo de exemplo se os principais não existirem
ARQUIVO_EXEMPLO = "./assets/exemplo_estabelecimentos.json"
ARQUIVO_DADOS_SAIDA = "./conversas/estabelecimentos_saude.json"

def carregar_estabelecimentos(caminhos_arquivos):
    """
    Carrega estabelecimentos de uma lista de arquivos JSON e os entrega
    um por um, de forma contínua, usando um gerador.
    """
    arquivos_reais = [p for p in caminhos_arquivos if os.path.exists(p)]
    if not arquivos_reais:
        print("Aviso: Arquivos de dados principais não encontrados. Usando arquivo de exemplo.")
        if os.path.exists(ARQUIVO_EXEMPLO):
            arquivos_reais = [ARQUIVO_EXEMPLO]
        else:
            print(f"Erro: Arquivo de exemplo também não encontrado em {ARQUIVO_EXEMPLO}")
            return

    for caminho in arquivos_reais:
        print(f"Processando o arquivo: {caminho}")
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                dados = json.load(f)
                if isinstance(dados, list):
                    # O gerador agora itera aqui dentro e entrega cada item
                    for est in dados:
                        yield est
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Erro ao processar o arquivo {caminho}: {e}")
            continue

def mapear_gestao(codigo):
    """Traduz o código de gestão para um texto descritivo."""
    mapa = {
        "M": "Municipal",
        "E": "Estadual",
        "D": "Dupla (Estadual e Municipal)",
        "S": "Sem gestão",
        "Z": "Não informada"
    }
    return mapa.get(codigo, "Não informada")

def gerar_conversas(estabelecimentos, codigo_ibge=None):
    """
    Gera uma estrutura de conversas para o ChatterBot a partir de um
    fluxo de estabelecimentos.
    """
    conversas = {"conversas": []}
    count = 0
    print(f"Filtrando e gerando conversas... (IBGE: {codigo_ibge or 'Todos'})")

    # Loop foi simplificado para uma única iteração, como deveria ser.
    for est in estabelecimentos:
        if not isinstance(est, dict) or not est.get("NO_FANTASIA"):
            continue

        if codigo_ibge and est.get("CO_IBGE") != codigo_ibge:
            continue

        count += 1
        nome = est.get("NO_FANTASIA", "Nome não informado")
        
        # Informações de Endereço
        logradouro = est.get("NO_LOGRADOURO", "")
        numero = est.get("NU_ENDERECO", "s/n")
        bairro = est.get("NO_BAIRRO", "")
        endereco_completo = f"{logradouro}, {numero}, {bairro}".strip(", ")
        if endereco_completo:
            conversas["conversas"].append({
                "mensagens": [
                    f"Qual o endereço do {nome}?", 
                    f"Onde fica o {nome}?", 
                    f"Onde está localizado o {nome}?"
                ],
                "resposta": f"O endereço do {nome} é: {endereco_completo}."
            })

        # Informações de Contato
        telefone = est.get("NU_TELEFONE")
        if telefone:
            conversas["conversas"].append({
                "mensagens": [
                    f"Qual o telefone do {nome}?", 
                    f"Qual o contato do {nome}?", 
                    f"Como entrar em contato com o {nome}?"
                ],
                "resposta": f"O telefone do {nome} é: {telefone}."
            })

        # Horário de Funcionamento
        turno = est.get("DS_TURNO_ATENDIMENTO")
        if turno:
            conversas["conversas"].append({
                "mensagens": [
                    f"Qual o horário de funcionamento do {nome}?", 
                    f"O {nome} funciona que horas?", 
                    f"Que horas abre o {nome}?"
                ],
                "resposta": f"O horário de atendimento do {nome} é: {turno}."
            })

        # Atendimento SUS
        atende_sus = est.get("CO_AMBULATORIAL_SUS", "Não informado").upper()
        resposta_sus = "Sim" if atende_sus == "SIM" else "Não"
        conversas["conversas"].append({
            "mensagens": [
                f"O {nome} atende pelo SUS?", 
                f"Posso usar o SUS no {nome}?", 
                f"O {nome} aceita SUS?"
            ],
            "resposta": f"{resposta_sus}, o {nome} {'atende' if resposta_sus == 'Sim' else 'não atende'} pelo SUS."
        })

        # Tipo de Gestão
        gestao = mapear_gestao(est.get("TP_GESTAO"))
        conversas["conversas"].append({
            "mensagens": [
                f"Qual o tipo de gestão do {nome}?", 
                f"Quem administra o {nome}?", 
                f"Qual a administração do {nome}?"
            ],
            "resposta": f"A gestão do {nome} é: {gestao}."
        })

        # Coordenadas Geográficas
        lat = est.get("NU_LATITUDE")
        lon = est.get("NU_LONGITUDE")
        if lat and lon:
            conversas["conversas"].append({
                "mensagens": [
                    f"Quais as coordenadas do {nome}?", 
                    f"Qual a latitude e longitude do {nome}?", 
                    f"Onde fica o {nome} no mapa?"
                ],
                "resposta": f"As coordenadas do {nome} são: Latitude {lat}, Longitude {lon}."
            })

    print(f"Total de {count} estabelecimentos processados.")
    return conversas

def salvar_conversas(conversas, caminho_saida):
    """Salva a estrutura de conversas em um arquivo JSON."""
    print(f"Salvando arquivo de conversas em: {caminho_saida}")
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    with open(caminho_saida, "w", encoding="utf-8") as f:
        json.dump(conversas, f, indent=2, ensure_ascii=False)
    print("Arquivo salvo com sucesso!")

def main():
    """
    Função principal para orquestrar o pipeline de preparação de dados.
    """
    parser = argparse.ArgumentParser(
        description="Prepara os dados de estabelecimentos de saúde para o treinamento do Botesus."
    )
    parser.add_argument(
        "--ibge",
        type=str,
        help="Código IBGE do município para filtrar os dados. Se não for fornecido, todos os municípios serão processados."
    )
    args = parser.parse_args()

    start_time = time.time()
    
    # 1. Carregar os dados
    estabelecimentos_gen = carregar_estabelecimentos(ARQUIVOS_DADOS_ENTRADA)
    
    # 2. Gerar as conversas (com filtro opcional)
    conversas_geradas = gerar_conversas(estabelecimentos_gen, args.ibge)
    
    # 3. Salvar o arquivo final
    salvar_conversas(conversas_geradas, ARQUIVO_DADOS_SAIDA)
    
    end_time = time.time()
    print(f"Pipeline de preparação de dados concluído em {end_time - start_time:.2f} segundos.")

if __name__ == "__main__":
    main()
