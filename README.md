# SimNotes - CLI Tool for Similar Note Retrieval

SimNotes is a command-line interface (CLI) tool written in Python that allows users to find similar notes within their notes
collection. The tool utilizes sentence embeddings with sbert to compare a given query against a corpus of user notes.

## Features

- Embedding: Utilizes sbert to generate vector embeddings for notes.
- Similarity Search: Finds notes similar to a given query based on embeddings.
- Configurable: Allows users to configure directories, file extensions, and exclusion criteria.

## Installation

1. Let's first install pytorch library separately

Visit [Pytorch Download](https://pytorch.org/get-started/locally/) and choose your requirements and download the library
globally

If you want pytorch cpu version then go ahead with,

```bash
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

1. Clone the repository:

```bash
git clone https://github.com/your-username/simnotes.git
cd simnotes
```
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the CLI tool:

```bash
python simnotes.py "Your Query Text"
```

## Usage

Command-Line Arguments

- Query via Arguments:

```bash
python simnotes.py "Your Query Text"
```

- Query via Standard Input:

```bash
cat your_note.md | python simnotes.py
```

## Configuration

SimNotes uses a configuration file (config.txt) to set preferences. Make sure to configure the tool before usage.

### Configuration Directory

- Linux:

```plaintext
~/.config/simnotesconfig/
```

- macOS:

```plaintext
~/.simnotesconfig/
```

- Windows:

For Windows, use AppData\Roaming for per-user configuration:

```plaintext
AppData\Roaming\Simnotes\
```

or else can put config.txt at home directiory

```plaintext
~/.simnotesconfig/
```

### Configuration File (config.txt)

Create a config.txt file in the configuration directory. Below is an example configuration:

```plaintext
notes_dir = /path/to/your/notes
exclude_dir = directory1,directory2
exclude_file = file1,file2
note_extension = .md
```

Configuration Parameters:

- notes_dir: Path to the directory containing your notes.

- exclude_dir: Comma-separated directories to exclude from the search. Paths should be relative to notes_dir.

- exclude_file: Comma-separated files to exclude from the search. Paths should be relative to notes_dir.

- note_extension: The extension of your note files (e.g., .md).

## License

This project is licensed under the MIT License.

## Contributing

Feel free to contribute to SimNotes by creating issues or submitting pull requests.

## Acknowledgments

[Sentence-BERT](https://www.sbert.net/index.html) for sentence embeddings.

## Future:

- I feel like simple dot product hits are enough to find similar notes but in future if there is need to 
improve results then consider this roop
https://www.sbert.net/examples/applications/retrieve_rerank/README.html
https://youtu.be/zMDBc_Q9Ark?feature=shared

- If it is taking more memory, then we can quantise the vectors into int8
https://www.sbert.net/examples/training/distillation/README.html#quantization
