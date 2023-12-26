const express = require('express')
const basicAuth = require('express-basic-auth')
const app = express()
const port = 4131

app.set("views", "templates");
app.set("view engine", "pug");

app.use(express.urlencoded({extended: true}));
app.use(express.json());

const data = require('./data.js');

let reviews = [
    {name: "Tinker Bell", message: "The news is always fresh and up to date"},
    {name: "Piglet", message: "My favorite news source ever im checking the website regularly"},
    {name: "Elsa", message: "Makes my day whenever theres a news update"},
    {name: "Pluto", message: "Best news site ever!!!"},
    {name: "Flynn", message: "So excited to hear all the movie news"}, 
    {name: "Mr. Incredible", message: "Great for any disney fan or parent with kids"},
    {name: "WALL-E", message: "Who needs twitter when you have this news source"}
];


async function addContact(param) {
    if (param.birthday != "" && param.name != "" && param.email != "") {
        if(param.rumors) {
            let res = await data.addContact(param.name, param.email, param.birthday, param.news, true);
            return 0;
        }
        else {
            let res = await data.addContact(param.name, param.email, param.birthday, param.news, false);
            return 0;
        }
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
app.post("/contact", async (req, res) => {
    if(req.body != null) {
        let succ = await addContact(req.body);
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
async (req, res) => {
    let contacts = await data.getContacts();
    res.render("contactlog.pug", {contacts});
})

//deletes a contact
app.delete("/api/contact", basicAuth({
    users: { 'admin': 'password' },
    challenge: true
}), 
async (req, res) => {
    if(req.header('Content-type') == 'application/json' && req.body.length < 3) {
        await data.deleteContact(req.body.id)
        res.sendStatus(200);
    }
    else {
        res.sendStatus(400);
    }
})

//gets a sale
app.get("/api/sale", async (req, res) => {
    let sale = await data.getLastSale();
    res.setHeader('Content-Type', 'application/json');
    res.send(JSON.stringify(sale[0]));
})

//sets a sale
app.post("/api/sale", basicAuth({
    users: { 'admin': 'password' },
    challenge: true
}),
async (req, res) => {
    if(req.header('Content-type') == 'application/json' && req.body.length < 3) {
        await data.addSale(req.body.message);
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
async (req, res) => {
    await data.endSale();
    res.sendStatus(200);
})

//returns the sales log
app.get("/admin/salelog", basicAuth({
    users: { 'admin': 'password' },
    challenge: true
}), 
async (req, res) => {
    res.send(await data.getRecentSales());
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