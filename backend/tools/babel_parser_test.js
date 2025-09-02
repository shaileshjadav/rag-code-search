const parser = require('@babel/parser');
const t = require('@babel/types');
const fs = require('fs');
const path = require('path');
const babel = require("@babel/core");
const traverse = require('@babel/traverse').default;

const filePath = process.argv[2];
if (!filePath) {
    console.error("Error: No file path provided.");
    process.exit(1);
}

const code = fs.readFileSync(filePath, 'utf8');

try {
    const ast = babel.transformFileSync(filePath);
    console.log(ast)
    const results = [];
    const fileName = path.basename(filePath);

    traverse(ast, {
        FunctionDeclaration(path) {
            results.push({
                file_path: filePath,
                file_name: fileName,
                struct_name: "function",
                snippet: code.substring(path.node.start, path.node.end)
            });
        },
        ClassDeclaration(path) {
            results.push({
                file_path: filePath,
                file_name: fileName,
                struct_name: "class",
                snippet: code.substring(path.node.start, path.node.end)
            });
        }
        // You can add more node types like VariableDeclaration, etc.
    });

    console.log(results);

} catch (e) {
    console.error(`Error parsing file ${filePath}: ${e.message}`);
    process.exit(1);
}
