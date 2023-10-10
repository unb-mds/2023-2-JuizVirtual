# 2023-2-Squad06

# Guia de instalação

## Resumo

Para a instalação e a operação corretas, deve se ter instalado na máquina:
- Python versão 3.11.5
- Poetry versão 1.6.1

Após verificar quanto aos requisitos acima, rode estes comandos:

- `poetry install`
- Se necessárias dependências de documentação, `poetry install --with docs`
- Para instalar Git Hooks:
    ```bash
    poetry run pre-commit install \
    --hook-type commit-msg \
    --hook-type pre-commit \
    --hook-type pre-push
    ```
- Gerar o arquivo config `poetry run ./bin/create-env`
- Para finalizar a instalação e conseguir visualizar a página:

    - `docker compose build && docker compose up -d`
    - `docker compose run django python manage.py migrate`
    - `docker compose run django python manage.py createsuperuser`
