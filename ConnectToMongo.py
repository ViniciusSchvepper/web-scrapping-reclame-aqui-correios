from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from uri import uri as connectionAddress
from WebScrapping import titles_list, complaints_statuses_list, complaints_descriptions_list

client = MongoClient(connectionAddress, server_api = ServerApi('1'))

try:
    # client.admin.command('ping')
    database = client['reclamacoes']
    collection = database['reclamacoes']
    print('Conectado com sucesso!')

    collection.delete_many({})
    print('Dados anteriores excluidos.')

    documents = []
    for title, status, descriptions in zip(titles_list, complaints_statuses_list, complaints_descriptions_list):
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