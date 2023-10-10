Guia de instalação
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

Docker
~~~~~~

O projeto usa Docker para facilitar a instalação e execução do projeto. Nós
**recomendamos fortemente** que você use Docker para rodar o projeto, pois
isso facilitará a instalação e execução do projeto. Para instalar o Docker,
siga as instruções do
`site oficial <https://docs.docker.com/engine/install/ubuntu/>`_.

Instalação
----------

Assumindo que você tenha instalado o Python, o Poetry e o Docker, você pode
instalar o projeto com os seguintes comandos:

.. code-block:: bash

   git clone https://github.com/unb-mds/2023-2-Squad06.git


.. code-block:: python
   :emphasize-lines: 2
   :linenos:
   :caption: Code block caption.

   print("Don't highlight this")
   print("But this!")
   print("And this is unimportant again")
