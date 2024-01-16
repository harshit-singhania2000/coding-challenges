import asyncio
from http_request_utils import parse_raw_http_request, create_response_string
import os

def read_file_at_path(path):    
    base_dir = os.path.join(os.getcwd(), "webserver", "www")
    filepath = os.path.join(base_dir, "index.html" if path=="/" else path[1:])
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r") as f:
        return f.read()

async def read_full_http_request(reader):
    """
    reads from the socket until complete parse-able http request text has been received
    if the request isn't parse-able it assumes that the full request hasn't been sent through yet
    and waits for more data on the socket
    """
    message = ""
    while True:
        data = await reader.read(10**6)
        data = data.decode()
        # print("received %s"%data)
        message += data
        try:
            http_verb, path, http_version, headers, message_body = parse_raw_http_request(message)
            break
        except Exception as e:
            # print("encountered exception:\n %s \n\n when attempting to read message:\n %s \n\n. Will keep waiting for more data"%(str(e), message))                    
            pass
    return http_verb, path, http_version, headers, message_body

async def handle_connection(reader, writer):
    keep_connection_open = True
    addr = writer.get_extra_info('peername')
    print("received new connection from", addr)
    ctr = 0
    while keep_connection_open:
        http_verb, path, http_version, headers, message_body = await read_full_http_request(reader)
        message_body = read_file_at_path(path)
        if message_body is None:
            response = create_response_string(404, http_version, "File Not Found", {"Connection": "close"}, message_body)
            keep_connection_open = False
        else:
            response = create_response_string(200, http_version, "OK", {"Connection": "keep-alive", 
                                                                        "temp": "123", "temp2": "456"}, 
                                                                        message_body)
        writer.write(response.encode())
        await writer.drain()
        if headers.get("Connection") != "keep-alive":
            keep_connection_open = False
    print("Closing the connection to", addr)
    writer.close()

async def main():
    server = await asyncio.start_server(handle_connection, '127.0.0.1', 8888)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

asyncio.run(main())