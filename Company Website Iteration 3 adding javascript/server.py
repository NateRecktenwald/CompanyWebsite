from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib

# PUT YOUR GLOBAL VARIABLES AND HELPER FUNCTIONS HERE.
# It is not required, but is is strongly recommended that you write a function to parse form data out of the URL, and a second function for generating the contact log page html.

contacts = { "Woody": ["Woody@gmail.com", "03-20-2002", "All News", "no rumors"], 
            "Buzz": ["Buzz@gmail.com", "01-20-2024", "Movies", "wants rumors"], 
            "nate": ["nate@gmail.com", "11-09-2025", "Parks", "no rumors"],
            "john": ["john@gmail.com", "02-29-2346", "Tv Shows", "wants rumors"],
            "rex": ["rex@gmail.com", "05-01-2598", "Movies", "wants rumors"],
            "Bob": ["Bob@gmail.com", "12-18-2023", "Cruise", "no rumors"] }

def setParams(params):
    name = ""
    email = ""
    birthdate = ""
    news = "All News"
    rumor = ""
    count = 2
    #convert url string to normal characters and split the parameters
    normParams = urllib.parse.unquote(params, encoding='utf-8', errors='replace')
    vals = (normParams.split("&"))
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
            birthdate = val
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



def contactlogPage():   
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
            </head>

            <body id="body">
                <nav>
                    <a href="/main">The Magical Report</a>
                    <a href="/contact">Mailing List</a>
                    <a href="/testimonies">Reviews</a>
                    <a href="/admin/contactlog">Contact Log</a>
                    <button type="button" name="theme" id="theme">Toggle: Dark Mode</button>
                </nav>

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
        for x in range(len(val_list)):
            if x != 0:
                page += "<td>" + val_list[x] + "</td>"
            elif x == 0:
                page += "<td> <a href=mailto:\"" + val_list[x] + "\">" + val_list[x] + "</a>"
        page += "<td> <button type=\"button\" name=\"delete\" id=\"delete\">remove</button> </td>"
        page += "</tr>"
        counter += 1

    page += """ </tbody>
            </table>       
        </body>
    </html>
            """

    return page, "text/html", 200


def server_GET(url: str) -> tuple[str | bytes, str, int]:
    """
    url is a *PARTIAL* URL. If the browser requests `http://localhost:4131/contact?name=joe`
    then the `url` parameter will have the value "/contact?name=joe". (so the schema and
    authority will not be included, but the full path, any query, and any anchor will be included)

    This function is called each time another program/computer makes a request to this website.
    The URL represents the requested file.

    This function should return three values (string or bytes, string, int) in a list or tuple. The first is the content to return
    The second is the content-type. The third is the HTTP Status Code for the response
    """
    #YOUR CODE GOES HERE!
    result = ((url.split("?")[0]).split("#"))[0]
    if len(url.split("?")) > 1:
        params = ((url.split("?")[1]).split("#"))[0]

    if result == "/":
        result = "static/html/mainpage.html" 
        file = open(result).read()
        return file, "text/html", 200
    elif result == "/main.css":
        result = "static/css/main.css"
        file = open(result, "rb").read()
        return file, "text/css", 200
    elif result == "/admin/contactlog":
        return contactlogPage()
    elif result == "/images/main":
        file = open("static/images/main.jpg", "rb").read()
        return file, "image/jpeg", 200
    elif result == "/testimonies": 
        result = "static/html/testimonies.html"
        file = open(result).read()
        return file, "text/html", 200
    elif result == "/main": 
        result = "static/html/mainpage.html"
        file = open(result).read()
        return file, "text/html", 200
    elif result == "/contact": 
        result = "static/html/contactform.html"
        file = open(result).read()
        return file, "text/html", 200
    elif result == "/main.dark.css": 
        result = "static/css/main.dark.css"
        file = open(result, "rb").read()
        return file, "text/css", 200
    elif result == "/js/table.js": 
        result = "static/js/table.js"
        file = open(result, "rb").read()
        return file, "text/javascript", 200
    elif result == "/js/contact.js": 
        result = "static/js/contact.js"
        file = open(result, "rb").read()
        return file, "text/javascript", 200
    elif result == "/js/main.js": 
        result = "static/js/main.js"
        file = open(result, "rb").read()
        return file, "text/javascript", 200
    else: 
        return "static/html/404.html", "text/html", 404

def server_POST(url: str, body: str) -> tuple[str | bytes, str, int]:
    """
    url is a *PARTIAL* URL. If the browser requests `http://localhost:4131/contact?name=joe`
    then the `url` parameter will have the value "/contact?name=joe". (so the schema and
    authority will not be included, but the full path, any query, and any anchor will be included)

    This function is called each time another program/computer makes a POST request to this website.

    This function should return three values (string or bytes, string, int) in a list or tuple. The first is the content to return
    The second is the content-type. The third is the HTTP Status Code for the response
    """
    result = ((url.split("?")[0]).split("#"))[0]
    params = body
    statusCode = 400

    if result == "/contacts":
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
        return result, "text/html", statusCode
    else:
        return "static/html/404.html", "text/html", 404

# You shouldn't need to change content below this. It would be best if you just left it alone.

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Read the content-length header sent by the BROWSER
        content_length = int(self.headers.get('Content-Length',0))
        # read the data being uploaded by the BROWSER
        body = self.rfile.read(content_length)
        # we're making some assumptions here -- but decode to a string.
        body = str(body, encoding="utf-8")

        message, content_type, response_code = server_POST(self.path, body)

        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")

        # prepare the response object with minimal viable headers.
        self.protocol_version = "HTTP/1.1"
        # Send response code
        self.send_response(response_code)
        # Send headers
        # Note -- this would be binary length, not string length
        self.send_header("Content-Length", len(message))
        self.send_header("Content-Type", content_type)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()

        # Send the file.
        self.wfile.write(message)
        return

    def do_GET(self):
        # Call the student-edited server code.
        message, content_type, response_code = server_GET(self.path)

        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")

        # prepare the response object with minimal viable headers.
        self.protocol_version = "HTTP/1.1"
        # Send response code
        self.send_response(response_code)
        # Send headers
        # Note -- this would be binary length, not string length
        self.send_header("Content-Length", len(message))
        self.send_header("Content-Type", content_type)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()

        # Send the file.
        self.wfile.write(message)
        return


def run():
    PORT = 4131
    print(f"Starting server http://localhost:{PORT}/")
    server = ("", PORT)
    httpd = HTTPServer(server, RequestHandler)
    httpd.serve_forever()


run()
