const express = require('express');
const app = express();
const fs = require('fs')
const Docker = require('dockerode')
const PORT = process.env.PORT || 3000;

const docker = new Docker()
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// APIs 
app.get("/", (req, res) => {
    res.send("Hello world")
});

app.post("/execute", async (req, res) => {
    const id = req.params.id;
    const code = req.body.code;

    await runCodeInContainer(code);
    res.send("Successfully run the code.")
});

// Helper function.
const runCodeInContainer = async (userCode) => {
    const container = await docker.createContainer({
        Image: "python:3.11-slim",
        Cmd: ["python3", "-c", userCode]
    });

    await container.start();
    const output = await container.wait();
    const logs = await container.logs({ stdout: true, stderr: true });
    console.log(output)

    console.log(logs.toString());

    await container.remove();
};

app.listen(PORT, () => {
    console.log("Server is Listening at PORT: ", PORT);
})