// server.js
const express = require('express');

const app = express();
app.use(express.json()); // parse JSON body

app.post('/test', (req, res) => {
  console.log('Received body:', req.body);
  res.json({ message: 'POST received successfully', data: req.body });
});

const PORT = 8500;
app.listen(PORT, () => {
  console.log(`Server running on ${PORT}`);
});