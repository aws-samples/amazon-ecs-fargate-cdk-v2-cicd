# from flask import Flask, escape, request, render_template
import flask
import datetime
import platform
import os

app = flask.Flask(__name__)


@app.route('/')
def hello():
    name = flask.request.args.get("name", "Flask-demo")
    time = datetime.datetime.now()
    python_version = platform.python_version()
    aws_platform = os.environ.get('PLATFORM', 'Amazon Web Services')
    #page = 'hello.html'
    page = 'solid.hello.htlm'
    return flask.render_template('hello.html',
                                 platform=aws_platform,
                                 flask_version=flask.__version__,
                                 python_version=python_version,
                                 flask_url='https://palletsprojects.com/p/flask/',
                                 time=time,
                                 name=name)


if __name__ == '__main__':
    app.run(
        debug=os.getenv('FLASK_DEBUG',False),
        host='0.0.0.0',
        port=5000
    )
