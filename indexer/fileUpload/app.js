const express = require('express');
console.log("test");

/**
 * Adds two numbers together.
 * @param {number} a The first number.
 * @param {number} b The second number.
 * @returns {number} The sum of the two numbers.
 **/
const app = express();

app.listen(3000, () => {
  console.log('Server is running on http://localhost:3000');
});