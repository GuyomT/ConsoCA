# ConsoCA

Projet en informatique I

Il est nécessaire de créer une base de données MySQL nommée consoca.

```sql
CREATE DATABASE consoca;
```

Vous pouvez alors installer les dépendances du projet et lancer l'application avec streamlit.

```bash
pip install -r requirements.txt
```

Add your user and password in the corresponding fields in the file .streamlit/secrets.toml

```toml
username = "root"
password = "password"
[connections.mydb]
dialect = "mysql"
host = "localhost"
port = 3306
database = "consoca"
username = "root"
password = "password"
```

```bash
streamlit run ./src/run.py
```
