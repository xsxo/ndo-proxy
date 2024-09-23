from _websocket import REQS, send_data
from socket import socket, SOCK_STREAM, AF_INET
from datetime import datetime
from _argv import ar, clear
from urllib.parse import urlparse
from threading import Thread, Lock
from ssl import SSLContext, PROTOCOL_TLS_SERVER, PROTOCOL_TLS_CLIENT, CERT_NONE
from webbrowser import open as oops
from websocket_server import WebsocketServer

class counting:
    def __init__(self) -> None:
        self.loop = 0

class realser:
    def __init__(self) -> None:
        self.create : bool = True
        self.last : dict = {}

    def relase(self) -> dict:
        if self.create:
            self.create = False
            counter.loop += 1
            self.last = {"number":counter.loop, "time": datetime.now().isoformat()}
            return self.last
        else: 
            self.create = True
            return self.last

def html_page():
    with open('test.html', 'r', encoding='utf-8') as file:
        html = file.read()

    return f"""HTTP/1.1 200 OK\r
Content-Type: text/html\r
Connection: close\r
\r
{html}"""

# "method": "", "response_status_code": ""

def send_request(client_socket:socket):
    to_connect = client_socket.recv(4096).decode('utf-8')
    host = to_connect.splitlines()[0].split(' ')[1]
    THE = realser()

    try:
        if to_connect.__contains__(f'{HOST}:{PORT}') and to_connect.__contains__('GET / HTTP/1.1'):
            client_socket.sendall(html_page().encode('utf-8'))
            client_socket.close()
            return
        elif to_connect.__contains__(f'{HOST}:{PORT}') and to_connect.__contains__('favicon.ico'):
            client_socket.close()
            return

        if '//' in host:
            parsed_url = urlparse(host)
            port = parsed_url.port or (80 if parsed_url.scheme == 'http' else 443)
            host = parsed_url.hostname
        elif ':' in host:
            port = host.split(':')[1]
            host = host.split(':')[0]

        if 'CONNECT' in to_connect:
            client_socket.send("HTTP/1.1 200 Connection Established\r\n\r\n".encode('utf-8'))

            context = SSLContext(PROTOCOL_TLS_SERVER)
            context.load_cert_chain(certfile=CERTFILE, keyfile=KEYFILE)
            context.verify_mode = CERT_NONE
            client_socket = context.wrap_socket(client_socket, server_side=True, do_handshake_on_connect=False)
            server_socket = socket(AF_INET, SOCK_STREAM)
            server_socket.connect((host, int(port)))

            context = SSLContext(PROTOCOL_TLS_CLIENT)
            context.check_hostname = False
            context.verify_mode = CERT_NONE
            context.load_verify_locations(CERTFILE)

            ssl_server = context.wrap_socket(server_socket, server_hostname=host)

            Thread(target=forward, args=(client_socket, ssl_server, 'REQ', THE, f'https://{host}',)).start()
            Thread(target=forward, args=(ssl_server, client_socket, 'RES', THE, f'https://{host}',)).start()

        else:
            server_socket = socket(AF_INET, SOCK_STREAM)
            server_socket.connect((host, int(port)))

            server_socket.send(to_connect.encode('utf-8'))
            Thread(target=forward, args=(client_socket, server_socket, 'raw_request', THE, f'http://{host}',)).start()
            Thread(target=forward, args=(server_socket, client_socket, 'raw_response', THE, f'http://{host}',)).start()
    except:
        pass

def forward(source, destination, mode:str, THE:realser, schame_with_host:str):
    resutl = False
    while True:
        try:
            data = source.recv(4096)
            destination.send(data)
            LOCK.acquire()
            print(f'{mode}: {data.decode('utf-8')}')
            if b'HTTP/1.1' in data:
                resutl = THE.relase()
                resutl[mode] = ''

            if mode == 'raw_request':
                resutl["api"] = schame_with_host

            try:
                resutl[mode] += data.decode('utf-8')
                REQS.append(resutl)
            except:
                pass
            

            if len(data) == 0:
                break

        except:
            break

        LOCK.release()

    # source.close()
    # destination.close()
 
def accecpted():
    while 1:
        try:
            client_socket, addr = server.accept()
            print(f'accepted {client_socket}:{addr}')
            Thread(target=send_request, args=(client_socket,)).start()
        except:
            pass

def main():
    Thread(target=accecpted).start()
    server = WebsocketServer(host=HOST, port=PORT + 2)
    server.set_fn_new_client(send_data)
    server.run_forever()

if __name__ == "__main__":
    clear()
    print('- help: https://github.com/xsxo/ndo-proxy')

    CERTFILE = 'cers/server.pem'
    KEYFILE = 'cers/server.key'    
    HOST, PORT = ar()
    LOCK = Lock()

    counter = counting()
    server = socket(AF_INET, SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1000000)

    clear()
    print('- help: https://github.com/xsxo/ndo-proxy')
    print(f'- proxy/url: http://{HOST}:{PORT}')
    print('- set the url proxy in browser to show results')

    oops(f'http://{HOST}:{PORT}')
    main()