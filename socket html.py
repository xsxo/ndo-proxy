import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 9911))
server.listen(1)
client_socket, addr = server.accept()
print(f'addr: {addr}')

with open('test.html', 'r') as file:
    html = file.read()

html_content = f"""
HTTP/1.1 200 OK\r
Content-Type: text/html\r
Connection: close\r
\r
{html}
"""

while 1:
    data = client_socket.recv(4096)
    if data.__contains__(b'127.0.0.1:9911') and data.__contains__(b'GET / HTTP/1.1'):
        client_socket.sendall(html_content.encode('utf-8'))
        client_socket.close()
        break
    elif data.__contains__(b'127.0.0.1:9911') and data.__contains__(b'favicon.ico'):
        client_socket.close()
        


# import socket

# # إعداد خادم الـsocket
# HOST, PORT = '127.0.0.1', 8080

# # إنشاء الـsocket
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.bind((HOST, PORT))
# server_socket.listen(1)

# print(f'Server is listening on {HOST}:{PORT}')

# # صفحة HTML التي سيتم عرضها في المتصفح
# html_content = """
# HTTP/1.1 200 OK
# Content-Type: text/html

# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Socket HTML Response</title>
# </head>
# <body>
#     <h1>Hello from Socket Server!</h1>
#     <p>This is a response from a Python socket server.</p>
# </body>
# </html>
# """

# # انتظار الاتصال من المتصفح
# while True:
#     client_socket, client_address = server_socket.accept()
#     print(f'Connection from {client_address}')
    
#     # قراءة طلب المتصفح
#     request = client_socket.recv(1024).decode('utf-8')
#     print(f'Request:\n{request}')
    
#     # إرسال استجابة HTTP تتضمن صفحة HTML
#     client_socket.sendall(html_content.encode('utf-8'))
    
#     # إغلاق الاتصال
#     client_socket.close()