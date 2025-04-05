from neo4j import GraphDatabase
from dotenv import load_dotenv 
import os
import pandas as pd
load_dotenv()


URI = os.getenv("NEO4J_URI")
AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))
driver = GraphDatabase.driver(URI, auth=AUTH)

try:
    driver.verify_connectivity()
    print("Conectado ao banco de dados com sucesso!")
except:
    print("Erro ao conectar ao banco de dados")

df = pd.read_csv('estacoes.csv')

# Verifica se as colunas necessárias estão presentes
if 'nome_estacao' not in df.columns or 'linha_cor' not in df.columns:
    raise KeyError("As colunas 'nome_estacao' e 'linha_cor' devem estar presentes no arquivo CSV.")

def cria_relacao(tx, df):
    for i in range(len(df)):
        estacao_atual = df.iloc[i]

        # Verifica a próxima estação na mesma linha (linha_cor)
        if i < len(df) - 1:
            for j in range(i + 1, len(df)):
                proxima_estacao = df.iloc[j]
                if estacao_atual['linha_cor'] == proxima_estacao['linha_cor']:
                    query = """
                    MERGE (e1:Estacao {nome: $estacao1, linha_cor: $linha_cor})
                    MERGE (e2:Estacao {nome: $estacao2, linha_cor: $linha_cor})
                    MERGE (e1)-[:VAI_PARA]->(e2)
                    """
                    tx.run(query, 
                           estacao1=estacao_atual['nome_estacao'], 
                           estacao2=proxima_estacao['nome_estacao'], 
                           linha_cor=estacao_atual['linha_cor'])
                    break  # Encontrou a próxima estação na mesma linha, pode parar

        # Verifica se a estação atual faz baldeação (tem uma segunda linha)
        if pd.notna(estacao_atual.get('linha_cor_2')):
            # Cria a relação de baldeação
            query_baldeacao = """
            MERGE (e:Estacao {nome: $estacao, linha_cor: $linha_cor})
            MERGE (e_baldeacao:Estacao {nome: $estacao, linha_cor: $linha_cor_2})
            MERGE (e)-[:BALDEACAO]->(e_baldeacao)
            """
            tx.run(query_baldeacao, 
                   estacao=estacao_atual['nome_estacao'], 
                   linha_cor=estacao_atual['linha_cor'], 
                   linha_cor_2=estacao_atual['linha_cor_2'])

            # Verifica a próxima estação na segunda linha (linha_cor_2)
            for j in range(i + 1, len(df)):
                proxima_estacao_2 = df.iloc[j]
                if estacao_atual['linha_cor_2'] == proxima_estacao_2['linha_cor']:
                    query_proxima_2 = """
                    MERGE (e1:Estacao {nome: $estacao1, linha_cor: $linha_cor_2})
                    MERGE (e2:Estacao {nome: $estacao2, linha_cor: $linha_cor_2})
                    MERGE (e1)-[:VAI_PARA]->(e2)
                    """
                    tx.run(query_proxima_2, 
                           estacao1=estacao_atual['nome_estacao'], 
                           estacao2=proxima_estacao_2['nome_estacao'], 
                           linha_cor_2=estacao_atual['linha_cor_2'])
                    break  # Encontrou a próxima estação na linha_cor_2, pode parar


def insert_relacoes(estacao):
    with driver.session() as session:
        #session.write_transaction(insere_publicacoes, pesquisador)
        session.write_transaction(cria_relacao, estacao)


insert_relacoes(df)