import json
from websocket_server import WebsocketServer

REQS = []
def send_data(client:dict, server:WebsocketServer):
    while True:
        if REQS:
            REQ : dict = REQS[-1]
            if 'raw_request' in REQ.keys():
                try:
                    request = REQ['raw_request'].splitlines()[0].split(' ')
                    REQ["method"] = request[0]
                    if '://' in request[1]:
                        REQ["api"] = request[1]
                    else:
                        REQ["api"] += request[1]
                except:
                    REQ["method"] = ""
                    
            server.send_message(client, json.dumps(REQ))
            REQS.remove(REQ)