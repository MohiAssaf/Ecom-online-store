import socketserver
import io
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from db import create_user_table


class RequestHandler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        content_len = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_len)
        data = parse_qs(post_data.decode('utf-8'))
        
    
    


class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    'Handeling requests in a seperate thread.'
    

if __name__ == '__main__':
    create_user_table()
    server_address = ('', 8000)
    httpd = ThreadedHTTPServer(server_address, RequestHandler)
    httpd.serve_forever()
    print('The server is running on port 8000')