# Project: HTTP client and server
A simple http client and server, written using Python v3.12.3

Restrictions - the following helper functions are forbidden:
- The `socket.create_connection()` function.
- The `socket.create_server()` function.
- Anything in the `urllib` modules.

# Web client usage
The client can be accessed via the command line using the format: `$ python3 webclient.py address port`.</br>
Address and port are optional, and will default to "example.com" and 80.</br>
`$ python3 webclient.py example.com`</br>
`$ python3 webclient.py example.com 80` </br>
will return an output like this (truncated):
```
HTTP/1.1 200 OK
Accept-Ranges: bytes
Age: 438508
Cache-Control: max-age=604800
Content-Type: text/html; charset=UTF-8
Date: Tue, 07 Jan 2025 20:33:42 GMT
Etag: "3147526947"
Expires: Tue, 14 Jan 2025 20:33:42 GMT
Last-Modified: Thu, 17 Oct 2019 07:18:26 GMT
Server: ECAcc (dcd/7D2C)
Vary: Accept-Encoding
X-Cache: HIT
Content-Length: 1256
Connection: close

<!doctype html>
<html>
<head>
    <title>Example Domain</title>
    ...
```

# Web server usage
The web server can started via the command line using the format: `$ python3 webserver.py port`.</br>
Port is optional and will default to 28333.</br>
`$ python3 webserver.py` </br>
`$ python3 webserver.py 20888`

The web server will return a simple HTTP response:
```
HTTP/1.1 200 OK
Content-Type: text/plain
Content-Length: 6
Connection: close

Hello!
```
