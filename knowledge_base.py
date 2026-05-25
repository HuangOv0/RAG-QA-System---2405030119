import os
import glob
from PyPDF2 import PdfReader
from docx import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import TextLoader

class KnowledgeBase:
    def __init__(self, persist_directory="./chroma_db"):
        self.persist_directory = persist_directory
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        self.vector_store = None

    def load_document(self, file_path):
        text = ""
        try:
            if file_path.endswith(".pdf"):
                reader = PdfReader(file_path)
                for page in reader.pages:
                    text += page.extract_text() or ""
            elif file_path.endswith(".docx"):
                doc = Document(file_path)
                for para in doc.paragraphs:
                    text += para.text + "\n"
            elif file_path.endswith(".txt"):
                loader = TextLoader(file_path, encoding='utf-8')
                docs = loader.load()
                text = docs[0].page_content if docs else ""
            else:
                print(f"不支持的文件格式: {file_path}")
                return None
        except Exception as e:
            print(f"加载文件 {file_path} 时出错: {e}")
            return None
        
        return text if text.strip() else None

    def load_documents_from_folder(self, folder_path):
        documents = []
        supported_extensions = ["*.pdf", "*.docx", "*.txt"]
        
        for ext in supported_extensions:
            files = glob.glob(os.path.join(folder_path, ext))
            for file in files:
                print(f"正在加载文件: {file}")
                text = self.load_document(file)
                if text:
                    documents.append({"file": os.path.basename(file), "content": text})
        
        return documents

    def build_vector_store(self, documents):
        all_chunks = []
        for doc in documents:
            chunks = self.text_splitter.split_text(doc["content"])
            for i, chunk in enumerate(chunks):
                metadata = {
                    "source": doc["file"],
                    "chunk_index": i
                }
                all_chunks.append({"content": chunk, "metadata": metadata})
        
        if not all_chunks:
            print("没有可处理的文档内容")
            return False
        
        texts = [chunk["content"] for chunk in all_chunks]
        metadatas = [chunk["metadata"] for chunk in all_chunks]
        
        self.vector_store = Chroma.from_texts(
            texts=texts,
            embedding=self.embeddings,
            metadatas=metadatas,
            persist_directory=self.persist_directory
        )
        print(f"向量数据库构建完成，共 {len(all_chunks)} 个文本块")
        return True

    def load_vector_store(self):
        if os.path.exists(self.persist_directory):
            self.vector_store = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
            print("向量数据库加载成功")
            return True
        return False

    def search(self, query, k=3):
        if not self.vector_store:
            print("向量数据库未加载")
            return []
        
        results = self.vector_store.similarity_search(query, k=k)
        return results

    def get_doc_count(self):
        if not self.vector_store:
            return 0
        return len(self.vector_store.get()['ids'])

if __name__ == "__main__":
    kb = KnowledgeBase()
    
    documents = kb.load_documents_from_folder("./docs")
    if documents:
        kb.build_vector_store(documents)
    
    kb.load_vector_store()
    
    test_query = "什么是Transformer?"
    results = kb.search(test_query)
    print(f"\n检索结果 ({len(results)}):")
    for i, result in enumerate(results):
        print(f"\n结果 {i+1}:")
        print(f"来源: {result.metadata.get('source', '未知')}")
        print(f"内容: {result.page_content[:200]}...")