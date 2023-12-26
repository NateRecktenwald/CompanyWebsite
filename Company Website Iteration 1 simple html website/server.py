from http.server import BaseHTTPRequestHandler, HTTPServer


def server(url):
    """
    url is a *PARTIAL* URL. If the browser requests `http://localhost:4131/contact?name=joe`
    then the `url` parameter will have the value "/contact?name=joe". (so the schema and 
    authority will not be included, but the full path, any query, and any anchor will be included)

    This function is called each time another program/computer makes a request to this website.
    The URL represents the requested file.

    This function should return a string.
    """

    #get a copy of the url in case there is no path
    result = url

    #go through the url to look for a query and/or anchor
    for i in url:
        #found a query and cut it off
        print(url)
        if i == "?":
            x = url.split("?")
            print(x)
            result = x[1]
            break
        #found a anchor and cut it off
        elif i == "#":
            print(x)
            x = url.split("#")
            result = x[1]
            break

    #if there is no path go to the mainpage
    if result == "/":
        result = "mainpage.html" 
        file = open(result).read()
        return file
        print(result)
    #if there is a path cut off the / and return the html file
    else:
        print(result)
        temp = result.split("/")
        print(temp)
        result = temp[1]+".html"
        print(result)
        file = open(result).read()
        return file
    

# You shouldn't need to change content below this. It would be best if you just left it alone.

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Call the student-edited server code.
        message = server(self.path)
        
        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")

        # prepare the response object with minimal viable headers.
        self.protocol_version = "HTTP/1.1"
        # Send response code
        self.send_response(200)
        # Send headers
        # Note -- this would be binary length, not string length
        self.send_header("Content-Length", len(message))
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

        # Send the file.
        self.wfile.write(message)
        return

def run():
    PORT = 4137
    print(f"Starting server http://localhost:{PORT}/")
    server = ('', PORT)
    httpd = HTTPServer(server, RequestHandler)
    httpd.serve_forever()
run()
