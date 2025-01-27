from http.server import HTTPServer, SimpleHTTPRequestHandler

if __name__ == "__main__":
    server_address = ('127.0.0.1', 8000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Server is running at http://{server_address[0]}:{server_address[1]}")
    httpd.serve_forever()