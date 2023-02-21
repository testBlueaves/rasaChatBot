from flask import Flask, render_template
from ML_Pipeline.utlis import client_id
from ML_Pipeline.db import UserQuery

answer_list = UserQuery(client_id)

app = Flask(__name__, template_folder='../templates', static_folder='../input/static/')


@app.route('/query', methods=['GET'])
def query():
    return render_template('index.html', query=queries)


@app.route('/add_answer', methods=['POST'])
def add_answer():
    return render_template('index.html', query=queries)


if __name__ == '__main__':
    app.run()
