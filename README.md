# Projeto

Criação de uma REST API em Python que organiza os artistas do usuário e faz um CRUD, persistindo os dados em um Banco de Dados MySQL, tendo como base a integração realizada com os dados obtidos na [API do iTunes](https://developer.apple.com/library/archive/documentation/AudioVideo/Conceptual/iTuneSearchAPI/index.html).

Baseado no desafio proposto em: https://github.com/Infoglobo/desafio-backend-infograficos

## Tecnologias

- Python na versão 3.8
  - Uso do framework Flask para criação das rotas da API
- Docker
  - Uso do Docker Compose para rodar a API e o banco de dados
- Banco de Dados MySQL na versão 8.0

## Rodando a aplicação

Após clonar o repositório, basta executar o comando `docker-compose up` e aplicação será executada.

Também é possível rodar localmente utilizando uma base de dados SQLite. Para isso, é necessário alterar o ambiente para `test` utilizado no arquivo `main.py` e instalar as dependências necessárias, que se encontram no arquivo `requirements.txt`.

Em ambos os casos a API estará disponível em http://localhost:5000.

## Endpoints

A aplicação foi documentada utilizando o Flasgger e a documentação pode ser acessada em: http://localhost:5000/apidocs/.

## Considerações

Para as rotas de criação foi considerado que o primeiro match do dado é o que o usuário procura. Foi implementado desta maneira para facilitar a integração com a API do iTunes.

Nas rotas de criação de álbuns e músicas, é necessário mandar além do nome do recurso, o nome do artista e do álbum, no caso das músicas. Caso contrário, seria mais difícil dificultar unicamente o que o usuário procura.
