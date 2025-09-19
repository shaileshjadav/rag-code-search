// backend/tools/babel_parser_test.js
const parser = require('@babel/parser');
const fs = require('fs');
const path = require('path');
const traverse = require('@babel/traverse').default;

const filePath = process.argv[2];
if (!filePath) {
  console.error("Error: No file path provided.");
  process.exit(1);
}

const code = fs.readFileSync(filePath, 'utf8');

// Parse to AST (File/Program)
const ast = parser.parse(code, {
  sourceType: 'module',
  plugins: ['jsx', 'typescript', 'classProperties']
});

const results = [];
const fileName = path.basename(filePath);

traverse(ast, {
  FunctionDeclaration(p) {
    results.push({
      file_path: filePath,
      file_name: fileName,
      struct_name: 'function',
      snippet: code.substring(p.node.start, p.node.end),
    });
  },
  ClassDeclaration(p) {
    results.push({
      file_path: filePath,
      file_name: fileName,
      struct_name: 'class',
      snippet: code.substring(p.node.start, p.node.end),
    });
  },
});

console.log(results);