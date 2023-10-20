# MDS - Squad 06 (2023/2)

Repositório contendo o código do projeto da disciplina de Métodos de
Desenvolvimento de Software. O projeto consiste em um juíz online para
programação competitiva.

## Instalação

Para instalar o projeto, é necessário ter o Python 3.11.5 e o Poetry 1.6.1
instalados. Você pode ver o guia de instalação do projeto
[aqui](https://mds.kyomi.dev/pt/latest/installation.html), ou seguir as
instruções abaixo:


## Ambiente

Recomendamos o uso de **distribuições baseadas em Debian** como ambiente de
desenvolvimento do projeto. No Windows, recomendamos o uso do [WSL](https://docs.microsoft.com/en-us/windows/wsl/install-win10)

## Começando

Você pode instalar o projeto com os seguintes comandos:

```bash
# Clonando o repositório do projeto:
$ git clone https://github.com/unb-mds/2023-2-Squad06.git
# Entrando na pasta do projeto:
$ cd 2023-2-Squad06
```

Tendo feito isso, instale as dependências do projeto com o Poetry:

```bash
$ poetry install
# Caso você precise das dependências de documentação, use:
$ poetry install --with docs
```

Crie o arquivo de ambiente usando o script do próprio projeto:

```bash
$ poetry run ./bin/create-env
```

Por fim, rode o projeto com o Docker:

```bash
$ docker compose up # para rodar em segundo plano, adicione ' -d '
```

```bash
$ git config --global core.autocrlf false
```

Para rodar as migrações do banco de dados, você precisará criar um container
temporário que executará as migrações. Faça isso com o seguinte comando:

```bash
$ docker compose run --rm web python manage.py migrate
```

Para fechar o servidor do Django, use o seguinte comando:

```bash
$ docker compose down
# Caso você queira remover os volumes do Docker, use:
$ docker compose down -v
# Isto removerá os volumes do Docker, o que significa que os dados do banco de dados serão perdidos.
```

Para executar os testes do projeto, use o seguinte comando:

```bash
$ docker compose run --rm django python manage.py test
```

Se você precisar olhar os logs do servidor do Django, use o seguinte comando:

```bash
$ docker compose logs
```

## Para Desenvolvimento Local

### Git Hooks

```bash
$ poetry run pre-commit install \
  --hook-type pre-commit \
  --hook-type pre-push \
  --hook-type commit-msg
```

### Django

Para criar um superusuário, a fim de se poder acessar o painel de administração
do Django, use o seguinte comando:

```bash
$ docker compose run --rm web python manage.py createsuperuser
```

E para criar migrações do banco de dados, use o seguinte comando:

```bash
$ docker compose run --rm web python manage.py makemigrations
```

## Links

- [Documentação](https://mds.kyomi.dev/pt/latest/)
