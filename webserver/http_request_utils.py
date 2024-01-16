CRLF = "\r\n"

def parse_raw_http_request(request_str):
    parts = request_str.split(CRLF)
    http_verb, path, http_version = parse_request_line(parts[0])
    headers_till = len(parts) if "" not in parts else parts.index("")
    headers = parse_headers(parts[1: headers_till])
    message_body = None
    if "" in parts:
        # i.e. there is a message body
        message_body = parts[headers_till+1]
    return http_verb, path, http_version, headers, message_body
    
def parse_request_line(request_line):
    verb, path, version = request_line.split()
    return verb, path, version

def parse_headers(headers_parts):
    result = {}
    for header_line in headers_parts:
        sep_index = header_line.index(":")
        key = header_line[:sep_index]
        value = header_line[sep_index+1:]        
        key, value = key.strip(), value.strip()
        result[key] = value
    return result

def create_response_string(http_status, http_version, phrase, headers, message_body, add_content_length_header=True):
    response = ""
    response_line = "%s %s %s%s"%(http_version, http_status, phrase, CRLF)    
    response += response_line
    if add_content_length_header:
        if message_body:
            headers["Content-Length"] = len(message_body.encode())
        else:
            headers["Content-Length"] = 0
    for key, value in headers.items():
        header_line = "%s: %s%s"%(key, value, CRLF)
        response += header_line
    if message_body:
        response += CRLF + message_body
    return response

if __name__ == "__main__":
    request_str = "GET / HTTP/1.1\r\nHOST: LOCALHOST:8888\r\nUSER-AGENT: MOZILLA/5.0 (WINDOWS NT 10.0;\r\n\r\nabdcdhbd"
    print(parse_raw_http_request(request_str))