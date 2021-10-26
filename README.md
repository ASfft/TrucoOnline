# Truco Online (Client-side)

Esse projeto é o back-end da web-application 

## Rodando localmente
###Obs: Para executar os testes é necessário rodar o projeto localmente

Usamos o poetry para gerenciar as dependências, portanto instale o poetry:
```bash
pip install poetry
```
Após instalado basta instalar as dependências:
```bash
poetry install
```

Para rodar o banco de dados (Postgres) localmente, utilizamos o docker,
por isso caso não o tenho instalado siga os passos em: https://docs.docker.com/get-docker/


Obs: Também é necessário instalar o docker-compose (https://docs.docker.com/compose/install/)

Para criar um container do banco de dados execute: 
```bash
./manage.py start_db
```

Para criar as tabelas no banco de dados, execute o código python localizado em utils/initalize.py

####Para executar os testes
Agora basta executar o test.py localizado na raiz do projeto (também é possível executar os testes um por um)

Os resultados são mostrados no terminal e são gerados arquivos html para verificação da cobertura do código

Bastar abrir no navegador o arquivo localizado em htmlcov/index.html

####Para rodar a API
Execute o run.py localizado na root do projeto

Para acessar a documentação da API, esteja com ela rodando e abra http://localhost:3000/docs

