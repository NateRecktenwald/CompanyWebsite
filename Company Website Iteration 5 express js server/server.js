const express = require('express')
const basicAuth = require('express-basic-auth')
const app = express()
const port = 4131

app.set("views", "templates");
app.set("view engine", "pug");

app.use(express.urlencoded({extended: true}));
app.use(express.json());


let contacts = {0: ["Woody", "Woody@gmail.com", "03-20-2002", "All News", "no rumors"], 
                1: ["Buzz", "Buzz@gmail.com", "01-20-2024", "Movies", "wants rumors"], 
                2: ["nate", "nate@gmail.com", "11-09-2025", "Parks", "no rumors"],
                3: ["john", "john@gmail.com", "02-29-2346", "Tv Shows", "wants rumors"],
                4: ["rex", "rex@gmail.com", "05-01-2598", "Movies", "wants rumors"],
                5: ["Bob", "Bob@gmail.com", "12-18-2023", "Cruise", "no rumors"]};

let reviews = [
    {name: "Tinker Bell", message: "The news is always fresh and up to date"},
    {name: "Piglet", message: "My favorite news source ever im checking the website regularly"},
    {name: "Elsa", message: "Makes my day whenever theres a news update"},
    {name: "Pluto", message: "Best news site ever!!!"},
    {name: "Flynn", message: "So excited to hear all the movie news"}, 
    {name: "Mr. Incredible", message: "Great for any disney fan or parent with kids"},
    {name: "WALL-E", message: "Who needs twitter when you have this news source"}
];


let index = 6;

let sale_cur = false;
let sale_desc = "";

function addContact(param) {
    if (param.birthday != "" && param.name != "" && param.email != "") {
        if(param.rumors) {
            contacts[index] = [param.name, param.email, param.birthday, param.news, "wants rumors"];
        }
        else {
            contacts[index] = [param.name, param.email, param.birthday, param.news, "no rumors"];
        }
        index += 1;
        return 0;
    }
    else {
        return 1;
    }
}

//get the mainpage
app.get("/", (req, res) => {
    res.render("mainpage.pug");
})

//get the mainpage
app.get("/main", (req, res) => {
    res.render("mainpage.pug");
})

//get the contact form
app.get("/contact", (req, res) => {
    res.render("contactform.pug");
})

//post to the contact form
app.post("/contact", (req, res) => {
    if(req.header('Content-type') == 'application/json' && req.body != null) {
        let succ = addContact(req.body);
        if(succ == 0) {
            res.render("contactsucess.pug");
        }
        else {
            res.status(400).render("contactfail.pug");
        }
    }
    else {
        res.status(400).render("contactfail.pug");
    }
})

//get the testimonies page
app.get("/testimonies", (req, res) => {
    res.render("testimonies.pug", {reviews});
})

//get the contact log page
app.get("/admin/contactlog", basicAuth({
    users: { 'admin': 'password' },
    challenge: true
}), 
(req, res) => {
    res.render("contactlog.pug", {contacts});
})

//deletes a contact
app.delete("/api/contact", basicAuth({
    users: { 'admin': 'password' },
    challenge: true
}), 
(req, res) => {
    if(req.header('Content-type') == 'application/json' && req.body.length < 3) {
        delete contacts[req.body.id];
        res.sendStatus(200);
    }
    else {
        res.sendStatus(400);
    }
})

//gets a sale
app.get("/api/sale", (req, res) => {
    let x = {
        "active": sale_cur,
        "message": sale_desc
    }
    res.setHeader('Content-Type', 'application/json');
    res.send(JSON.stringify(x));
})

//sets a sale
app.post("/api/sale", basicAuth({
    users: { 'admin': 'password' },
    challenge: true
}),
(req, res) => {
    if(req.header('Content-type') == 'application/json' && req.body.length < 3) {
        sale_cur = true;
        sale_desc = req.body.message;
        res.sendStatus(200);
    }
    else {
        res.sendStatus(400);
    }
})

//ends a sale
app.delete("/api/sale", basicAuth({
    users: { 'admin': 'password' },
    challenge: true
}), 
(req, res) => {
    sale_cur = false;
    res.sendStatus(200);
})

//get static files
app.use("/resources", express.static("resources"));

//return 404 if all the paths above dont catch the request
app.use((req, res, next) => {
    res.status(404).send("Couldn't find that file");
})

//runs the server
app.listen(port , () => {
    console.log(`Example app listening on port ${port}`);
})