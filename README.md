# Projeto

Criação de uma REST API em Python, que organiza os artistas do usuário, persistindo os dados em um Banco de Dados e tendo como base os dados obtidos a partir de consulta a API do Itunes. (https://developer.apple.com/library/archive/documentation/AudioVideo/Conceptual/iTuneSearchAPI/index.html)

## Tecnologias

- Python na versão 3.7.6
  * Uso do framework Flask para criação das rotas da API
- Docker
  * Uso do Docker Compose para linkar a aplicação em Python com o banco de dados
- Banco de Dados MySQL na versão 8.0

## Instalação

Para utilizar o projeto é necessário ter o Docker e Docker Compose instalado. O projeto foi testado e está funcionando corretamente com o Docker Toolbox no Windows.

Para começar a utilizar deve-se clonar o repositório:

```shell
git clone https://github.com/pedrovicentesantos/rest-api-infoglobo.git
cd rest-api-infoglobo
```

É importante manter a seguinte estrutura dos arquivos. Caso contrário, o `docker-compose` não irá encontrar os arquivos e não vai funcionar.
  
    rest-api-infoglobo  
    └── app
    │    ├── app.py
    │    ├── db_connect.py
    │    ├── Dockerfile
    │    ├── helpers.py
    │    ├── main.py
    │    ├── requirements.py
    │    └── test_helpers.py
    └── db
    │    └── init.sql
    ├── docker-compose.yml
    └── README.md

Depois de fazer o download dos arquivos deste repositório, para começar a usar deve-se fazer:

```shell
docker-compose up  # Cria as imagens e os containers
```

Feito isto, o container já estará funcionando. Dependendo do sistema operacional utilizado pode-se acessar a API por meio de `localhost:5000` ou `192.168.99.100:5000`.

O IP `192.168.99.100` é o default no Windows, mas caso não funcione, para pegar o IP correto pode-se usar o comando `docker-machine ip`.

## Comandos úteis

- Para parar o container:

```shell
docker-compose stop
```

- Para retomar o uso do container:

```shell
docker-compose start
```

- Para criar os containers novamente após alterações no código:

```shell
docker-compose up --build
```

- Para rodar os containers sem travar o terminal:

```shell
docker-compose up -d    # Pode-se usar --detach também
```

É importante comentar que o seguinte comando fará com que os dado não sejam persistidos no Banco de Dados:

```shell
docker-compose down   # Este comando deleta os containers e os dados do BD são reiniciados ao dar up nos containers novamente
```

Portanto, deve-se tomar cuidado ao usar este comando, pois pode gerar perda de dados.

## Funcionamento
Para usar a API funcionando pode-se usar comandos como `curl` ou programas específicos para este fim como `Postman` e `Insomnia`.

Com essas ferramentas é possível fazer os requests corretamente e incluir o `body` do request corretamente quando necessário.

Exemplos de usos podem ser vistos no link para a documentação no Postman:

<!-- Link para Postman -->

## Endpoints
Com o container rodando no Docker é possível fazer chamadas a API utilizando os endpoints documentados em:

<!-- Link para Postman -->

Mais informações sobre como funciona a lógica da API também se encontram no link acima.

## Testes Unitários
O projeto também conta com um arquivo para testes unitários, chamado `test_helpers.py`, que pode ser encontrado dentro da pasta `app`.

Para rodar os testes basta usar o comando:

```shell
python test_helpers.py
```

OBS: Como ainda estou iniciando em testes unitários, consegui realizar alguns poucos testes com o conhecimento que tenho no momento.

