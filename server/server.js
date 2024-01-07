const express = require('express');
const app = express();
const fs = require('fs')
const axios = require('axios')
const CircularJson = require('circular-json')
const amqp = require('amqplib');
const PORT = process.env.PORT || 3000;
const queueUrl = process.env.QUEUE_URL || "amqp://guest:guest@localhost:5672";

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// APIs 
app.get("/", (req, res) => {
    res.send("Hello world")
});

// app.post("/execute", async (req, res) => {
//     try {
//         const code = req.body.code;
//         const userId = req.body.userId;

//         const data = await axios.post(`${queueUrl}/execute`, {
//             userCode: code,
//             userId: userId,
//         });
//         result = data.data;
//         console.log(result);
//         res.status(200).json({result: CircularJson.stringify(result)});
//     } catch (err) {
//         console.log("Error in executing code", err);
//         return res.status(500).json({ error: err })
//     }
// });

app.post('/sendTask', async (req, res) => {
    try {
      const connection = await amqp.connect(queueUrl);
      const channel = await connection.createChannel();
  
      const queueName = 'task';
      await channel.assertQueue(queueName, { durable: false });
  
      const taskMessage = JSON.stringify(req.body)
      channel.sendToQueue(queueName, Buffer.from(taskMessage));
  
      console.log(`Task sent: ${taskMessage}`);
  
      await channel.close();
      await connection.close();
  
      res.send('Task sent successfully');
    } catch (error) {
      console.error('Error sending task:', error);
      res.status(500).send('Internal Server Error');
    }
});

app.listen(PORT, () => {
    console.log("Server is Listening at PORT: ", PORT);
})
