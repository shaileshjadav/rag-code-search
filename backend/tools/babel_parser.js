const parser = require('@babel/parser');
const t = require('@babel/types');
const fs = require('fs');
const path = require('path');
const traverse = require('@babel/traverse').default;

const filePath = process.argv[2];
if (!filePath) {
    console.error("Error: No file path provided.");
    process.exit(1);
}

const code = fs.readFileSync(filePath, 'utf8');

try {
    const ast = parser.parse(code, {
        sourceType: "module",
        plugins: ["jsx", "typescript", "classProperties"] // Add plugins as needed
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
    console.log(JSON.stringify(results));

} catch (e) {
    console.error(`Error parsing file ${filePath}: ${e.message}`);
    process.exit(1);
}