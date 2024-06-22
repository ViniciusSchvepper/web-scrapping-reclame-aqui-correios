from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from uri import uri as connectionAddress
from WebScrapping import Main

all_retrived_titles, all_retrived_statuses, all_retrived_descriptions = Main()
client = MongoClient(connectionAddress, server_api = ServerApi('1'))

try:
    database = client['reclamacoes']
    collection = database['reclamacoes']
    print('Conectado com sucesso!')

    documents = []
    for title, status, descriptions in zip(all_retrived_titles, all_retrived_statuses, all_retrived_descriptions):
        document = {
            "title": title,
            "status": status,
            "descriptions": descriptions
        }
        documents.append(document)

    collection.insert_many(documents)
    print('Dados inseridos.')

except Exception as e:
    print(e)

finally:
    client.close()
    print('Conexao fechada.')