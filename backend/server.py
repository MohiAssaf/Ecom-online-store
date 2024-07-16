import socketserver
import io
import os
import base64
import mimetypes
from http.server import BaseHTTPRequestHandler, HTTPServer
from http.cookies import SimpleCookie
from urllib.parse import urlparse, parse_qs
from db import create_user_table, connect_db
from util import generate_captcha_text, generate_captcha_img, generate_session_id
from werkzeug.security import generate_password_hash, check_password_hash


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
                    
            elif path == '/logout':
                self.send_response(302)
                self.send_header('Set-Cookie', 'session_id=; Max-Age=0; Path=/')
                self.send_header('Location', '/login')
                self.end_headers()
                    
            elif path == '/profile':
                cookie_header = self.headers.get('Cookie')
                cookie = SimpleCookie(cookie_header)
                session_id = cookie.get('session_id')
                if not session_id:
                    self.send_response(302)
                    self.send_header('Location', '/login')
                    self.end_headers()
                    return
                
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("SELECT first_name, last_name, email, username, profile_picture FROM users WHERE sessionid = %s", (session_id.value,))
                user = cursor.fetchone()
                
                if not user:
                    self.send_response(302)
                    self.send_header('Location', '/login')
                    self.end_headers()
                    return
                
                first_name, last_name, email, username, profile_picture = user
                
                if profile_picture:
                    profile_picture_base64 = base64.b64encode(profile_picture).decode('utf-8')
                    profile_picture_src = f"data:image/png;base64,{profile_picture_base64}"
                else:
                    profile_picture_src = '../images/profile-default.png'
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                with open('../frontend/html/profile.html') as file:
                    html = file.read()
                    html = html.replace('{first_name}', first_name) \
                                .replace('{last_name}', last_name) \
                                .replace('{email}', email) \
                                .replace('{username}', username) \
                                .replace('{profile_picture}', profile_picture_src)
                    self.wfile.write(html.encode('utf-8'))
            elif path == '/update-profile':
                
                cookie_header = self.headers.get('Cookie')
                cookie = SimpleCookie(cookie_header)
                session_id = cookie.get('session_id')
                if not session_id:
                    self.send_response(302)
                    self.send_header('Location', '/login')
                    self.end_headers()
                    return
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                with open('../frontend/html/update-profile.html', encoding='utf-8') as file:
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
            profile_pic = data.get('profile_picture')[0]
            
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
            
            cursor.execute('INSERT INTO users(first_name, last_name, email, username, password, profile_picture) VALUES(%s, %s, %s, %s, %s, %s)',
                           (first_name, last_name, email, username, generate_password_hash(password), profile_pic))
            
            conn.commit()
            self.send_response(302)
            self.send_header('Location', '/login')
            self.end_headers()
            
            
        elif path == '/login':
            username = data.get('username')[0]
            password = data.get('password')[0]
            
            conn = connect_db()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM users WHERE username = %s", (username, ))
            user = cursor.fetchone()
            
            if user:
                hashed_password = user[5]
                print(hashed_password)
                if check_password_hash(hashed_password, password):
                    session_id = generate_session_id()
                    
                    cursor.execute('UPDATE users SET sessionid = %s WHERE username = %s', (session_id, username))
                    conn.commit()
                    
                    self.send_response(302)
                    self.send_header('Set-Cookie', f'session_id={session_id}; Path=/')
                    self.send_header('Location', '/')
                    self.end_headers()
                else:
                    self.send_response(401)
                    self.send_header('Content-Type', 'text/plain')
                    self.end_headers()
                    self.wfile.write(b'Passwords don\'t match')
                    
        elif path == '/update-profile':
            
            first_name = data.get('first_name')[0]
            last_name = data.get('last_name')[0]
            email = data.get('email')[0]
            username = data.get('username')[0]
            profile_pic = data.get('profile_picture')[0]
            current_password = data.get('current_password')[0]
            
            
            cookie_header = self.headers.get('Cookie')
            cookie = SimpleCookie(cookie_header)
            session_id = cookie.get('session_id')
            
            conn = connect_db()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM users WHERE sessionid = %s", (session_id, ))
            user = cursor.fetchone()
            hashed_password = user[5]
            
            if check_password_hash(hashed_password, current_password):
                pass
            else:
                self.send_response(401)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'Passwords don\'t match')

            
            
            
        else:
            self.send_response(401)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Invalid credentials')
        
        
        
    
    


class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    'Handeling requests in a seperate thread.'
    

if __name__ == '__main__':
    create_user_table()
    server_address = ('', 8000)
    httpd = ThreadedHTTPServer(server_address, RequestHandler)
    print('The server is running on port 8000')
    httpd.serve_forever()