Arquitetura
===========

.. rst-class:: lead

    Aqui você encontrará informações sobre a arquitetura do projeto.

Motivação
---------

Escolhemos desenvolver um juiz virtual para programação competitiva porque
queremos que os alunos da UnB tenham uma ferramenta que os ajude a treinar
para as competições de programação através de uma plataforma moderna e
intuitiva, que seja fácil de usar e que tenha uma boa experiência de usuário,
mas que os professores também possam usar para criar e gerenciar competições
de programação.

Geral
-----

A arquitetura do projeto é feita em um monolito, onde temos um único projeto
que contém todas as funcionalidades da aplicação. A arquitetura é dividida em
camadas, onde cada camada tem uma responsabilidade específica. A imagem abaixo
mostra a arquitetura da aplicação.

.. image:: ../_static/arch.png
   :alt: Arquitetura da aplicação.
   :align: center

A fila de mensagens é utilizada para processar as submissões de códigos dos
usuários. A fila é utilizada para que o usuário não precise esperar o código
ser executado para receber o resultado. A fila é processada por um worker que
executa o código e envia o resultado para o usuário.

Épico
-----

.. image:: ../_static/epic.jpeg
   :alt: Épico.
   :align: center

User Story
----------

.. image:: ../_static/user_story.jpeg
   :alt: User Story.
   :align: center

Protótipo
---------

.. image:: ../_static/prototipo_mds-01.png
   :alt: Protótipo.
   :align: center

.. image:: ../_static/prototipo_mds-02.png
   :alt: Protótipo.
   :align: center

.. image:: ../_static/prototipo_mds-03.png
   :alt: Protótipo.
   :align: center

.. image:: ../_static/prototipo_mds-04.png
   :alt: Protótipo.
   :align: center

.. image:: ../_static/prototipo_mds-05.png
   :alt: Protótipo.
   :align: center

.. image:: ../_static/prototipo_mds-06.png
   :alt: Protótipo.
   :align: center

.. image:: ../_static/prototipo_mds-07.png
   :alt: Protótipo.
   :align: center

.. image:: ../_static/prototipo_mds-08.png
   :alt: Protótipo.
   :align: center

.. image:: ../_static/prototipo_mds-09.png
   :alt: Protótipo.
   :align: center

.. image:: ../_static/prototipo_mds-10.png
   :alt: Protótipo.
   :align: center

.. image:: ../_static/prototipo_mds-11.png
   :alt: Protótipo.
   :align: center

.. image:: ../_static/prototipo_mds-12.png
   :alt: Protótipo.
   :align: center

.. image:: ../_static/prototipo_mds-13.png
   :alt: Protótipo.
   :align: center

.. image:: ../_static/prototipo_mds-14.png
   :alt: Protótipo.
   :align: center

.. image:: ../_static/prototipo_mds-15.png
   :alt: Protótipo.
   :align: center

.. image:: ../_static/prototipo_mds-16.png
   :alt: Protótipo.
   :align: center

.. image:: ../_static/prototipo_mds-17.png
   :alt: Protótipo.
   :align: center

.. image:: ../_static/prototipo_mds-18.png
   :alt: Protótipo.
   :align: center

.. image:: ../_static/prototipo_mds-19.png
   :alt: Protótipo.
   :align: center

.. image:: ../_static/prototipo_mds-20.png
   :alt: Protótipo.
   :align: center

.. image:: ../_static/prototipo_mds-21.png
   :alt: Protótipo.
   :align: center
