import glob
from typing import Dict, List


from src.knowledge import store_document


def load_files() -> List[Dict[str, str]]:
    """Load the sample documents from the data directory."""
    file_paths = glob.glob("data/sample-docs/*")

    documents = []
    # Create a document for each file
    for f_path in file_paths:
        name = f_path.split("/")[-1]  # Get the file name

        # Read the context of the file into a Document object
        with open(f_path, "r", encoding="utf-8") as f:
            text = f.read()
        partition_name = f"physics:{name}"
        documents.append({"text": text, "partition_name": partition_name})

    return documents


def main():
    """Main function.

    Currently we are showing an example of how to load documents into the knowledge base.
    """
    # Load the sample documents
    documents = load_files()

    for doc in documents:
        store_document(doc["text"], doc["partition_name"])


if __name__ == "__main__":
    main()
