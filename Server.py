"""Run the EasyInstall command"""
import socket

URLS={
    '/homepage':'homepage',
    '/':'Hello'
}
def content(code,url):
    if code==404:
        return '<h1>404</h1><p>Not found</p>'
    if code==405:
        return '<h1>405</h1><p>Method not allowed</p>'
    return '<h1>{}</h1>'.format(URLS[url])


def run():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind(("localhost", 7902))
    server_socket.listen()
    while True:
        client_socket, addr = server_socket.accept()
        request = client_socket.recv(1024)
        print(request)
        print()
        print(addr)

        response = response_gen(request.decode('utf-8'))

        client_socket.sendall(response)
        client_socket.close()

def parse_request(request):
    parsed=request.split(' ')
    method=parsed[0]
    url=parsed[1]
    return (method,url)

def response_gen(request):
    method,url=parse_request(request)
    headers,code=headers_gen(method,url)
    body=content(code,url)
    return (headers+body).encode()

def headers_gen(method,url):
    if not method =='GET':
        return ('HTTP/1.1 405 Method not allowed\n\n',405)
    if not url in URLS:
        return ('HTTP/1.1 404 Not found\n\n',404)
    return ('HTTP/1.1 200 OK\n\n',200)

if __name__ == '__main__':
    run()
