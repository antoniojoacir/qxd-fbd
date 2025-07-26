# Aplicação python com integração sql
Criar um ambiente virtual para a instalação dos pacotes necessarios

```bash
python3 -m venv .venv
```

Agora carregar o ambiente

```bash
source .venv
```

Pacotes a serem instalados

```bash
pip install -r requeriments.txt
```

Para a conexão ao banco de dados, você vai precisar criar o arquivo `db.py` dentro do diretorio env

```bash
mkdir env && touch db.py
```

Após a criação, você vai preencher o arquivo com as seguintes informações

```python
import psycopg2


def db_connect():
    return psycopg2.connect(
        # !NOTE: nome do banco de dados a ser acessado
        dbname="dbname", 
        # !NOTE: Procure deixar o padrão (postgres) na hora da criação do banco
        user="user",       
        # !NOTE: senha do usuario de acesso
        password="password", 
        # !NOTE: localização do banco de dados
        host="localhost"
    )
```
