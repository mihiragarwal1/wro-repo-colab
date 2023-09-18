const express = require('express');
const app = express();
const server = require('http').Server(app);

// Define your IP variable
let ip;

// Middleware to set the IP variable
app.use((req, res, next) => {
    ip = req.ip || req.socket.remoteAddress;
    next();
});

const static = express.static(__dirname);
app.get('/', (req, res) => {
    res.writeHead(301, { location: '/Car_Control/' });
    res.end();
});
app.use('/', (req, res, next) => {
    if (!ip.replace('::ffff:', '').startsWith('127.') && !(ip.endsWith(':1') && ip.replace(/[^0-9]/ig, '').split('').reduce((prev, curr) => prev + parseInt(curr), 0) == 1)) {
        res.sendStatus(403);
    }
    static(req, res, next);
});

// Pass the IP variable to the client-side JavaScript
app.get('/getip', (req, res) => {
    res.json({ ip });
});

server.listen(8081);

console.log("server Started");
