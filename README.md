# MDS - Squad 06 (2023/2)

Repositório contendo o código do projeto da disciplina de Métodos de
Desenvolvimento de Software. O projeto consiste em um juíz online para
programação competitiva.

## Resumo

Um juiz online representa uma plataforma essencial em competições de
programação, desempenhando o papel crucial de avaliar e classificar as soluções
submetidas pelos participantes. Além de ser uma ferramenta valiosa para
competições, também serve como um ambiente propício para a exploração e
aprendizado de novas linguagens de programação. Nessa plataforma, os
participantes enfrentam desafios por meio de questões específicas, e ao
submeterem seus códigos, essas submissões são sujeitas a limites rigorosos de
tempo e memória, adicionando uma dimensão adicional de desafio e eficiência à
avaliação.

## Motivação

Nossa motivação é desenvolver um juiz online que adira estritamente aos
princípios do software livre.

## Showcase

Você pode olhar um showcase do nosso projeto através desses links:

- [Ambiente de desenvolvimento](https://develop.squad06.com)
- [Ambiente de homologação](https://staging.squad06.com)
- [Ambiente de produção](https://squad06.com)

## Instalação

### Ambiente

Recomendamos o uso de **distribuições baseadas em Debian** como ambiente de
desenvolvimento do projeto. No Windows, recomendamos o uso do
[WSL](https://docs.microsoft.com/en-us/windows/wsl/install-win10).

### Começando

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
$ docker compose up
# Para rodar em segundo plano, use:
$ docker compose up -d
```

Para rodar as migrações do banco de dados, você precisará criar um container
temporário que executará as migrações. Faça isso com o seguinte comando:

```bash
$ docker compose run --rm django python manage.py migrate
```

Para fechar o servidor do Django, use o seguinte comando:

```bash
$ docker compose down
# Caso você queira remover os volumes do Docker, use:
$ docker compose down -v
# Isto removerá os volumes do Docker, o que significa que os dados do banco de
# dados serão perdidos.
```

Em caso de problemas com a instalação, verifique a
[documentação](https://docs.squad06.com/pt/latest/installation.html).

## Links

- [Documentação](https://docs.squad06.com/pt/latest/)
- [Link para o projeto](https://squad06.com)

## Membros

<table>
  <tr>
    <td align="center"><a href="https://github.com/bitterteriyaki"><img style="border-radius: 50%;" src="https://github.com/bitterteriyaki.png?size=100" width="100px;" alt=""/><br /><sub><b>Caio Alexandre</b></sub></a><br />
    <td align="center"><a href="https://github.com/jpcfarias"><img style="border-radius: 50%;" src="https://github.com/jpcfarias.png?size=100" width="100px;" alt=""/><br /><sub><b>João Farias</b></sub></a><br />
    <td align="center"><a href="https://github.com/thegm445"><img style="border-radius: 50%;" src="https://github.com/thegm445.png?size=100" width="100px;" alt=""/><br /><sub><b>Gabriel Moura</b></sub></a><br />
    <td align="center"><a href="https://github.com/LuizaMaluf"><img style="border-radius: 50%;" src="https://github.com/LuizaMaluf.png?size=100" width="100px;" alt=""/><br /><sub><b>Luiza Maluf</b></sub></a><br /><a href="Link git" title="Rocketseat"></a></td>
    <td align="center"><a href="https://github.com/HladczukLe"><img style="border-radius: 50%;" src="https://github.com/HladczukLe.png?size=100" width="100px;" alt=""/><br /><sub><b>Letícia Hladczuk</b></sub></a><br />
    <td align="center"><a href="https://github.com/MMcLovin"><img style="border-radius: 50%;" src="https://github.com/MMcLovin.png?size=100" width="100px;" alt=""/><br /><sub><b>Gabriel Fernando</b></sub></a><br />
  </tr>
</table>
