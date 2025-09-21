// server.js
const http = require("http");
const url = require("url");
const fs = require("fs");
const path = require("path");

const PORT = 8080;

const server = http.createServer((req, res) => {
    const parsed = url.parse(req.url, true);
    const fileParam = parsed.query.file;
    if (!fileParam) {
        res.writeHead(400, {"Content-Type":"text/plain"});
        return res.end("Missing file param");
    }

    const filePath = path.resolve(fileParam);
    try {
        const stats = fs.statSync(filePath);
        res.writeHead(200, {"Content-Type":"application/octet-stream", "Content-Length": stats.size});
        fs.createReadStream(filePath).pipe(res);
    } catch (err) {
        res.writeHead(404, {"Content-Type":"text/plain"});
        res.end("File not found");
    }
});

server.listen(PORT, () => {
    console.log(`Server listening on ${PORT}`);
});

