from flask import Flask

server = Flask(__name__)
server.config["SECRET_KEY"] = '123456'

@server.route('/hello')
def hello() -> str:
    return 'Hello world from Flask!'



if __name__ == '__main__':
    server.run(port=2342, debug=True)