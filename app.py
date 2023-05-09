from flask import Flask, render_template, request
from main import convo
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    human_input = request.form['human_input']
    output = convo.run(human_input)
    return {'response': output}

if __name__ == '__main__':
    app.run(debug=True)
