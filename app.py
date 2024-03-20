from flask import Flask, request, jsonify, render_template
# from pa2_1 import IntelligentAleeza, reflectionTable, emotionTable, responseTable
import joblib
import json

app = Flask(__name__)
model = joblib.load('model.joblib')

@app.route('/', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data['user_input']
    response = model.predict(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)