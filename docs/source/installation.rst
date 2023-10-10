Guia de Instalação
==================

.. rst-class:: lead

   Aqui você encontrará instruções e informações necessárias para a instalação
   e execução do projeto.

Ambiente
--------

Recomendamos o uso de **distribuições baseadas em Debian** como ambiente de
desenvolvimento do projeto. Apesar desse projeto provalemente funcionar em
ambientes Windows, não damos suporte a esse tipo de instalação. Os comandos
abaixo presume que você está usando um ambiente Ubuntu. Caso esteja usando
outra distribuição, adapte os comandos de acordo.

Para rodar o projeto, você precisará instalar Python 3.11.5 e o gerenciador de
pacotes `Poetry <https://python-poetry.org/>`_. Se atente em instalar as
versões corretas do Python e do Poetry, pois não há garantias de que o projeto
funcionará em versões diferentes.

Docker e Docker Compose
~~~~~~~~~~~~~~~~~~~~~~~

O projeto usa Docker e Docker Compose para facilitar a instalação e execução do
projeto. Nós **recomendamos fortemente** que você use Docker para rodar o
projeto, pois isso facilitará a instalação e execução do projeto. Para instalar
o Docker, siga as instruções do
`Docker <https://docs.docker.com/engine/install/ubuntu/>`_ e do
`Docker Compose <https://docs.docker.com/compose/install/linux/>`_.

Instalação
----------

Assumindo que você tenha instalado o Python, o Poetry e o Docker, você pode
instalar o projeto com os seguintes comandos:


.. code-block:: bash

   # Clonando o repositório do projeto:
   git clone https://github.com/unb-mds/2023-2-Squad06.git
   # Entrando na pasta do projeto:
   cd 2023-2-Squad06

Tendo feito isso, instale as dependências do projeto com o Poetry:

.. code-block:: bash

   poetry install
   # Caso você precise das dependências de documentação, use:
   poetry install --with docs

Crie o arquivo de ambiente usando o script do próprio projeto:

.. code-block:: bash

   poetry run ./bin/create_env

Por fim, rode o projeto com o Docker:

.. code-block:: bash

   docker compose build
   docker compose up -d

O site estará disponível em ``http://localhost:8000``. Entretanto, é necessário
rodar as migrações do banco de dados para que o site funcione corretamente.
Você pode fazer isso com o seguinte comando:

.. code-block:: bash

   # Isso criará um container temporário que executará as migrações.
   docker compose run --rm web python manage.py migrate


Desenvolvimento Local
---------------------

Git Hooks
~~~~~~~~~

Para desenvolver o projeto, recomendamos usar as ferramentas de desenvolvimento
do projeto. A primeira ferramenta são os Git hooks, que são scripts que são
executados automaticamente quando você executa certos comandos do Git. Para
instalar os Git hooks, use o seguinte comando:

.. code-block:: bash

   poetry run pre-commit install \
     --hook-type pre-commit \
     --hook-type pre-push \
     --hook-type commit-msg


É importante instalar os Git hooks para que seu código seja formatado
da maneira correta e para que os testes sejam executados antes de cada
commit. Caso você não queira instalar os Git hooks, você pode pular essa
etapa, mas é importante que você execute os testes e formate seu código
manualmente antes de cada commit, caso contrário seu commit será rejeitado
pelo CI (GitHub Actions).

Django
~~~~~~

Quando você rodar o projeto, você talvez precisará criar um superusuário para
acessar o painel de administração do Django. Para criar um superusuário, use o
seguinte comando:

.. code-block:: bash

   docker compose run --rm web python manage.py createsuperuser

E para criar migrações do banco de dados, use o seguinte comando:

.. code-block:: bash

   docker compose run --rm web python manage.py makemigrations
