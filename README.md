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

Este arquivo pode ser repartido em quatro partes, que são suas funções principais sendo elas:
- Pegar todas as reclamações presentes na página atual.
- Pegar o status, se foi respondido ou não.
- Entrar em cada uma dessas reclamações e pegar a descrição do cliente.
- Junção de todas as funções com algumas regras adicionais que contornam algumas inconsistencias.

### Pegar os titulos das reclamações (get_complaints_titles)
Procura por elementos especificos que correspondem as reclamoções feitas na página:
 `status = driver.find_elements(By.CSS_SELECTOR, 'span.sc-1pe7b5t-4')`, efetua um loop e aloca em uma lista vazia, que será utilizada posteriormente para redirecionar para as paginas correspondentes a uma reclamação especifica.

### Pegar o status da reclamação (get_complaints_statuses)
Esta função essencialmente é parecida com a de buscar pelso titulos, mas com a diferença que irá procurar por um elemento CSS diferente. Também retorna uma lista com os status.

### Pegar a descrição completa da reclamação (get_complaints_descriptions)
Para que esta função seja executada, ela esperar por dois parametros: **titles_list** que já foi explicado anteriormente e **actual_url** que será explicado posteriormente.
Com a lista de titulo é feita uma iteração para entrar na página de reclamação e extrair a descrição completa e então voltar para a página com os titulos resgatados para todos os titulos presentes.

### Função complementar (get_overlay_status)
A criação dessa função é dada pela necessidade de contornar um dos "problemas" presentes ao trocar de pagina ou retornar para a pagina de onde estão todas as reclmações, um pop-up aparece impedindo que qualquer ação seja tomada.
Portanto essa função pega o status de uma das divs, se for blocked, significa que o pop-up esta presente, caso for none, ações podem ser tomadas normalmente.

### Entendendo a função principal (Main)
Começamos criando três novas listas vazias, onde irão receber todas as os dados resgatados (titulos, status e descrições), e definimos um loop *while* que só será terminado em caso de nenhum titulo for encontrado, o que significa que não existem mais dados para serem extraidos.
Dentro deste loop a variável **actual_url** é definida para dar um novo ponto de retorno (que é onde estarão todos os titulos), visto que os scripts `driver.back()` e `driver.execute_script(windows.history.go(-1))` são inscosistentes na hora de voltar para a pagina anterior. Dessa forma sempre que trocarmos de página teremos definido um ponto de volta.
O proximo passo é conferir se a janela de pop-up esta presentes, caso sim é definido um `time.sleep(90)` que é o tempo aproximado para que ela desapareça e permita a tomada de novas ações.
Quando liberado, a função para pegar as descrições é chamada e repetida ate que todas as reclamações presentes na página tenham sido revindicadas.
Após isso é clicado no botão de ir para a proxima página com novas reclamações e o processo se repetir.
O retorno dado são as três listas que serão usadas para serem alocadas dentro do banco de dados.

## Alocando dentro do banco de dados
Novamente, começamos importando modulos para posibilitarem a conexão com o banco de dados, e desta vez serão importados também variaveis do arquivo de Web Scrapping e de outro arquivo onde tem as informações de login do banco de dados:
```
from uri import uri as connectionAddress
from WebScrapping import Main
```
Após feita a conexão com o *cluster* são definidos tanto a base de dados quanto a coleção:
```
client = MongoClient(connectionAddress, server_api = ServerApi('1'))
database = client['reclamacoes']
collection = database['reclamacoes']
```
Podemos fazer um loop para colocar todos os dados resgatados de maneira organizada, dentro de uma lista vazia, para fazer a inserção dentro do Mongo.

```
    documents = []
    for title, status, descriptions in zip(all_retrived_titles, all_retrived_statuses, all_retrived_descriptions):
        document = {
            "title": title,
            "status": status,
            "descriptions": descriptions
        }
        documents.append(document)

    collection.insert_many(documents)
```