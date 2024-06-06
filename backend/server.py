import socketserver
import io
import base64
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from db import create_user_table
from captch_generator import generate_captcha_text, generate_captcha_img


class RequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/register':
            captcha_txt = generate_captcha_text()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Set-Cookie', f'captcha={captcha_txt}; Path=/')
            self.end_headers()
            
            with open('../frontend/html/register.html', 'r') as file:
                html = file.read()
                captcha_img = generate_captcha_img(captcha_txt)
                with io.BytesIO() as output:
                    captcha_img.save(output, format='PNG')
                    captcha_data = output.getvalue()
                captch_bs64 = base64.b64encode(captcha_data).decode('utf-8')
                html = html.replace('{captcha_img}', f'<img src="data:image/png;base64,{captch_bs64}" alt="CAPTCHA">')
                self.wfile.write(html.encode('utf-8'))
                    
    
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