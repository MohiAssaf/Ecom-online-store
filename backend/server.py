import socketserver
import io
import os
import base64
import mimetypes
from http.server import BaseHTTPRequestHandler, HTTPServer
from http.cookies import SimpleCookie
from urllib.parse import urlparse, parse_qs
from db import create_user_table, connect_db
from captch_generator import generate_captcha_text, generate_captcha_img
from werkzeug.security import generate_password_hash


class RequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        try:
            
            if path == '/':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                with open('../frontend/html/index.html', encoding='utf-8') as file:
                    html = file.read()
                    self.wfile.write(html.encode('utf-8'))
                    
            elif path == '/products':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                with open('../frontend/html/products.html', encoding='utf-8') as file:
                    html = file.read()
                    self.wfile.write(html.encode('utf-8'))
                    
                    
            elif path == '/contact':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                with open('../frontend/html/contact.html', encoding='utf-8') as file:
                    html = file.read()
                    self.wfile.write(html.encode('utf-8'))
            
            elif path == '/register':
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
                    
            elif path == '/login':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                with open('../frontend/html/login.html') as file:
                    html = file.read()
                    self.wfile.write(html.encode('utf-8'))
                    
            elif path.endswith('.css'):
                file_p = '../frontend' + path

                with open(file_p, 'rb') as file:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/css')
                    self.end_headers()
                    self.wfile.write(file.read())
                    
            else:
                static_path = os.path.join('../frontend', path.lstrip('/'))
                
                if os.path.isfile(static_path):
                    self.send_response(200)
                    mime_type, _ = mimetypes.guess_type(static_path)
                    self.send_header('Content-type', mime_type)
                    self.end_headers()
                    
                    with open(static_path, 'rb') as file:
                        self.wfile.write(file.read())
                        
                else:
                    self.send_response(404)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b'404 File not found')
                        
                
        except Exception as ex:
            
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f"500 Internal Server Erroe: {ex}".encode('utf-8'))
    
    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        content_len = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_len)
        data = parse_qs(post_data.decode('utf-8'))
        
        if path == '/register':
            first_name = data.get('first_name')[0]
            last_name = data.get('last_name')[0]
            email = data.get('email')[0]
            username = data.get('username')[0]
            password = data.get('password')[0]
            repeat_password = data.get('repassword')[0]
            captcha_input = data.get('captcha')[0]
            
            cookie_header = self.headers.get('Cookie')
            
            if not cookie_header:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Missing captcha')
                return
            
            cookie = SimpleCookie(cookie_header)
            captcha_txt = cookie.get('captcha').value
            
            if captcha_input != captcha_txt:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Invalid Captcha')
                return
            
            if password != repeat_password:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Passwords don\'t match')
                return
            
            conn = connect_db()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
            user_exists= cursor.fetchone()
            
            if user_exists:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Username already exists, please choose a different username')
                return
            
            cursor.execute('INSERT INTO users(first_name, last_name, email, username, password) VALUES(%s, %s, %s, %s, %s)',
                           (first_name, last_name, email, username, generate_password_hash(password)))
            
            conn.commit()
            self.send_response(302)
            self.send_header('Location', '/login')
            self.end_headers()
            
            
                
            
            
            
                
            
            
            
        elif path == '/login':
            username = data.get('username')[0]
            password = data.get('password')[0]
        
        
        
    
    


class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    'Handeling requests in a seperate thread.'
    

if __name__ == '__main__':
    create_user_table()
    server_address = ('', 8000)
    httpd = ThreadedHTTPServer(server_address, RequestHandler)
    print('The server is running on port 8000')
    httpd.serve_forever()