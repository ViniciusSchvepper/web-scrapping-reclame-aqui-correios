from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from uri import uri as connectionAddress
from WebScrapping import titles_list, complaints_status_list

client = MongoClient(connectionAddress, server_api = ServerApi('1'))

try:
    client.admin.command('ping')
    print('Conectado com sucesso!')
    database = client['reclamacoes']
    collection = database['reclamacoes']

    collection.delete_many({})
    print('Dados limpos')

    documents = []
    for title, status in zip(titles_list, complaints_status_list):
        document = {
            "title": title,
            "status": status
        }
        documents.append(document)

    collection.insert_many(documents)
    print('documentos inseridos com sucesso')

except Exception as e:
    print(e)

finally:
    client.close()
    print('Conexao fechada com sucesso')