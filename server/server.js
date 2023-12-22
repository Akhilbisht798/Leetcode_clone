const express = require('express');
const app = express();
const fs = require('fs')
const axios = require('axios')
const PORT = process.env.PORT || 3000;
const rceUrl = process.env.RCE_URL;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// APIs 
app.get("/", (req, res) => {
    res.send("Hello world")
});

app.post("/execute", async (req, res) => {
    try {
        const id = req.params.id;
        const code = req.body.code;

        const res = await axios.post(`${RCE_URL}/execute`, {
            userCode: code
        });

        console.log(res);
        res.json({res});
    } catch (err) {
        console.log("Error in executing code", err);
    }
});

app.listen(PORT, () => {
    console.log("Server is Listening at PORT: ", PORT);
})
