from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import logging
from datetime import timezone, datetime
from honeypot.alert import send_email_alert, Service

class HoneypotHandler(BaseHTTPRequestHandler):
    def log_request_details(self, method, body=None):
       
        log_entry = {
            'time': datetime.now(timezone.utc).isoformat(),
            'method': method,
            'client_ip': self.client_address[0],
            'path': self.path,
            'headers': dict(self.headers),
        }
        if body:
            log_entry['body'] = body.decode(errors='ignore')
        logging.info(log_entry)

    def do_GET(self):

        if self.path == '/':
            send_email_alert(self.client_address[0], Service.HTTP)
            self.log_request_details('GET')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            login_page = """
            <html>
            <body>
            <h1>Login Page</h1>
            <form method="post">
            <label for="username">Username:</label><br>
            <input type="text" id="username" name="username"><br>
            <label for="password">Password:</label><br>
            <input type="password" id="password" name="password"><br>
            <input type="submit" value="Login">
            </form>
            </body>
            </html>
            """
            self.wfile.write(login_page.encode())

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_body = self.rfile.read(content_length)
        self.log_request_details('POST', body=post_body)

        # Parse form data
        data = parse_qs(post_body.decode('utf-8'))
        username = data.get('username', [''])[0]
        password = data.get('password', [''])[0]

        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()

        response = f"""
        <html>
        <body>
        <h1>Login Attempt</h1>
        <p>Username: {username}</p>
        <p>Password: {password}</p>
        </body>
        </html>
        """
        self.wfile.write(response.encode('utf-8'))


    # def log_message(self, format, *args):
    #     # Disable default logging to stdout
    #     return


def http_main():
    logging.basicConfig(
        filename='honeypot.log',
        level=logging.INFO,
        format='%(message)s'
    )
    server_address = ('0.0.0.0', 8080)
    httpd = HTTPServer(server_address, HoneypotHandler)
    httpd.serve_forever()

if __name__ == "__main__":
    logging.basicConfig(
        filename='http_honeypot.log',
        level=logging.INFO,
        format='%(message)s'
    )

    server_address = ('0.0.0.0', 8080)  
    httpd = HTTPServer(server_address, HoneypotHandler)
    print(f"[*] Fake HTTP Honeypot running on port {server_address[1]}")
    httpd.serve_forever()
