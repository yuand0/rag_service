from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path


class DocumentLoaderService:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", "。", "！", "？", " ", ""]
        )

    def load_file(self, file_path: str):
        path = Path(file_path)
        ext = path.suffix.lower()

        if ext == ".pdf":
            loader = PyPDFLoader(file_path)
        elif ext in (".txt", ".md", ".markdown"):
            loader = TextLoader(file_path, encoding="utf-8")
        else:
            raise ValueError(f"不支持的文件类型: {ext}")

        docs = loader.load()
        chunks = self.splitter.split_documents(docs)
        return chunks

    def load_directory(self, dir_path: str):
        all_chunks = []
        for file_path in Path(dir_path).rglob("*"):
            if file_path.suffix.lower() in (".pdf", ".txt", ".md", ".markdown"):
                try:
                    chunks = self.load_file(str(file_path))
                    all_chunks.extend(chunks)
                    print(f"✅ {file_path.name}: {len(chunks)} 个分块")
                except Exception as e:
                    print(f"❌ {file_path.name}: {e}")
        return all_chunks


loader_service = DocumentLoaderService()
