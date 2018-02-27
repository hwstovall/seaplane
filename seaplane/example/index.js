'use strict';

const express = require('express');
const path = require('path');

const app = express();

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname + '/index.html'));
});

app.listen(8080, '0.0.0.0', () => console.log('Server started on 0.0.0.0:8000.'));
