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

## License

[Add your license information here]