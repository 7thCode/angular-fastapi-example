# angular-fastapi-example

angular/fastapi auth example.


# Archtectre
### Client

Angular 14

### Server

uvicorn/FastAPI

# Config

### config file

default.jsonを追加してみてください。
パスは“config/default.json”です。


default.json

{
	"host": "localhost",
    "db": "fastapi",
    "collection": "accounts",
    "secret": "To be, or not to be."
}


host: 接続先(MongoDB)
db: データベース名。任意。
collection: accountのコレクション名。任意。
secret: トークンの鍵。任意。



# API

