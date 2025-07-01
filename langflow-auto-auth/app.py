
import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

LANGFLOW_URL = os.environ.get("LANGFLOW_URL", "http://localhost:3000")

@app.route('/')
def index():
    return render_template('index.html', langflow_url=LANGFLOW_URL)

@app.route('/login', methods=['POST'])
def login():
    username = "testuser2"
    password = "testpass"
    print(f"Username: {username}, Password: {password}")

    # First, try to create the user. If the user already exists, the API will return an error, which we'll ignore.
    try:
        requests.post(f'{LANGFLOW_URL}/api/v1/users/', json={'username': username, 'password': password})
    except requests.exceptions.RequestException as e:
        # This will likely fail if the user already exists, which is fine.
        print(f"Could not create user (may already exist): {e}")


    # Now, log in the user to get a token
    try:
        response = requests.post(f'{LANGFLOW_URL}/api/v1/login', data={'username': username, 'password': password})
        response.raise_for_status()  # Raise an exception for bad status codes
        token_data = response.json()
        return jsonify(token_data)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Failed to login to Langflow: {e}'}), 500

if __name__ == '__main__':
    app.run(port=5001)
