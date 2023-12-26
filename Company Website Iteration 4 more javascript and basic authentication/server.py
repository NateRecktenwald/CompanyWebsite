from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib #Only for parse.unquote and parse.unquote_plus.
import json
import base64
from typing import Union, Optional
import re
# If you need to add anything above here you should check with course staff first.

contacts = { "Woody": ["Woody@gmail.com", "03-20-2002", "All News", "no rumors"], 
            "Buzz": ["Buzz@gmail.com", "01-20-2024", "Movies", "wants rumors"], 
            "nate": ["nate@gmail.com", "11-09-2025", "Parks", "no rumors"],
            "john": ["john@gmail.com", "02-29-2346", "Tv Shows", "wants rumors"],
            "rex": ["rex@gmail.com", "05-01-2598", "Movies", "wants rumors"],
            "Bob": ["Bob@gmail.com", "12-18-2023", "Cruise", "no rumors"] }


sale_desc = ""
sale_cur = False

#take the form input and adds it the contact form data structure
def setParams(params):
    global contacts
    name = ""
    email = ""
    birthdate = ""
    news = "All News"
    rumor = "no rumors"
    count = 2
    #convert url string to normal characters and split the parameters
    try:
        normParams = urllib.parse.unquote(params, encoding='utf-8', errors='replace')
    except:
        return 0
    vals = (normParams.split("&"))

    if(len(vals) > 4):
        return 0
    
    for i in range(len(vals)):
        key = vals[i].split("=")[0]
        val = vals[i].split("=")[1]
        if key == "name":
            name += val.replace('+', ' ')
            count += 1
        elif key == "email":
            email = val
            count += 1
        elif key == "birthday":
            temp = val.split("-")
            if(val != ""):
                birthdate = temp[1] + "-" + temp[2] + "-" + temp[0]
        elif key == "news":
            news = val
        elif key == "rumors":
            if val == "on":
                rumor = "wants rumors"
            else:
                rumor = "no rumors"


    if count == 4 and birthdate != "":
        contacts[name] = [email, birthdate, news, rumor]
        return 1
    else:
        return 0
    
#create the contact log page
def contactlogPage():   
    global contacts
    page = ""
    header = """<!DOCTYPE html>
            <html lang = "en">
            <head>
                <meta charset="UTF-8">
                <title>Contact</title>
                <link rel="stylesheet" href="/main.css" class ="light">
                <link rel="stylesheet" href="/main.dark.css" class="dark">
                <script src="/js/main.js" defer></script>
                <script src="/js/table.js" defer></script>
                <script src="/js/sale.admin.js" defer></script>
            </head>

            <body id="body">
                <nav>
                    <a href="/main">The Magical Report</a>
                    <a href="/contact">Mailing List</a>
                    <a href="/testimonies">Reviews</a>
                    <a href="/admin/contactlog">Contact Log</a>
                    <button type="button" name="theme" id="theme">Toggle: Dark Mode</button>
                </nav>

                <div id="sale_block">
                    <div id="set_sale">
                        <p id="change_sale">Set Sale</p>
                        <form>
                            <div id="sale_input">
                                <label for="sale_text">Sale text</label>
                                <input type="text" id="sale_text" name="sale_text" value="">
                            </div>

                            <div id="start_sale">
                                <button type="button" name="set" id="set">Start Sale</button>
                            </div>

                            <div id="end_sale">
                                <button type="button" name="end" id="end">End Sale</button>
                            </div>
                        </form>
                    </div>
                </div>

                <h1>Contact List</h1>

                <table id=\"log\">
                    <tbody id=\"table_body\">
                    <tr>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Birthday</th>                                
                        <th>News</th>
                        <th>Rumors</th>
                        <th>Row Deletion</th>
                    </tr>
            """
    page += header

    counter = 0
    for i in contacts:
        if counter % 2 == 0:
            page += "<tr class=\"even\" id=\"index " + str(counter) + "\">"
        else:
            page += "<tr id=\"index " + str(counter) + "\">"
        page += "<td>" + i + "</td>"
        val_list = contacts[i]
        name = i
        for x in range(len(val_list)):
            if x != 0:
                page += "<td>" + val_list[x] + "</td>"
            elif x == 0:
                page += "<td> <a href=mailto:\"" + val_list[x] + "\">" + val_list[x] + "</a>"
        page += "<td> <button type=\"button\" name=\"delete\" id=" + name + ">remove</button> </td>"
        page += "</tr>"
        counter += 1

    page += """ </tbody>
            </table>       
        </body>
    </html>
            """

    return page, 200, {"Content-Type": "text/html; charset=utf-8"}

def auth(headers: dict[str, str]):
    if headers["Authorization"] != None:
        coded = headers["Authorization"]
        coded = coded.split(" ")[1]
        decoded = base64.b64decode(coded).decode("utf-8")
        arr = decoded.split(":")
        username = arr[0]
        password = arr[1]
        if username == "admin" and password == "password":
            return 200
        else:
            return 403
    else:
        return 401


