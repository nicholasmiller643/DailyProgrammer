import socket
import re
import sys


def get_address_components(address):
    addr_match = re.fullmatch('(([a-z]+)://)?([a-zA-Z0-9-.]+)(:(\d+))?(/\S+)?', address)
    if addr_match is None:
        raise AssertionError('Invalid URL')
    protocol = addr_match.group(2)
    host = addr_match.group(3)
    port = addr_match.group(5)
    uri = addr_match.group(6)

    if (protocol is not None) and (protocol != 'http'):
        raise AssertionError('Protocol: {} is not supported.'.format(protocol))
    if port is None:
        port = 80
    if uri is None:
        uri = '/'

    return host, port, uri


def formulate_http_request(uri, headers):
    request_method = 'GET {} HTTP/1.1'.format(uri)
    headers = '\r\n'.join(('{}: {}'.format(key, value) for key, value in headers.items()))
    body = ''
    http_request = request_method + '\r\n' + headers + 2 * '\r\n' + body
    http_request = http_request.encode()
    return http_request


def main():
    address = sys.argv[1]

    host, port, uri = get_address_components(address)
    headers = {'Host': host}
    request = formulate_http_request(uri, headers)

    sock = socket.socket()
    sock.connect((host, port))
    sock.sendall(request)

    data = True
    while data:
        data = sock.recv(4096)
        print(data.decode())

if __name__ == '__main__':
    main()
