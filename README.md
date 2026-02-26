# Repository Search

A code search and indexing tool that uses LSIF (Language Server Index Format) and embeddings to enable semantic search across code repositories.

## Features

- **Code Indexing**: Generate LSIF indexes for TypeScript/JavaScript projects
- **Semantic Search**: Search code using natural language queries
- **Vector Embeddings**: Uses sentence transformers for code similarity search
- **Qdrant Integration**: Stores embeddings and metadata in Qdrant vector database

## Prerequisites

- Python 3.8+
- Node.js (for LSIF generation)
- Qdrant server running (default: http://localhost:6333)

## Demo
<video src="./demo.mp4" width="100%" controls controlsList="nodownload"></video>

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd repo-search
```

2. Install Python dependencies:
```bash
pip install -r backend/requirements.txt
```

3. Install Node.js dependencies for LSIF generation:
```bash
npm install -g lsif-tsc
```

4. Start HTTP server:
```bash
python3 -m  backend.app
```

## Usage

### Index a Repository

To index a code repository for search:

```bash
python -m backend.cli index --repo=./backend/fileUpload
```

This command will:
- Generate LSIF index for the repository
- Convert LSIF data to searchable format
- Create embeddings for code snippets
- Store everything in the Qdrant database

### Search Code

To search for code using natural language queries:

```bash
python -m backend.cli search --query="your search query here"
```

Example queries:
- "Router.handle method, where is it defined?"
- "authentication middleware"
- "database connection setup"

## Project Structure

```
repo-search/
├── backend/
│   ├── cli.py                 # Main CLI interface
│   ├── config.py              # Configuration settings
│   ├── data/                  # Generated data files
│   ├── fileUpload/            # Sample code repository
│   ├── helper/                # Utility modules
│   │   ├── embeddings.py      # Embedding generation
│   │   ├── upload_code.py     # Code upload to Qdrant
│   │   └── upload_signatures.py
│   ├── index/                 # Indexing modules
│   │   ├── files_to_json.py   # File processing
│   │   ├── generate_lsif_index.py
│   │   ├── convert_lsif_index.py
│   │   └── generate_signatures.py
│   ├── search/                # Search functionality
│   │   ├── search.py          # Search interface
│   │   └── searcher.py        # Search implementation
│   └── tools/                 # External tools
└── README.md
```

## Configuration

Edit `backend/config.py` to configure:

- **Qdrant Settings**: URL, API key, collection names
- **Embedding Model**: Sentence transformer model name
- **Data Directories**: Paths for data storage

## Environment Variables

Create a `.env` file in the project root:

```env
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your_api_key_here
```

## Working

#### Indexing

**Step 1:** Create a JSON array of objects where each object contains 4 attributes:
1. `path` - File path
2. `code` - Array of code lines
3. `startLine` - Starting line number
4. `endLine` - Ending line number


**Step 2:** Generate LSIF (Language Server Index Format) for the project, which creates a `dump.lsif` file.

> **LSIF** is a standard JSON-based format developed by Microsoft for indexing codebases to provide fast, precise code intelligence (definitions, references, hovers) without needing a running language server. It acts as a serialized dump of a language server's knowledge, allowing IDEs or web interfaces to quickly display code intelligence features like "go to definition".

References:
- [LSIF Specification](https://lsif.dev/)
- [Writing an LSIF Indexer](https://sourcegraph.com/blog/writing-an-lsif-indexer)
- [Language Server Index Format Overview](https://microsoft.github.io/language-server-protocol/overviews/lsif/overview/)

**Step 3:** Parse the LSIF dump file and extract code snippets from range vertices, including character positions for precise code location.

**Step 4:** Run the Babel parser on JavaScript files and generate a list of dictionaries containing:
- Code snippets
- Context information
- Signature types

The Babel parser parses the AST (Abstract Syntax Tree) of the code and creates JSON signatures.

**Step 5:** Create vector embeddings from the parsed LSIF dump file and save them in the Qdrant database.

**Step 6:** Create vector embeddings from AST-parsed data (Babel-parsed JSON) and save them in the database.

#### Indexing Flow

1. Create JSON dump for each file and code snippet
2. Generate LSIF index for the repository using `lsif-tsc`
3. Convert LSIF to JSON format (`qdrant_snippets`)
4. Generate signatures using Babel parser for each file (`signatures.json`)
5. Upload `qdrant_snippets` and `signatures.json` to the vector store (e.g., Qdrant)
6. Create two collections of embeddings:
   - **`{repo}_code`**: Stores code snippets as vector embeddings for code-based search
   - **`{repo}_signatures`**: Stores AST-generated signatures (converted to natural language embeddings) for semantic search

#### Searching

- **Code Collection Search**: Query against code snippets
- **Signatures Collection Search**: Query against natural language representations
- **Result Merging**: Merge overlapping code search results with NLU (Natural Language Understanding) search results for enhanced relevance

## Development

### Running Individual Modules

You can also run individual modules directly:

```bash
# Generate LSIF index
python -m backend.index.generate_lsif_index

# Convert LSIF to searchable format
python -m backend.index.convert_lsif_index

# Upload code embeddings
python -m backend.helper.upload_code

# Test search functionality
python -m backend.search.searcher
```

### Adding New Languages

To support additional programming languages:

1. Add language server configuration in `backend/index/generate_lsif_index.py`
2. Update the `LANGUAGE_SERVERS` dictionary
3. Install the corresponding language server

## Troubleshooting

### Common Issues

1. **Module not found errors**: Ensure you're running commands from the project root directory
2. **Qdrant connection errors**: Verify Qdrant server is running and accessible
3. **LSIF generation fails**: Check that Node.js and lsif-tsc are properly installed

### Debug Mode

For verbose output, you can modify the logging level in the configuration files.

