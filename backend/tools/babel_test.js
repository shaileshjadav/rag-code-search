var babel = require("@babel/core");

const code = `
function greet(name) {
    console.log('Hello, world!');
}
`;

const options = {
    // presets: ['@babel/preset-env'],
};

const result = babel.transformFileSync('babel_parser.js');
console.log(result);