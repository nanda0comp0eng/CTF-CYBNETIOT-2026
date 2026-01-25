const express = require("express");
const path = require("path");
const fs = require("fs");
const cookieParser = require("cookie-parser");
const crypto = require("crypto");
const { exec } = require("child_process");

const app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cookieParser());
app.use(express.static("public"));

const port = 3000;
const notes_dir = path.join(__dirname, "notes");
const allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_";

if (!fs.existsSync(notes_dir)) fs.mkdirSync(notes_dir, { recursive: true });

function check_uuid(uuid) {
    const uuid_regex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/;
    return uuid_regex.test(uuid);
}

function gen_uuid_v4() {
    const b = crypto.randomBytes(16);
    b[6] = (b[6] & 0x0f) | 0x40;
    b[8] = (b[8] & 0x3f) | 0x80;
    const hex = b.toString("hex");
    return `${hex.slice(0, 8)}-${hex.slice(8, 12)}-${hex.slice(12, 16)}-${hex.slice(16, 20)}-${hex.slice(20)}`;
}

function auth(req, res, next) {
    const uuid = req.cookies.uuid;
    if (uuid && check_uuid(uuid)) {
        req.uuid = uuid;
        return next();
    }
    const new_uuid = gen_uuid_v4();
    res.cookie("uuid", new_uuid);
    req.uuid = new_uuid;
    return next();
}

function sanitize_filename(filename) {
    let out = filename;
    let length = out.length;
    for (let i = 0; i < length; i++) {
        const char = out[i];
        if (!allowed_chars.includes(char)) {
            out = out.replace(char, "__");
        }
    }
    return out;
}

function ensure_user_dir(uuid) {
    const userBase = path.join(notes_dir, uuid);
    if (!fs.existsSync(userBase)) fs.mkdirSync(userBase, { recursive: true });
    return userBase;
}

function write_file_vuln(filepath, b64data) {
    return new Promise((resolve, reject) => {
        exec(`echo ${b64data} | base64 -d > ${filepath}`, (err, stdout, stderr) => {
            if (err) return reject(err.message);
            if (stderr) return reject(stderr);
            return resolve(stdout);
        });
    });
}


function read_file_safe(filepath) {
    try {
        return fs.readFileSync(filepath, "utf8");
    } catch {
        return null;
    }
}

app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, "public", "index.html"));
});

app.post("/create", auth, async (req, res) => {
    const uuid = req.uuid;
    const name = (req.body.name || "").toString();
    const body = (req.body.body || "").toString();

    if (!name || !body) {
        return res.status(400).json({ error: true, message: "Name and body must be specified" });
    }

    const base = ensure_user_dir(uuid);

    const safeName = sanitize_filename(name);
    const notePath = path.join(base, safeName + ".txt");

    const b64ed = Buffer.from(body, "utf8").toString("base64");

    try {
        await write_file_vuln(notePath, b64ed);
        return res.json({ message: safeName + ".txt" });
    } catch (e) {
        return res.json({ message: safeName + ".txt" });

    }
});

app.get("/read", auth, (req, res) => {
    const uuid = req.uuid;
    const name = path.basename(decodeURIComponent(req.query.name || "").toString());
    if (!name) return res.status(400).send("Name must be specified");

    const base = ensure_user_dir(uuid);
    const notePath = path.join(base, name);

    const data = read_file_safe(notePath);
    if (!data) return res.status(404).send("Note doesn't exist");

    res.type("text/plain").send(data);
});

app.get("/list", auth, (req, res) => {
    const uuid = req.uuid;
    const base = ensure_user_dir(uuid);

    try {
        const notes = fs.readdirSync(base);
        return res.json({ error: false, notes });
    } catch {
        return res.json({ error: false, notes: [] });
    }
});

app.listen(port, () => {
    console.log(`Listening on http://localhost:${port}`);
});
