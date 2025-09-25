import os.path
from pathlib import Path

import json
from urllib.parse import urlparse

from backend.config import DATA_DIR
from urllib.parse import urlparse, unquote

LSIF_INDEX = Path(DATA_DIR) / "dump.lsif"


def uri_to_path(uri: str) -> Path:
    # Works for file:/..., file:///, file://host/...
    p = urlparse(uri)
    if p.scheme == "file":
        path = unquote(p.path or "")
        print(f"path: {uri} ->> {Path(os.path.normpath(path))}")
        # On WSL we want /mnt/... unchanged; ensure it's absolute
        return Path(os.path.normpath(path))
    # Fallback: treat the input as a filesystem path
    return Path(os.path.normpath(uri))

def get_relative_path(abs_path: str, root_dir: Path) -> Path:
    print(f"abs_path: {abs_path}")
    print(f"root_dir: {root_dir}")
    # If inside WSL (/mnt/..), keep absolute
    if str(abs_path).startswith("/mnt/"):
        print(f"{abs_path.relative_to(root_dir)}")
        try:
            # Make it relative to root_dir if possible
            return abs_path.relative_to(root_dir)
        except ValueError:
            # Not under root_dir → just return absolute
            return abs_path
    else:
        return abs_path
    
def convert():
    """
    Parses an LSIF dump file and extracts code snippets from range vertices,
    including character positions for precise code location.
    """
    root_dir = None

    # Vertices
    documents = {}              # id -> {"uri": "...", ...}
    ranges = {}                 # id -> {"start": {...}, "end": {...}}
    result_sets = set()         # ids
    definition_results = set()  # ids

    # Edges (helpers)
    range_to_document = {}                 # range_id -> document_id
    rs_to_dr = {}                          # resultSet_id -> definitionResult_id
    dr_to_def_ranges = {}                  # definitionResult_id -> set(range_id)
    rs_to_ranges = {}                      # resultSet_id -> set(range_id)

    with open(LSIF_INDEX, "r", encoding="utf-8") as fp:
        for row in fp:
            row_dict = json.loads(row)
            t = row_dict.get("type")
            label = row_dict.get("label")
            vid = row_dict.get("id")

            # metaData: project root
            if t == "vertex" and label == "metaData":
                root_dir = Path(os.path.normpath(row_dict["projectRoot"].replace("file://", "")))

            # document vertices
            if t == "vertex" and label == "document":
                documents[vid] = row_dict

            # range vertices
            if t == "vertex" and label == "range":
                ranges[vid] = row_dict

            # resultSet vertices
            if t == "vertex" and label == "resultSet":
                result_sets.add(vid)

            # definitionResult vertices
            if t == "vertex" and label == "definitionResult":
                definition_results.add(vid)

            # contains edges: document -> ranges
            if t == "edge" and label == "contains":
                outV = row_dict.get("outV")
                inVs = row_dict.get("inVs", [])
                # Project->Document and Document->Range both use contains; we want Document->Range
                if outV in documents:
                    for r in inVs:
                        if r in ranges:
                            range_to_document[r] = outV

            # next edges: range -> resultSet (sometimes resultSet -> resultSet too)
            if t == "edge" and label == "next":
                outV = row_dict.get("outV")
                inV = row_dict.get("inV")
                # We only care about ranges that point to a resultSet
                if inV in result_sets and outV in ranges:
                    rs_to_ranges.setdefault(inV, set()).add(outV)

            # textDocument/definition: resultSet -> definitionResult
            if t == "edge" and label == "textDocument/definition":
                outV = row_dict.get("outV")  # resultSet
                inV = row_dict.get("inV")    # definitionResult
                if outV in result_sets and inV in definition_results:
                    rs_to_dr[outV] = inV

            # item edges: definitionResult -> definition range(s)
            if t == "edge" and label == "item":
                outV = row_dict.get("outV")     # definitionResult
                inVs = row_dict.get("inVs", []) # ranges
                if outV in definition_results:
                    s = dr_to_def_ranges.setdefault(outV, set())
                    for r in inVs:
                        if r in ranges:
                            s.add(r)
    # print(f"rs_to_dr: {rs_to_dr}")
    # print(f"dr_to_def_ranges: {dr_to_def_ranges}")
    # print(f"rs_to_ranges: {rs_to_ranges}")
    # print(f"range_to_document: {range_to_document}")
    # print(f"documents: {documents}")
    # print(f"ranges: {ranges}")
    # return
    # print(f"result_sets: {result_sets}")
    # print(f"definition_results: {definition_results}")
    # Build entries: one per definition resultSet, grouped with references
    entries = []
    for rs_id, dr_id in rs_to_dr.items():
        def_range_ids = dr_to_def_ranges.get(dr_id, set())
        all_rs_ranges = rs_to_ranges.get(rs_id, set())

        # Split into definition(s) and references
        ref_range_ids = [r for r in all_rs_ranges if r not in def_range_ids]

        # For each definition range, prepare an entry that includes all refs
        for def_rid in def_range_ids:
            doc_id = range_to_document.get(def_rid)
            if not doc_id or doc_id not in documents:
                continue

            doc_uri = documents[doc_id]["uri"]
            # abs_path = Path(str(doc_uri).replace("file:/mnt/e/", ""))
            # print(f"doc_uri: {doc_uri}")
            # rel_path = Path(abs_path).relative_to(Path(root_dir).absolute()) if root_dir else abs_path
            # rel_path = abs_path

            # load document text once
            text_path = uri_to_path(doc_uri)
            
            if not text_path.exists():
                # Skip if file is not available on disk
                continue
            doc_lines = text_path.read_text(encoding="utf-8", errors="ignore").split("\n")
            def_range = ranges[def_rid]
            
            ds = def_range["start"]
            de = def_range["end"]
            def_snippet = "\n".join(doc_lines[ds["line"] : de["line"] + 1])

            print(f"def_snippet: {def_snippet}, start: {ds}, end: {de}")
            
            refs = []
            for rrid in ref_range_ids:
                rdoc_id = range_to_document.get(rrid)
                if not rdoc_id or rdoc_id not in documents:
                    continue
                rdoc_uri = documents[rdoc_id]["uri"]
                rtext_path = uri_to_path(rdoc_uri)
                if not rtext_path.exists():
                    continue
                r_lines = rtext_path.read_text(encoding="utf-8", errors="ignore").split("\n")
                r = ranges[rrid]
                rs = r["start"]
                re_ = r["end"]
                # refs.append(
                #     {
                #         # "file": str(Path(str(rdoc_uri).replace("file://", "")).relative_to(Path(root_dir).absolute())) if root_dir else str(rtext_path),
                #         "file": str(rtext_path),
                #         "start_line": rs["line"],
                #         "start_character": rs["character"],
                #         "end_line": re_["line"],
                #         "end_character": re_["character"],
                #         "code_snippet": "\n".join(r_lines[rs["line"] : re_["line"] + 1]),
                #     }
                # )

            # entries.append(
            #     {
            #         "definition_result_set": rs_id,
            #         "definition_file": str(rel_path),
            #         "definition": {
            #             "start_line": ds["line"],
            #             "start_character": ds["character"],
            #             "end_line": de["line"],
            #             "end_character": de["character"],
            #             "code_snippet": def_snippet,
            #         },
            #         "references": refs,
            #     }
            # )

            entries.append(
                {
                        # "file": str(Path(str(rdoc_uri).replace("file://", "")).relative_to(Path(root_dir).absolute())) if root_dir else str(rtext_path),
                    "file": str(get_relative_path(rtext_path, root_dir.resolve())),
                    "start_line": rs["line"], 
                    "start_character": rs["character"],
                    "end_line": re_["line"],
                    "end_character": re_["character"],
                    "code_snippet": "\n".join(r_lines[rs["line"] : re_["line"] + 1]),
                }
            )
    print(f"Successfully processed {entries} entries")
    return entries
    

def main():
    files_data = convert()
    output_path = Path(DATA_DIR) / "qdrant_snippets.jsonl"
    with open(output_path, "w") as fp:
        for entry in files_data:
            fp.write(json.dumps(entry) + "\n")


if __name__ == '__main__':
    main()
        

