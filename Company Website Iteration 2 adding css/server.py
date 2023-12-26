from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib

# PUT YOUR GLOBAL VARIABLES AND HELPER FUNCTIONS HERE.
# It is not required, but is is strongly recommended that you write a function to parse form data out of the URL, and a second function for generating the contact log page html.

contacts = { "Woody": ["Woody@gmail.com", "03-20-2002", "All News", "no rumors"], 
            "Buzz": ["Buzz@gmail.com", "11-09-1996", "Movies", "wants rumors"] }

def setParams(params):
    name = "no name"
    email = "no email"
    birthdate = "no birthate"
    news = "All News"
    rumor = "off"
    #convert url string to normal characters and split the parameters
    normParams = urllib.parse.unquote(params, encoding='utf-8', errors='replace')
    vals = (normParams.split("&"))
    for i in range(len(vals)):
        key = vals[i].split("=")[0]
        val = vals[i].split("=")[1]
        if key == "name":
            name = val
        elif key == "email":
            email = val
        elif key == "birthday":
            birthdate = val
        elif key == "news":
            news = val
        elif key == "rumors":
            print(val)
            if val == "on":
                rumor = "wants rumors"
            else:
                rumor = "no rumors"
    contacts[name] = [email, birthdate, news, rumor]

def contactlogPage():   
    page = ""
    header = """<!DOCTYPE html>
            <html lang = "en">
            <head>
                <meta charset="UTF-8">
                <title>Contact</title>
                <link rel="stylesheet" href="/main.css">
            </head>

            <body id="contact">
                <nav>
                    <a href="/mainpage">The Magical Report</a>
                    <a href="/contactform">Mailing List</a>
                    <a href="/testimonies">Reviews</a>
                    <a href="/admin/contactlog">Contact Log</a>
                </nav>

                <h1>Contact List</h1>

                <table>
                    <tr>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Birthday</th>                                
                        <th>News</th>
                        <th>Rumors</th>
                    </tr>
            """
    page += header

    counter = 0
    for i in contacts:
        if counter % 2 == 0:
            page += "<tr class=\"even\">"
        else:
            page += "<tr>"
        page += "<td>" + i + "</td>"
        val_list = contacts[i]
        for x in range(len(val_list)):
            if x != 0:
                page += "<td>" + val_list[x] + "</td>"
            else:
                page += "<td> <a href=mailto:\"" + val_list[x] + "\">" + val_list[x] + "</a>"
        page += "</tr>"
        counter += 1
    page += """</table>       
        </body>
    </html>
            """

    return page, "text/html"



def server(url):
    """
    url is a *PARTIAL* URL. If the browser requests `http://localhost:4131/contact?name=joe#test`
    then the `url` parameter will have the value "/contact?name=joe". So you can expect the PATH
    and any PARAMETERS from the url, but nothing else.

    This function is called each time another program/computer makes a request to this website.
    The URL represents the requested file.

    This function should return two strings in a list or tuple. The first is the content to return
    The second is the content-type.
    """
    #YOUR CODE GOES HERE!

    #get a copy of the url in case there is no path
    result = ((url.split("?")[0]).split("#"))[0]
    if len(url.split("?")) > 1:
        params = ((url.split("?")[1]).split("#"))[0]
    if result == "/":
        result = "static/html/mainpage.html" 
        file = open(result).read()
        return file, "text/html"
        #if there is a path cut off the / and return the html file
    elif result == "/main.css":
        result = "static/css" + result
        file = open(result, "rb").read()
        return file, "text/css"
    elif result == "/admin/contactlog":
        return contactlogPage()
    elif result == "/images/main":
        file = open("static/images/main.jpg", "rb").read()
        return file, "image/jpeg"
    else:
        if result == "/contacts":
            setParams(params)
            result = "/contactform"
        result = "static/html" + result + ".html"
        file = open(result).read()
        return file, "text/html"
    return "static/html/404.html", "text/html"

# You shouldn't need to change content below this. It would be best if you just left it alone.

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Call the student-edited server code.
        message, content_type = server(self.path)

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
        self.send_header("Content-Type", content_type)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()

        # Send the file.
        self.wfile.write(message)
        return

def run():
    PORT = 4131
    print(f"Starting server http://localhost:{PORT}/")
    server = ('', PORT)
    httpd = HTTPServer(server, RequestHandler)
    httpd.serve_forever()
run()

