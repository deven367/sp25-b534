import json

import requests


def send_message(target_url, message):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(target_url, data=json.dumps(message), headers=headers)
    print(f"Response: {response.json()}")


if __name__ == "__main__":
    server_port = 8000

    while True:
        input_msg = input("Enter a message: ")
        message = {"type": "greeting", "content": input_msg}
        send_message(f'http://localhost:{server_port}', message)
