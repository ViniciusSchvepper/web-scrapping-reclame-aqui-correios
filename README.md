# A proposta
Este é um projeto pessoal que visa melhorar e aprender habilidades relacionadas a área de dados. Nada usado aqui tem qualquer outro intuito além do aprendizado.
Com o objetivo de fazer uma raspagem de dados do site [Reclame Aqui - Correios](https://www.reclameaqui.com.br/empresa/correios/lista-reclamacoes/), resgatar informações das reclamações ativas, e alocar em um banco de dados não relacional, que para esse caso, usarei [MongoDB](https://www.mongodb.com/products/platform/cloud).
Importante resaltar que para esta documentação irei assumir que o leitor tenha algum nível de conhecimento em Python, portanto alguns processos não serão explicados.

# O funcionamento
Este projeto é divido essencialmente em duas partes: o arquivo de raspagem e o arquivo responsável por lidar com o banco de dados. Neste caso ainda existe um terceiro arquivo onde tem uma unica variável com os dados de conexão ao cluster do mongo.

## Entendendo o processo de *Web Scrapping*
Para que seja possível fazer todos esses processos, usamremos o *framework* [Selenium](https://www.selenium.dev).

Primeiro são feitas as importações de módulos que vão permitir que possamos tomar algumas ações específicas dentro do navegador.


Após isso é feita a configuração do serviço do *Chrome*´, inicializamos uma nova instância e com essas configurações e por fim definimos a *URL* de acesso:
```
service = ChromeService(executable_path = ChromeDriverManager().install())
driver = webdriver.Chrome(service = service)
driver.get("https://www.reclameaqui.com.br/empresa/correios/lista-reclamacoes/")
```

Este arquivo pode ser repartido em três partes, que são suas funções principais sendo elas:
- Pegar todas as reclamações presentes na página atual.
- Pegar o status, se foi respondido ou não.
- Entrar em cada uma dessas reclamações e pegar a descrição do cliente.

### Pegar os titulos das reclamações
Ao abrir a página são esperados 5 segundos para que ele comece a procurar por todos os titulos presentes, e então é feito um loop para alojar todos esses titulos dentro de uma lista vazia que será retornada ao final da função.

### Pegar o status da reclamação
Esta função essencialmente é parecida com a de buscar pelso titulos, mas com a diferença que irá procurar por um elemento CSS diferente. Também retorna uma lista com os status.

### Pegar a descrição completa da reclamação
Esta função tem um argumento que é o retorno da primeira função, pois sem ele, não será possível fazer a iteração necessária.
Com este argumento da lista de titulos, será feita uma procura de um elemento CSS correspondente com aquele titulo:
```
for title in titles_list:
        link_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f'//h4[text()="{title}"]/ancestor::a'))
        )
```
Após encontrar o elemento correspondente, executará a função de clique, e uma vez dentro da página irá procurar outro elemento CSS que corresponde a descrição do problema.
Quando resgatado irá colocar dentro de uma lista vazia e retornar para a pagina anterior e repetir o loop para todos os titulos presentes nesta página.

## Alocando dentro do banco de dados
Novamente, começamos importando modulos para posibilitarem a conexão com o banco de dados, e desta vez serão importados também variaveis do arquivo de Web Scrapping e de outro arquivo onde tem as informações de login do banco de dados:
```
from uri import uri as connectionAddress
from WebScrapping import titles_list, complaints_statuses_list, complaints_descriptions_list
```
Após feita a conexão com o *cluster* e definidos tanto a base de dados quanto a coleção:
```
client = MongoClient(connectionAddress, server_api = ServerApi('1'))
database = client['reclamacoes']
collection = database['reclamacoes']
```
Podemos fazer um loop para colocar todos os dados resgatados de maneira organizada, dentro de uma lista vazia, para fazer a inserção dentro do Mongo.

```
documents = []
for title, status, descriptions in zip(titles_list, complaints_statuses_list, complaints_descriptions_list):
    document = {
        "title": title,
        "status": status,
        "descriptions": descriptions
    }
    documents.append(document)
collection.insert_many(documents)
```