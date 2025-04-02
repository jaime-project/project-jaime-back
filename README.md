# :card_index_dividers: project-jaime

> Herramienta para ejecutar scripts de python en nodos

- Jaimeeehhhh...!!!
- ¿Si, señora?
- El Kubernetes necesita CI/CD y no hay Jenkins
- Por eso siempre traigo scripts

![alt](img/logo.png)

## :gear: Requisitos

- python 3.12
- virtualenv

## :tada: Uso

```bash
# Levantar el ambiente
virtualenv -p python3.12 env
. env/bin/activate
pip install -r requirements.txt

# Ejecutar
python app.py
```

## :hammer: Configuraciones

Se puede usar una **base de datos externa** agregando una variable de ambiente o agregandola en el **logic/resources/variables.yaml**

```yaml
# mysql
DB_URL: mysql+pymysql://user:pass@host:port/database

# postgresql
DB_URL: postgresql+pg8000://user:pass@host:port/database

# sqlserver
DB_URL: mssql+pymssql://user:pass@host:port/database

```

## :books: Referencias

- [Iconos](https://github.com/ikatyang/emoji-cheat-sheet/blob/master/README.md)
- [Image to ascii](https://www.asciiart.eu/image-to-ascii)
