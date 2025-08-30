import os.path
from pathlib import Path
import json
from urllib.parse import urlparse
from config import DATA_DIR

# if not DATA_DIR.exists():
#     os.makedirs(DATA_DIR)

# This is the correct LSIF file path based on your previous examples.
LSIF_INDEX = Path(DATA_DIR) / "dump.lsif"

def convert():
    """
    Parses an LSIF dump file and extracts code snippets for definitions and references,
    including associated hover text.
    """
    root_dir = None
    all_vertices = {}
    next_edges, hover_edges = {}, {}
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
                
                if row_dict["type"] == "edge":
                    if row_dict["label"] == "item":
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
                    
                    # Store all "next" edges to link ranges to resultSets
                    elif row_dict["label"] == "next":
                        next_edges[row_dict["inV"]] = row_dict["outV"]
                    
                    # Store all "textDocument/hover" edges to link resultSets to hover data
                    elif row_dict["label"] == "textDocument/hover":
                        hover_edges[row_dict["outV"]] = row_dict["inV"]
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
            try:
                rel_path = doc_path.relative_to(Path(root_dir).absolute())
            except ValueError:
                continue

            doc_lines = doc_path.read_text().split("\n")
            
            full_range = range_data.get("tag", {}).get("fullRange", range_data)
            start_line, end_line = full_range["start"]["line"], full_range["end"]["line"]
            
            code_snippet = "\n".join(doc_lines[start_line : end_line + 1])
            
            # --- NEW LOGIC TO GET HOVER TEXT ---
            hover_text = None
            # Find the resultSet linked to this range via the 'next' edge
            resultSet_id = next_edges.get(range_id)
            if resultSet_id:
                # Find the hoverResult linked to this resultSet
                hoverResult_id = hover_edges.get(resultSet_id)
                if hoverResult_id:
                    # Get the actual hover text from the all_vertices dictionary
                    hover_text_vertex = all_vertices.get(hoverResult_id)
                    if hover_text_vertex:
                        # Safely access the contents
                        contents = hover_text_vertex.get("result", {}).get("contents", [])
                        if contents:
                            hover_text = contents[0].get("value")
            
            entries.append(
                {
                    "file": str(rel_path),
                    "start_line": start_line,
                    "end_line": end_line,
                    "code_snippet": code_snippet,
                    "hover_text": hover_text, # Added this field
                    "type": "definition" if range_id in definitions else "reference",
                    "text": range_data.get("tag", {}).get("text")
                }
            )
        except (KeyError, FileNotFoundError) as e:
            print(f"Skipping entry for range {range_id} due to error: {e}")
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