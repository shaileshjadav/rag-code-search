import os.path
from pathlib import Path
import json
from urllib.parse import urlparse

# Ensure the data directory exists
DATA_DIR = Path("./fileUpload")
if not DATA_DIR.exists():
    os.makedirs(DATA_DIR)

# This is the correct LSIF file path based on your previous examples.
LSIF_INDEX = Path(DATA_DIR) / "dump.lsif"

def convert(DATA_DIR):
    """
    Parses an LSIF dump file and extracts code snippets for definitions and references.
    """
    root_dir = None
    all_vertices = {}
    definitions, references, documents = dict(), dict(), dict()

    try:
        with open(LSIF_INDEX, "r") as fp:
            for row in fp:
                row_dict = json.loads(row)
                vertex_id = row_dict["id"]
                all_vertices[vertex_id] = row_dict
                
                if row_dict["type"] == "vertex":
                    if row_dict["label"] == "metaData":
                        root_dir = Path(os.path.normpath(row_dict["projectRoot"].replace("file://", "")))
                    if row_dict["label"] == "document":
                        documents[vertex_id] = row_dict
                
                if row_dict["type"] == "edge" and row_dict["label"] == "item":
                    document_id = row_dict.get("document")
                    if document_id:
                        for inV in row_dict.get("inVs", []):
                            prop = row_dict.get("property")
                            if prop == "definitions":
                                definitions[inV] = document_id
                            elif prop == "references":
                                references[inV] = document_id
                            else:
                                definitions[inV] = document_id
    except FileNotFoundError:
        print(f"Error: LSIF file not found at {LSIF_INDEX}")
        return []

    entries = []
    all_ranges = {**definitions, **references}
    
    for range_id, document_id in all_ranges.items():
        try:
            document = documents[document_id]
            range_data = all_vertices[range_id]
            
            doc_path = Path(urlparse(document["uri"]).path)

            # --- THE FIX IS HERE ---
            # Attempt to make the path relative, and if it fails, skip the entry
            try:
                rel_path = doc_path.relative_to(Path(root_dir).absolute())
            except ValueError:
                # This file is outside the project root; skip it.
                continue

            doc_lines = doc_path.read_text().split("\n")
            
            full_range = range_data.get("tag", {}).get("fullRange", range_data)
            start_line, end_line = full_range["start"]["line"], full_range["end"]["line"]
            
            code_snippet = "\n".join(doc_lines[start_line : end_line + 1])
            
            entries.append(
                {
                    "file": str(rel_path),
                    "start_line": start_line,
                    "end_line": end_line,
                    "code_snippet": code_snippet,
                    "type": "definition" if range_id in definitions else "reference",
                    "text": range_data.get("tag", {}).get("text")
                }
            )
        except (KeyError, FileNotFoundError) as e:
            print(f"Skipping entry for range {range_id} due to error: {e}")
            continue
            
    return entries

def main(DATA_DIR):
    files_data = convert(DATA_DIR)
    
    output_path = Path(DATA_DIR) / "qdrant_snippets.jsonl"
    with open(output_path, "w") as fp:
        for entry in files_data:
            fp.write(json.dumps(entry) + "\n")
            
    print(f"Successfully processed {len(files_data)} entries and saved to {output_path}")

if __name__ == '__main__':
    main(DATA_DIR)