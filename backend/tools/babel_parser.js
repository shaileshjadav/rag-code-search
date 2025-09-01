const parser = require('@babel/parser');
const t = require('@babel/types');
const fs = require('fs');
const path = require('path');

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
    
    console.log(JSON.stringify(ast));

    const results = [];
    const fileName = path.basename(filePath);

    // t.traverseFast(ast, {
    //     FunctionDeclaration(node) {
    //         results.push({
    //             file_path: filePath,
    //             file_name: fileName,
    //             struct_name: "function",
    //             snippet: code.substring(node.start, node.end)
    //         });
    //     },
    //     ClassDeclaration(node) {
    //         results.push({
    //             file_path: filePath,
    //             file_name: fileName,
    //             struct_name: "class",
    //             snippet: code.substring(node.start, node.end)
    //         });
    //     }
    //     // You can add more node types like VariableDeclaration, etc.
    // });

    // console.log((results, null, 2));

} catch (e) {
    console.error(`Error parsing file ${filePath}: ${e.message}`);
    process.exit(1);
}