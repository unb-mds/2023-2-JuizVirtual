Sprint 6
========

:bdg-info:`01/12/2023`

Resumo
------

Durante a sprint mais recente, realizamos diversas alterações significativas no sistema
para atender às necessidades dos usuários e corrigir questões importantes. Implementamos
uma nova página de administração para submissões, permitindo aos administradores
um controle mais eficiente. Também corrigimos um problema relacionado ao serviço
de arquivos estáticos no Heroku, garantindo uma experiência mais estável.
Além disso, introduzimos uma página dedicada a outros usuários, proporcionando uma experiência
mais personalizada. Corrigimos um bug que permitia acesso indevido a tarefas
em concursos não iniciados ou cancelados, promovendo a integridade dos processos de competição.
No aspecto de desenvolvimento, implementamos a funcionalidade de casos de teste, permitindo
uma verificação mais robusta de funcionalidades e a detecção precoce de problemas.
Adicionamos uma integração inicial com RabbitMQ e outros message brokers, estabelecendo as
bases para uma comunicação eficiente entre os componentes do sistema. Integrando o
sistema de fila (message broker) à aplicação, promovemos uma comunicação assíncrona eficiente e escalável.
Para atender a uma solicitação específica, criamos uma nova página dedicada
às submissões, facilitando o acompanhamento e a gestão das
contribuições dos usuários. Essas mudanças combinadas melhoram a usabilidade, a
segurança e a funcionalidade geral do sistema.


Changelog
----------

- `Criar página de submissões (#100) <https://github.com/unb-mds/2023-2-JuizVirtual/issues/100>`_
- `Criar página de submissões (PR) (#101) <https://github.com/unb-mds/2023-2-JuizVirtual/pull/101>`_
- `Integrar sistema de fila (message broker) com a aplicação (#28) <hhttps://github.com/unb-mds/2023-2-JuizVirtual/issues/28>`_
- `Adicionar integração inicial com RabbitMQ e message brokers (PR) (#102) <https://github.com/unb-mds/2023-2-JuizVirtual/pull/102>`_
- `Adicionar resumo da aplicação e motivação no README (#94) <https://github.com/unb-mds/2023-2-JuizVirtual/issues/94>`_
- `Adicionar resumo e motivação da aplicação no README (PR) (#103) <https://github.com/unb-mds/2023-2-JuizVirtual/pull/103>`_
- `Implement test cases feature (PR) (#98) <https://github.com/unb-mds/2023-2-JuizVirtual/pull/98>`_
- `Não permitir que usuário acessem tasks para contests não iniciados ou cancelados (#90) <https://github.com/unb-mds/2023-2-JuizVirtual/issues/90>`_
- `Não permitir que usuário acessem tasks para contests não iniciados ou cancelados (PR) (#99) <https://github.com/unb-mds/2023-2-JuizVirtual/pull/99>`_
- `Implementar página de outros usuários (#91) <https://github.com/unb-mds/2023-2-JuizVirtual/issues/91>`_
- `Implementar página de outros usuários (PR) (#97) <https://github.com/unb-mds/2023-2-JuizVirtual/pull/97>`_
- `Adicionar página de administração para submissões (#92) <https://github.com/unb-mds/2023-2-JuizVirtual/issues/92>`_
- `Adicionar página de administração para submissões (PR) (#93) <https://github.com/unb-mds/2023-2-JuizVirtual/pull/93>`_
- `Serve static files correctly on Heroku (PR) (#89) <https://github.com/unb-mds/2023-2-JuizVirtual/pull/89>`_
