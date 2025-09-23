import os.path
from pathlib import Path
import json
from urllib.parse import urlparse
from backend.config import DATA_DIR

# if not DATA_DIR.exists():
#     os.makedirs(DATA_DIR)

# This is the correct LSIF file path based on your previous examples.
LSIF_INDEX = Path(DATA_DIR) / "dump.lsif"

def convert():
    """
    Parses an LSIF dump file and extracts code snippets from range vertices,
    including character positions for precise code location.
    """
    root_dir = None
    all_vertices = {}
    documents = dict()

    try:
        with open(LSIF_INDEX, "r") as fp:
            for row in fp:
                row_dict = json.loads(row)
                vertex_id = row_dict["id"]
                all_vertices[vertex_id] = row_dict
                
                if row_dict["type"] == "vertex" and row_dict["label"] == "metaData":
                    root_dir = Path(os.path.normpath(row_dict["projectRoot"].replace("file://", "")))

                if row_dict["type"] == "vertex" and row_dict["label"] == "document":
                    documents[vertex_id] = row_dict
    except FileNotFoundError:
        print(f"Error: LSIF file not found at {LSIF_INDEX}")
        return []

    entries = []
    
    # Process all range vertices - use the first document for now (simplified approach)
    if not documents:
        print("No documents found in LSIF file")
        return []
    
    # Get the first document (our source file)
    document_id = list(documents.keys())[0]
    document = documents[document_id]
    doc_path = Path(urlparse(document["uri"]).path)
    
    try:
        rel_path = doc_path.relative_to(Path(root_dir).absolute())
    except ValueError:
        print(f"Could not make path relative: {doc_path} vs {root_dir}")
        return []
    
    # Read the document content
    try:
        doc_lines = doc_path.read_text().split("\n")
    except FileNotFoundError:
        print(f"Document file not found: {doc_path}")
        return []
    
    # Process all range vertices
    for vertex_id, vertex_data in all_vertices.items():
        if vertex_data.get("type") == "vertex" and vertex_data.get("label") == "range":
            try:
                # Get the range data
                start_data = vertex_data.get("start", {})
                end_data = vertex_data.get("end", {})
                
                start_line = start_data.get("line", 0)
                start_character = start_data.get("character", 0)
                end_line = end_data.get("line", 0)
                end_character = end_data.get("character", 0)
                
                # Get the tag information
                tag = vertex_data.get("tag", {})
                range_type = tag.get("type", "unknown")
                text = tag.get("text", "")
                
                # Skip ranges that are too far out (likely from external libraries)
                if start_line >= len(doc_lines):
                    continue
                # Extract code snippet
                if start_line == end_line:
                    # Single line range
                    if start_line < len(doc_lines):
                        line = doc_lines[start_line]
                        code_snippet = line[start_character:end_character]
                    else:
                        code_snippet = ""
                else:
                    # Multi-line range
                    if start_line < len(doc_lines) and end_line < len(doc_lines):
                        lines = doc_lines[start_line:end_line + 1]
                        if lines:
                            lines[0] = lines[0][start_character:]
                            lines[-1] = lines[-1][:end_character]
                        code_snippet = "\n".join(lines)
                    else:
                        code_snippet = ""

                # Only include non-empty code snippets
                if code_snippet.strip():
                    entries.append(
                        {
                            "file": str(rel_path),
                            "start_line": start_line,
                            "start_character": start_character,
                            "end_line": end_line,
                            "end_character": end_character,
                            "code_snippet": code_snippet,
                        }
                    )
            except (KeyError, IndexError) as e:
                print(f"Skipping range {vertex_id} due to error: {e}")
                continue
            
    return entries

def main():
    files_data = convert()
    output_path = Path(DATA_DIR) / "qdrant_snippets.jsonl"
    with open(output_path, "w") as fp:
        for entry in files_data:
            fp.write(json.dumps(entry) + "\n")
            
    print(f"Successfully processed {len(files_data)} entries and saved to {output_path}")

if __name__ == '__main__':
    main()