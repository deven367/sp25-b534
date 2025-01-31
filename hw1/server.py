import json
from http.server import BaseHTTPRequestHandler, HTTPServer


class MessageHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        message = post_data.decode('utf-8')

        print(f"Received message: {message}")

        # Send a response
        response = {'status': 'received', 'message': message}
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def log_message(self, format, *args):
        # print("log_message", format, args)
        return  # Suppress logging to console


if __name__ == "__main__":
    server_address = ('127.0.0.1', 8000)
    httpd = HTTPServer(server_address, MessageHandler)
    print(f"Server is running at http://{server_address[0]}:{server_address[1]}")
    httpd.serve_forever()