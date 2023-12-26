// this package behaves just like the mysql one, but uses async await instead of callbacks.
const mysql = require(`mysql-await`); // npm install mysql-await

// first -- I want a connection pool: https://www.npmjs.com/package/mysql#pooling-connections

// this is used a bit differently, but I think it's just better -- especially if server is doing heavy work.
var connPool = mysql.createPool({
    connectionLimit: 5, // it's a shared resource, let's not go nuts.
    host: "localhost",// this will work
    user: "C4131F23U181",
    database: "C4131F23U181",
    password: "32811", // we really shouldn't be saving this here long-term - and I probably shouldn't be sharing it with you...
});

// later you can use connPool.awaitQuery(query, data) -- it will return a promise for the query results.
// you CAN change the parameters for this function. please do not change the parameters for any other function in this file.

async function addContact(name, email, birthday, news, rumors){

    await connPool.awaitQuery("insert into contacts (username, email, birthday, news, rumors) values (?, ?, ?, ?, ?)", 
                            [name, email, birthday, news, rumors]);
}

async function deleteContact(id){

    let result = await connPool.awaitQuery("delete from contacts where id=?", [id]);

    if (result.affectedRows > 0) {
        return true;
    }
    else {
        return false;
    }
}

async function getContacts() {
    let contacts = await connPool.awaitQuery("select * from contacts");

    let result = {};
    
    for (let i = 0; i < contacts.length; i++) {
        let rum = "no rumors";
        if (contacts[i].rumors == 1) {
            rum = "wants rumors";
        }

        result[contacts[i].id] = {name : contacts[i].username, 
                                  email: contacts[i].email, 
                                  birthday: contacts[i].birthday, 
                                  news: contacts[i].news, 
                                  rumors: rum
        }
    }
    return result;
}


async function addSale(message) {
    await connPool.awaitQuery("insert into sales (content) values (?)", [message]);
}


async function endSale() {
    await connPool.awaitQuery("update sales set endTime = CURRENT_TIMESTAMP where endTime is null");
}

async function getLastSale() {
    let result = await connPool.awaitQuery("select * from sales order by startTime DESC limit 1");
    return result;
}

async function getRecentSales() {
    let result = await connPool.awaitQuery("select * from sales order by startTime DESC limit 3");
    let lst = [];
    for (let i = 0; i < result.length; i++) {
        if(result[i].endTime != null) {
            lst[i] = {message: result[i].content, active: false};
        }
        else {
            lst[i] = {message: result[i].content, active: true};
        }
    }

    return lst;
}

module.exports = {addContact, getContacts, deleteContact, addSale, endSale, getRecentSales, getLastSale}
