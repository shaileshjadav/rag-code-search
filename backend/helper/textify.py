import re


def split_camel_case(text):
    """Split camel case text into words.

    Args:
        text (str): A camel case text.
            Example: "StorageError"

    Returns:
        str: A text with spaces between words.
            Example: "Storage Error"
    """
    return re.sub(r"([a-z])([A-Z])", r"\1 \2", text)


def split_snake_case(text):
    """Split snake case text into words.

    Args:
        text (str): A snake case text.
            Example: "storage_error"

    Returns:
        str: A text with spaces between words.
            Example: "storage error"
    """
    return re.sub(r"([a-z])_([a-z])", r"\1 \2", text)


def check_special_tokens(text):
    """Check if a text consists of special tokens.

    Args:
        text (str): A text.
            Example: "fn"

    Returns:
        bool: True if the text consists of special tokens, False otherwise.
    """
    return re.match(r"^\W+$", text) is not None


def tokenize(text):
    """Tokenize a text by words borders.

    Args:
        text (str): A text.
            Example: "(& mut self , alias : & str)"

    Returns:
        list: A list of tokens.
            Example: ["(", "&", "mut", "self", ",", "alias", ":", "&", "str", ")"]
    """
    tokens = re.split(r"(\W)", text)
    tokens = [token for token in tokens if token != ""]
    return tokens


def clear_signature(signature):
    """Remove special symbols from a function signature.

    Args:
        signature (str): A function signature.
            Example: "fn remove (& mut self , alias : & str) -> Result < Option < String > , StorageError >"

    Returns:
        str: A function signature without special symbols. and proper tokenization.
            Example: "function remove alias str returns Result Option String Storage Error"

    >>> clear_signature("fn remove (& mut self , alias : & str) -> Result < Option < String > , StorageError >")
    'fn remove mut self alias str Result Option String Storage Error'
    """
    tokens = tokenize(signature)
    tokens = (token for token in tokens if not check_special_tokens(token))
    tokens = (token.strip() for token in tokens)
    tokens = (token for token in tokens if token != "")
    tokens = (split_snake_case(split_camel_case(token)) for token in tokens)
    sentence = " ".join(tokens)
    return sentence


def textify(structure):
    """Convert a piece of code structure into a text representation close to natural language.

    Args:
        structure (dict): A piece of code structure.
            Example:
            structure = {
                "name": "remove",
                "signature": "fn remove (& mut self , alias : & str) -> Result < Option < String > , StorageError >",
                "code_type": "Function",
                "docstring": null,
                "line": 75,
                "line_from": 75,
                "line_to": 79,
                "context": {
                    "module": "content_manager",
                    "file_path": "lib/storage/src/content_manager/alias_mapping.rs",
                    "file_name": "alias_mapping.rs",
                    "struct_name": "AliasPersistence",
                    "snippet": "    pub fn remove(&mut self, alias: &str) -> Result<Option<String>, StorageError> {\n        let res = self.alias_mapping.0.remove(alias);\n        self.alias_mapping.save(&self.data_path)?;\n        Ok(res)\n    }\n"
                }
            }

    Returns:
        str: A natural language representation of the code structure.
    """
    code_type = structure.get("code_type", "Code")
    docstring = ""
    if structure.get("docstring") is not None:
        docstring = "that does: " + structure["docstring"]

    context = ""
    if structure.get("context") is not None:
        context_struct = structure["context"]
        if context_struct.get("struct_name") is not None:
            context = f"""{context} in struct {context_struct["struct_name"]} """
        if context_struct.get("module") is not None:
            context = f"""{context} in module {context_struct["module"]} """
        if context_struct.get("file_name") is not None:
            context = f"""{context} in file {context_struct["file_name"]} """

    name = structure.get("name", "")
    signature = clear_signature(structure.get("signature", ""))
    text = f"""{code_type} {name} {docstring} defined as {signature} {context}"""
    return text.strip()


def textify_ast_node(ast_node, file_path=None):
    """Convert an AST node to a text representation.
    
    Args:
        ast_node (dict): AST node from babel parser
        file_path (str): Optional file path for context
        
    Returns:
        str: Natural language representation of the AST node
    """
    if not ast_node or not isinstance(ast_node, dict):
        return ""
    
    # Extract basic information
    node_type = ast_node.get("type", "Unknown")
    name = ""
    
    # Try to extract name based on node type
    if node_type == "FunctionDeclaration":
        name = ast_node.get("id", {}).get("name", "")
    elif node_type == "VariableDeclaration":
        declarations = ast_node.get("declarations", [])
        if declarations:
            name = declarations[0].get("id", {}).get("name", "")
    elif node_type == "ClassDeclaration":
        name = ast_node.get("id", {}).get("name", "")
    elif node_type == "MethodDefinition":
        name = ast_node.get("key", {}).get("name", "")
    
    # Create a more natural text representation
    if node_type == "FunctionDeclaration":
        text_parts = [f"function {name}"]
    elif node_type == "VariableDeclaration":
        text_parts = [f"variable {name}"]
    elif node_type == "ClassDeclaration":
        text_parts = [f"class {name}"]
    elif node_type == "MethodDefinition":
        text_parts = [f"method {name}"]
    else:
        text_parts = [node_type]
        if name:
            text_parts.append(name)
    
    # Add file context if available
    if file_path:
        file_name = file_path.split("/")[-1] if "/" in file_path else file_path
        text_parts.append(f"in file {file_name}")
    
    return " ".join(text_parts)