# The method signature is a bit "hairy", but don't stress it -- just check the documentation below.
def server(method: str, url: str, body: Optional[str], headers: dict[str, str]) -> tuple[Union[str, bytes], int, dict[str, str]]:    
    """
    method will be the HTTP method used, for our server that's GET, POST, DELETE
    url is the partial url, just like seen in previous assignments
    body will either be the python special None (if the body wouldn't be sent)
         or the body will be a string-parsed version of what data was sent.
    headers will be a python dictionary containing all sent headers.

    This function returns 3 things:
    The response body (a string containing text, or binary data)
    The response code (200 = ok, 404=not found, etc.)
    A _dictionary_ of headers. This should always contain Content-Type as seen in the example below.
    """
    global sale_desc
    global sale_cur
    global contacts

    # Parse URL
    result = ((url.split("?")[0]).split("#"))[0]
    if len(url.split("?")) > 1:
        params = ((url.split("?")[1]).split("#"))[0]

    #figure which file to retriece and return it
    if(method == "GET"):
        if result == "/": 
            result = "static/html/mainpage.html" 
            file = open(result).read()
            return file, 200, {"Content-Type": "text/html; charset=utf-8"}
        elif result == "/main.css": 
            result = "static/css/main.css"
            file = open(result, "rb").read()
            return file, 200, {"Content-Type": "text/css; charset=utf-8"}
        elif result == "/admin/contactlog": 
            code = auth(headers)
            if(code == 200):
                return contactlogPage()
            elif(code == 403):
                return "", code, {"WWW-Authenticate": "Basic realm=user visible realm"}
            else:
                return "", code, {"WWW-Authenticate": "Basic realm=user visible realm"}
        elif result == "/images/main": 
            file = open("static/images/main.jpg", "rb").read()
            return file, 200, {"Content-Type": "image/jpeg; charset=utf-8"}
        elif result == "/testimonies": 
            result = "static/html/testimonies.html"
            file = open(result).read()
            return file, 200, {"Content-Type": "text/html; charset=utf-8"}
        elif result == "/main": 
            result = "static/html/mainpage.html" 
            file = open(result).read()
            return file, 200, {"Content-Type": "text/html; charset=utf-8"}
        elif result == "/contact": 
            result = "static/html/contactform.html"
            file = open(result).read()
            return file, 200, {"Content-Type": "text/html; charset=utf-8"}
        elif result == "/main.dark.css": 
            result = "static/css/main.dark.css"
            file = open(result, "rb").read()
            return file, 200, {"Content-Type": "text/css; charset=utf-8"}
        elif result == "/js/table.js": 
            result = "static/js/table.js"
            file = open(result, "rb").read()
            return file, 200, {"Content-Type": "text/javascript; charset=utf-8"}
        elif result == "/js/contact.js": 
            result = "static/js/contact.js"
            file = open(result, "rb").read()
            return file, 200, {"Content-Type": "text/javascript; charset=utf-8"}
        elif result == "/js/main.js": 
            result = "static/js/main.js"
            file = open(result, "rb").read()
            return file, 200, {"Content-Type": "text/javascript; charset=utf-8"}
        elif result == "/js/sale.banner.js":
            result = "static/js/sale.banner.js"
            file = open(result, "rb").read()
            return file, 200, {"Content-Type": "text/javascript; charset=utf-8"}
        elif result == "/js/sale.admin.js":
            result = "static/js/sale.admin.js"
            file = open(result, "rb").read()
            return file, 200, {"Content-Type": "text/javascript; charset=utf-8"}
        elif result == "/api/sale": 
            x = {
                "active": sale_cur,
                "message": sale_desc
            }
            obj = json.dumps(x)
            return obj, 200, {"Content-Type": "application/json; charset=utf-8"}
        else: 
            return open("static/html/404.html").read(), 404, {"Content-Type": "text/html; charset=utf-8"}
    elif (method == "POST"):
        if result == "/contact":
            params = body
            success = setParams(params)
            result = """<!DOCTYPE html>
                <html lang = "en">
                <head>
                    <meta charset="UTF-8">
                    <title>Contact Result</title>
                    <link rel="stylesheet" href="/main.css" class ="light">
                    <link rel="stylesheet" href="/main.dark.css" class="dark">
                    <script src="/js/main.js" defer></script>
                </head>

                <body id="body">
                    <nav>
                        <a href="/main">The Magical Report</a>
                        <a href="/contact">Mailing List</a>
                        <a href="/testimonies">Reviews</a>
                        <a href="/admin/contactlog">Contact Log</a>
                        <button type="button" name="theme" id="theme">Toggle: Dark Mode</button>
                    </nav>
                    """

            if(success == 1):
                result += "<h1>Sucessfuly Signed Up!</h1>"
                statusCode = 201
            else:
                result += "<h1>Form didn't submit properly</h1>"
                statusCode = 400

            result += """</body>
            </html>
                """
            return result, statusCode, {"Content-Type": "text/html; charset=utf-8"}
        elif result == "/api/sale":
            code = auth(headers)
            if(code == 200):
                if (headers["Content-Type"] == "application/json"):
                    try: 
                        cont = json.loads(body)
                    except:
                        print("not valid json")
                        return "", 400, {}
                    try: 
                        cont = cont["message"]
                    except:
                        print("no message")
                        return "", 400, {}
                    sale_desc = ""
                    sale_desc = cont
                    sale_cur = True
                    return "", 200, {}
                else:
                    print("the content is not json")
                    return "", 400, {}
            elif(code == 403):
                return "", code, {"WWW-Authenticate": "Basic realm=user visible realm"}
            else:
                return "", code, {"WWW-Authenticate": "Basic realm=user visible realm"}
        else:
            return open("static/html/404.html").read(), 404, {"Content-Type": "text/html; charset=utf-8"}
    elif (method == "DELETE"):
        if result == "/api/contact":
            code = auth(headers)
            if(code == 200):
                if (headers["Content-Type"] == "application/json"):
                    try:
                        cont = json.loads(body)
                    except: 
                        print("Not valid body")
                        return "", 400, {}
                    try: 
                        cont = cont["id"]
                    except:
                        print("no id key in the message")
                        return "", 400, {}
                    try:
                        del contacts[cont]
                        print(contacts)
                        return "", 200, {}
                    except:
                        print("cannot find the contact")
                        return "", 404, {}
                else:
                    print("No content header type")
                    return "", 400, {}
            elif(code == 403):
                return "", code, {"WWW-Authenticate": "Basic realm=user visible realm"}
            else:
                return "", code, {"WWW-Authenticate": "Basic realm=user visible realm"}   
        elif result == "/api/sale":
            code = auth(headers)
            if(code == 200):
                sale_cur = False
                return "", 200, {}
            elif(code == 403):
                return "", code, {"WWW-Authenticate": "Basic realm=user visible realm"}
            else:
                return "", code, {"WWW-Authenticate": "Basic realm=user visible realm"}
        else:
            return open("static/html/404.html").read(), 404, {"Content-Type": "text/html; charset=utf-8"}
    else:
        return open("static/html/404.html").read(), 404, {"Content-Type": "text/html; charset=utf-8"}

    # And another freebie -- the 404 page will probably look like this.
    # Notice how we have to be explicit that "text/html" should be the value for
    # header: "Content-Type" now?]
    # I am sorry that you're going to have to do a bunch of boring refactoring.
    #return open("static/html/404.html").read(), 404, {"Content-Type": "text/html; charset=utf-8"}





