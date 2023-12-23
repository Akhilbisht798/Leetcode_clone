const express = require('express');
const app = express();
const fs = require('fs')
const axios = require('axios')
const CircularJson = require('circular-json')
const PORT = process.env.PORT || 3000;
const rceUrl = process.env.RCE_URL || "http://localhost:5000";

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// APIs 
app.get("/", (req, res) => {
    res.send("Hello world")
});

app.post("/execute", async (req, res) => {
    try {
        const code = req.body.code;

        const data = await axios.post(`${rceUrl}/execute`, {
            userCode: code
        });
        result = data.data;
        console.log(result);
        res.status(200).json({result: CircularJson.stringify(result)});
    } catch (err) {
        console.log("Error in executing code", err);
        return res.status(500).json({ error: err })
    }
});

app.listen(PORT, () => {
    console.log("Server is Listening at PORT: ", PORT);
})
