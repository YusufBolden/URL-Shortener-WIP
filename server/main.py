from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello():
    print 'Hello world I am running!'
    return 'Hello World!\n'