# You shouldn't need to change content below this. It would be best if you just left it alone.


class RequestHandler(BaseHTTPRequestHandler):
    def c_read_body(self):
        # Read the content-length header sent by the BROWSER
        content_length = int(self.headers.get("Content-Length", 0))
        # read the data being uploaded by the BROWSER
        body = self.rfile.read(content_length)
        # we're making some assumptions here -- but decode to a string.
        body = str(body, encoding="utf-8")
        return body

    def c_send_response(self, message, response_code, headers):
        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")
        
        # Send the first line of response.
        self.protocol_version = "HTTP/1.1"
        self.send_response(response_code)
        
        # Send headers (plus a few we'll handle for you)
        for key, value in headers.items():
            self.send_header(key, value)
        self.send_header("Content-Length", len(message))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()

        # Send the file.
        self.wfile.write(message)
        

    def do_POST(self):
        # Step 1: read the last bit of the request
        try:
            body = self.c_read_body()
        except Exception as error:
            # Can't read it -- that's the client's fault 400
            self.c_send_response("Couldn't read body as text", 400, {'Content-Type':"text/plain"})
            raise
                
        try:
            # Step 2: handle it.
            message, response_code, headers = server("POST", self.path, body, self.headers)
            # Step 3: send the response
            self.c_send_response(message, response_code, headers)
        except Exception as error:
            # If your code crashes -- that's our fault 500
            self.c_send_response("The server function crashed.", 500, {'Content-Type':"text/plain"})
            raise
        

    def do_GET(self):
        try:
            # Step 1: handle it.
            message, response_code, headers = server("GET", self.path, None, self.headers)
            # Step 3: send the response
            self.c_send_response(message, response_code, headers)
        except Exception as error:
            # If your code crashes -- that's our fault 500
            self.c_send_response("The server function crashed.", 500, {'Content-Type':"text/plain"})
            raise


    def do_DELETE(self):
        # Step 1: read the last bit of the request
        try:
            body = self.c_read_body()
        except Exception as error:
            # Can't read it -- that's the client's fault 400
            self.c_send_response("Couldn't read body as text", 400, {'Content-Type':"text/plain"})
            raise
        
        try:
            # Step 2: handle it.
            message, response_code, headers = server("DELETE", self.path, body, self.headers)
            # Step 3: send the response
            self.c_send_response(message, response_code, headers)
        except Exception as error:
            # If your code crashes -- that's our fault 500
            self.c_send_response("The server function crashed.", 500, {'Content-Type':"text/plain"})
            raise



def run():
    PORT = 4133
    print(f"Starting server http://localhost:{PORT}/")
    server = ("", PORT)
    httpd = HTTPServer(server, RequestHandler)
    httpd.serve_forever()


run()
