import json
from pathlib import Path

# Read the LSIF file and debug
LSIF_INDEX = Path("data/dump.lsif")

root_dir = None
all_vertices = {}
documents = dict()

print("Reading LSIF file...")
with open(LSIF_INDEX, "r") as fp:
    for row in fp:
        row_dict = json.loads(row)
        vertex_id = row_dict["id"]
        all_vertices[vertex_id] = row_dict
        
        if row_dict["type"] == "vertex" and row_dict["label"] == "metaData":
            root_dir = row_dict["projectRoot"].replace("file://", "")
            print(f"Root dir: {root_dir}")

        if row_dict["type"] == "vertex" and row_dict["label"] == "document":
            documents[vertex_id] = row_dict
            print(f"Document {vertex_id}: {row_dict['uri']}")

print(f"Found {len(documents)} documents")
print(f"Found {len(all_vertices)} total vertices")

# Count range vertices
range_count = 0
for vertex_id, vertex_data in all_vertices.items():
    if vertex_data.get("type") == "vertex" and vertex_data.get("label") == "range":
        range_count += 1
        if range_count <= 3:  # Show first 3 ranges
            print(f"Range {vertex_id}: {vertex_data}")

print(f"Found {range_count} range vertices")

# Count edges
edge_count = 0
for vertex_id, vertex_data in all_vertices.items():
    if vertex_data.get("type") == "edge":
        edge_count += 1
        if edge_count <= 3:  # Show first 3 edges
            print(f"Edge {vertex_id}: {vertex_data}")

print(f"Found {edge_count} edges")