# Project 0: HTTP client and server
A simple http client and server, written using Python v3.12.3 on Ubuntu 24.04.

### Requirements (completed)
- Create a web client that runs from the command line and makes simple http `GET` requests.
- Create a web server that runs from the command line and implements `GET` requests.

### Restrictions - the following helper functions are forbidden:
- The `socket.create_connection()` function.
- The `socket.create_server()` function.
- Anything in the `urllib` modules.

### Extensions (completed):

1. Modify the server to print out the IP address and port of the client that just connected to it.
2. Modify the client to be able to send payloads.
3. Modify the server to extract and print out the "request method" from the request.
4. Modify the server to extract and print a payload sent by the client.

# Web client usage
The client can be accessed via the command line using the format: `$ python3 webclient.py address port payload`.</br>
Address, port and payload are optional, and will default to "example.com", 80.</br>
`$ python3 webclient.py example.com`</br>
`$ python3 webclient.py example.com 80`</br>
`$ python3 webclient.py example.com 80 "This is a text payload"`</br>
The first command will return an output like this (truncated):
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

The web server has implemented `GET`, `HEAD`, `POST`, everything else will return a `501 Not implemented`.</br>
`POST` will only accept a plain text payload, which will be echoed back in the response.</br>
Below is an example response:

```
HTTP/1.1 200 OK
Content-Type: text/plain
Content-Length: 6
Connection: close

Hello!
```
