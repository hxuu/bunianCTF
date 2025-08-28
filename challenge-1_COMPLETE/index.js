// To run the challenge:
// npm i express
// node index.js
//
// your task is to login :)
// made by: @hxuu
const express = require('express');
const crypto = require('crypto');
const app = express();

app.use(express.urlencoded({ extended: true }));

let users = {
    "admin": {
        // you can't see this, it's randomly generated
        "password": crypto.randomBytes(32).toString('hex'),
    }
};

app.post("/login", (req, res) => {
    const { username, password } = req.body;
    const user = users[username];

    if (user && user.password === password) {
        return res.send(` Congrat! you logged in >_< !! \n Your flag is: Bunian{${crypto.randomBytes(16).toString('hex')}}`);
    }
    res.send(" You couldn't log in :( ");
});

app.post("/vuln", (req, res) => {
    const { username, settings } = req.body;
    if (username === "admin") {
        return res.send("not ok");
    }
    Object.assign(users[username] || {}, settings);
    res.send("ok");
});

app.listen(3000, () => console.log('Server running on port 3000'));

