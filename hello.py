# -- coding:utf-8 --
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index() :
    return "<h1>你好,肖艳平</h1>"
if __name__ == '__main__':
    app.run()
