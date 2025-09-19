const parser = require("@babel/parser");
const t = require("@babel/types");
const fs = require("fs");
const path = require("path");
const traverse = require("@babel/traverse").default;

const filePath = process.argv[2];
if (!filePath) {
  console.error("Error: No file path provided.");
  process.exit(1);
}

const code = fs.readFileSync(filePath, "utf8");

try {
  const ast = parser.parse(code, {
    sourceType: "module",
    plugins: ["jsx", "typescript", "classProperties"], // Add plugins as needed
  });
  // console.log("File parsed successfully", JSON.stringify(ast));

  // Enums to match Rust structure
  const CodeType = {
    Function: "Function",
    Class:'Class',
    Variable:"Variable",
    // Struct: 'Struct',
    // Enum: 'Enum',
    // Impl: 'Impl'
  };

  // Context structure
function createContext(filePath, fileName, moduleName = null, structName = null, snippet = null) {
  // remove ./backend/{foldername}/...
  const normalizedFilePath = filePath.split("/").slice(3).join("/");
  return {
    module: moduleName,
    file_path: normalizedFilePath,
    file_name: fileName,
    struct_name: structName,
    snippet: snippet
  };
}

// Add snippet to context
function addSnippet(context, lines, lineFrom, lineTo) {
  let snippet = '';
  for (let i = lineFrom - 1; i < lineTo && i < lines.length; i++) {
    snippet += lines[i] + '\n';
  }
  context.snippet = snippet;
  return context;
}

function createTCode(name, signature, codeType, docstring, line, lineFrom, lineTo, context) {
  return {
    name: name,
    signature: signature,
    code_type: codeType,
    docstring: docstring,
    line: line,
    line_from: lineFrom,
    line_to: lineTo,
    context: context
  };
}


// Extract docstring from comments
function extractDocstring(node) {
  if (!node || !node.leadingComments) return null;
  
  // Look for JSDoc comments
  const jsDocComment = node.leadingComments.find(comment => 
    comment.type === 'CommentBlock' && comment.value.trim().startsWith('*')
  );
  
  if (jsDocComment) {
    return jsDocComment.value.trim();
  }
  
  // Fallback to last comment before the function
  const lastComment = node.leadingComments[node.leadingComments.length - 1];
  return lastComment ? lastComment.value.trim() : null;
}

// Generate function signature
function generateSignature(node, functionName) {
  try {
    if (!node) return `${functionName}()`;
    
    // Build parameter list
    const params = (node.params || []).map(param => {
      if (t.isIdentifier(param)) {
        return param.name;
      } else if (t.isAssignmentPattern(param) && t.isIdentifier(param.left)) {
        const defaultVal = generate(param.right).code;
        return `${param.left.name} = ${defaultVal}`;
      } else if (t.isRestElement(param) && t.isIdentifier(param.argument)) {
        return `...${param.argument.name}`;
      } else {
        try {
          return generate(param).code;
        } catch {
          return 'param';
        }
      }
    });
    
    // Build signature
    let signature = '';
    if (node.async) signature += 'async ';
    if (node.generator) signature += 'function* ';
    else if (t.isFunctionDeclaration(node) || t.isFunctionExpression(node)) {
      signature += 'function ';
    }
    
    signature += functionName;
    signature += `(${params.join(', ')})`;
    
    return signature;
  } catch (error) {
    console.warn(`Error generating signature for ${functionName}:`, error.message);
    return `${functionName}()`;
  }
}



// Main function to parse a function node
function parseFunction(node, path, context, lines) {
  try {
    if (!node) return null;
    
    const functionName = extractFunctionName(node, path);
    const signature = generateSignature(node, functionName);
    const docstring = extractDocstring(node);
    
    // Get line numbers
    const line = node.loc ? node.loc.start.line : 1;
    const lineFrom = node.loc ? node.loc.start.line : 1;
    const lineTo = node.loc ? node.loc.end.line : 1;
    
    // Create context with snippet
    let functionContext = { ...context };
    
    // Add struct_name for class methods
    if (path && path.parent && t.isClassMethod(path.parent)) {
      const classPath = path.findParent(p => t.isClassDeclaration(p.node));
      if (classPath && classPath.node.id) {
        functionContext.struct_name = classPath.node.id.name;
      }
    }
    
    functionContext = addSnippet(functionContext, lines, lineFrom, lineTo);
    
    return createTCode(
      functionName,
      signature,
      CodeType.Function,
      docstring,
      line,
      lineFrom,
      lineTo,
      functionContext
    );
  } catch (error) {
    console.error('Error parsing function:', error.message);
    return null;
  }
}


// Main function to parse a Class
function parseClass(node, path, context, lines) {
  try {
    if (!node) return null;
    
    const functionName = extractFunctionName(node, path);
    const signature = generateSignature(node, functionName);
    const docstring = extractDocstring(node);
    
    // Get line numbers
    const line = node.loc ? node.loc.start.line : 1;
    const lineFrom = node.loc ? node.loc.start.line : 1;
    const lineTo = node.loc ? node.loc.end.line : 1;
    
    // Create context with snippet
    let functionContext = { ...context };
    
    // Add struct_name for class methods
    if (path && path.parent && t.isClassMethod(path.parent)) {
      const classPath = path.findParent(p => t.isClassDeclaration(p.node));
      if (classPath && classPath.node.id) {
        functionContext.struct_name = classPath.node.id.name;
      }
    }
    
    functionContext = addSnippet(functionContext, lines, lineFrom, lineTo);
    
    return createTCode(
      functionName,
      signature,
      CodeType.Class,
      docstring,
      line,
      lineFrom,
      lineTo,
      functionContext
    );
  } catch (error) {
    console.error('Error parsing function:', error.message);
    return null;
  }
}

function parseVariable(node, path, context, lines) {
  try {
    if (!node) return null;
    
    const functionName = extractFunctionName(node, path);
    const signature = generateSignature(node, functionName);
    const docstring = extractDocstring(node);
    
    // Get line numbers
    const line = node.loc ? node.loc.start.line : 1;
    const lineFrom = node.loc ? node.loc.start.line : 1;
    const lineTo = node.loc ? node.loc.end.line : 1;
    
    // Create context with snippet
    let functionContext = { ...context };
    
    // Add struct_name for class methods
    if (path && path.parent && t.isClassMethod(path.parent)) {
      const classPath = path.findParent(p => t.isClassDeclaration(p.node));
      if (classPath && classPath.node.id) {
        functionContext.struct_name = classPath.node.id.name;
      }
    }
    
    functionContext = addSnippet(functionContext, lines, lineFrom, lineTo);
    
    return createTCode(
      functionName,
      signature,
      CodeType.Variable,
      docstring,
      line,
      lineFrom,
      lineTo,
      functionContext
    );
  } catch (error) {
    console.error('Error parsing function:', error.message);
    return null;
  }
}

// Extract function name with various fallback strategies
function extractFunctionName(node, path) {
  try {
    // Direct function name
    if (node.id && node.id.name) {
      return node.id.name;
    }
    
    // Check parent contexts using path (safer than node.parent)
    if (path && path.parent) {
      const parent = path.parent;
      
      // Variable assignment: const fn = function() {}
      if (t.isVariableDeclarator(parent) && parent.id && t.isIdentifier(parent.id)) {
        return parent.id.name;
      }
      
      // Object property: { methodName: function() {} }
      if (t.isProperty(parent) && parent.key) {
        return t.isIdentifier(parent.key) ? parent.key.name : parent.key.value;
      }
      
      // Class method
      if (t.isClassMethod(parent) && parent.key) {
        return t.isIdentifier(parent.key) ? parent.key.name : parent.key.value;
      }
      
      // Object method: { methodName() {} }
      if (t.isObjectMethod(parent) && parent.key) {
        return t.isIdentifier(parent.key) ? parent.key.name : parent.key.value;
      }
      
      // Assignment expression: obj.method = function() {}
      if (t.isAssignmentExpression(parent) && t.isMemberExpression(parent.left)) {
        return parent.left.property.name;
      }
    }
    
    return 'anonymous';
  } catch (error) {
    console.warn('Error extracting function name:', error.message);
    return 'anonymous';
  }
}

  const results = [];
  const fileName = path.basename(filePath);
  const context = createContext(filePath, fileName, fileName.split('.')[0]);

  const lines = code.split('\n');

  traverse(ast, {
    FunctionDeclaration(p) {
      // console.log("FunctionDeclaration", JSON.stringify(p.node));
      const signature = parseFunction(p.node, path, context, lines);

      // console.log(signature);
      results.push(signature);
      // results.push({
      //   name: id.name,
      //   signature:
      //   module: fileName.split('.')[0],
      //   file_path: filePath,
      //   file_name: fileName,
      //   struct_name: 'function',
      //   snippet: code.substring(p.node.start, p.node.end),
      // });
    },
    ClassDeclaration(p) {
      const signature = parseClass(p.node, path, context, lines);

      // console.log(signature);
      results.push(signature);
      // results.push({
      //   module: fileName.split(".")[0],
      //   file_path: filePath,
      //   file_name: fileName,
      //   struct_name: "class",
      //   snippet: code.substring(p.node.start, p.node.end),
      // });
    },
    VariableDeclarator(p) {
      const signature = parseVariable(p.node, path, context, lines);

      results.push(signature);
      // results.push({
      //   module: fileName.split(".")[0],
      //   file_path: filePath,
      //   file_name: fileName,
      //   struct_name: "class",
      //   snippet: code.substring(p.node.start, p.node.end),
      // });
    },
  });
  if (results.length > 0) {
    console.log(JSON.stringify(results));
  }
} catch (e) {
  console.error(`Error parsing file ${filePath}: ${e.message}`);
  process.exit(1);
}
