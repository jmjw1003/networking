# Project 1: A better web server
### Requirements
Time to improve the web server so that it serves actual files!

We’re going to make it so that when a web client (in this case we’ll use a browser) requests a specific file, the webserver will return that file.

There are some interesting details to be found along the way.

### Restrictions
In order to better understand the sockets API at a lower level, the following helper functions are forbidden:
- The `socket.create_connection()` function.
- The `socket.create_server()` function.
- Anything in the `urllib` modules.

### Extensions
- Add MIME support for other file types so you can serve JPEGs and other files.
- Add support for showing a directory listing. If the user doesn’t specify a file in the URL, show a directory listing where each file name is a link to that file.
- Instead of just dropping the entire path, allow serving out of subdirectories from a root directory your specify on the server.