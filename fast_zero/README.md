# Psy Utils

O Psy_utils destina-se a prover ferramentas uteis para a interação entre psicólogos e clientes.

## Pré-requisitos

Certifique-se de ter os seguintes pré-requisitos instalados:

- [pyenv](https://github.com/pyenv/pyenv)
- [pipx](https://pipxproject.github.io/pipx/)
- [Poetry](https://python-poetry.org/)

## Configuração do Ambiente

Siga os passos abaixo para configurar o ambiente virtual do projeto.

### 1. Instalar e Configurar o pyenv

#### No windows:

Instala o pyvenv
```Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"```

instala a versão do python
```pyenv install latest```

define ela como a versão global
```pyenv global {versão instalada}```

#### No Linux Ubuntu

```curl -fsSL https://pyenv.run | ``

instala a versão do python
```pyenv install latest```

define ela como a versão global
```pyenv global {versão instalada}```

### 2. Instalar e Configurar o pipx

#### No Windows

```scoop install pipx ``` 

```pipx ensurepath```

#### No Linux Ubuntu

```sudo apt update```

```sudo apt install pipx```

```pipx ensurepath```

### 3. Instalar e Configurar o poetry

```pipx install poetry```

No diretório do projeto:
```poetry install```

## Utilização

### Configurando o projeto
Crie um arquivo .env na raiz do projeto, e insira a url da base de dados na variável
```DATABASE_URL```.
Bem como configure as variáveis
```SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES```

Ex: ```DATABASE_URL="sqlite+aiosqlite:///database.db"```

### Executando o projeto
Levantando o servidor: ```task run```

Executando os testes: ```task test```

Executando o formatador: ```task format```

Criando migrações no alembic: ```alembic revision --autogenerate -m "migration title"```

Aplicando as migrações do alembic: ```alembic upgrade head```
