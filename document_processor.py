from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
import os

class DocumentProcessor:
    def __init__(self, persist_directory="./db"):
        self.persist_directory = persist_directory
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        self.vector_store = None

    def load_document(self, file_path):
        """加载单个文档并提取文本"""
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            loader = PyPDFLoader(file_path)
        elif ext == ".docx":
            loader = Docx2txtLoader(file_path)
        elif ext == ".txt":
            loader = TextLoader(file_path, encoding='utf-8')
        else:
            raise ValueError(f"不支持的文件格式: {ext}")

        return loader.load()

    def split_documents(self, documents):
        """将文档分割成文本块"""
        return self.text_splitter.split_documents(documents)

    def _embed_texts(self, texts):
        """手动嵌入文本"""
        return self.embeddings.embed_documents(texts)

    def create_vector_store(self, documents):
        """创建并保存向量数据库"""
        texts = self.split_documents(documents)
        text_contents = [t.page_content for t in texts]
        text_metadata = [{"source": t.metadata.get("source", "unknown")} for t in texts]

        embeddings = self._embed_texts(text_contents)

        client = Chroma(persist_directory=self.persist_directory)
        client.add_texts(texts=text_contents, embeddings=embeddings, metadatas=text_metadata)
        client.persist()

        self.vector_store = client
        return len(texts)

    def load_vector_store(self):
        """加载已保存的向量数据库"""
        if os.path.exists(self.persist_directory):
            try:
                self.vector_store = Chroma(persist_directory=self.persist_directory)
                return True
            except:
                return False
        return False

    def add_documents(self, new_documents):
        """向现有向量库添加新文档"""
        if self.vector_store is None:
            self.load_vector_store()

        if self.vector_store is None:
            return self.create_vector_store(new_documents)

        texts = self.split_documents(new_documents)
        text_contents = [t.page_content for t in texts]
        text_metadata = [{"source": t.metadata.get("source", "unknown")} for t in texts]

        embeddings = self._embed_texts(text_contents)

        self.vector_store.add_texts(texts=text_contents, embeddings=embeddings, metadatas=text_metadata)
        self.vector_store.persist()
        return len(texts)

    def retrieve(self, query, k=3):
        """检索与查询最相关的k个文本块"""
        if self.vector_store is None:
            self.load_vector_store()

        if self.vector_store is None:
            return []

        return self.vector_store.similarity_search(query, k=k)

    def get_doc_count(self):
        """获取向量库中文档数量"""
        if self.vector_store is None:
            self.load_vector_store()

        if self.vector_store is None:
            return 0

        return self.vector_store._collection.count()

    def clear_vector_store(self):
        """清空向量数据库"""
        if os.path.exists(self.persist_directory):
            import shutil
            shutil.rmtree(self.persist_directory)
        self.vector_store = None
