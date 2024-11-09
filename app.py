import json
import os
from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from transformers import pipeline, TFAutoModelForTokenClassification, AutoTokenizer
from inference import obfuscate as obf

app = Flask(__name__)
auth = HTTPBasicAuth()

model = TFAutoModelForTokenClassification.from_pretrained("DeaganH/pii_obfuscation_model", ignore_mismatched_sizes=True)
tokenizer = AutoTokenizer.from_pretrained("distilbert/distilbert-base-cased")

USER = os.environ.get('USER')
PASSWORD = os.environ.get('PASSWORD')

users = {
    USER: generate_password_hash(PASSWORD),
    "susan": generate_password_hash("bye")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return True
    return False

def pii_removal(text):

    PII_Entities = obf.predict_token_ids(text, tokenizer, model)

    redacted_text = obf.redact_text(text, PII_Entities)

    output = {
        'redacted_text': redacted_text
    }

    return jsonify(output) 

@app.route('/obfuscate/', methods=['GET', 'POST'])
@auth.login_required
def obfuscate():
    data = request.get_json()
    
    text = data.get('text', '')

    if len(text) == 0:
        return jsonify({'error': 'No text provided!'})

    return pii_removal(text)

if __name__ == '__main__':

    app.run(debug=True)