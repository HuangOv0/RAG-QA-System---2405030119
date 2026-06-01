from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb
from chromadb.config import Settings
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

class SimpleEmbeddings:
    """简单的TF-IDF嵌入模型"""
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=384)
        self.fitted = False
    
    def embed_documents(self, texts):
        if not self.fitted:
            self.vectorizer.fit(texts)
            self.fitted = True
        vectors = self.vectorizer.transform(texts).toarray()
        # 调整维度到384
        if vectors.shape[1] < 384:
            padding = np.zeros((vectors.shape[0], 384 - vectors.shape[1]))
            vectors = np.concatenate([vectors, padding], axis=1)
        elif vectors.shape[1] > 384:
            vectors = vectors[:, :384]
        return vectors.tolist()
    
    def embed_query(self, text):
        return self.embed_documents([text])[0]

class DocumentProcessor:
    def __init__(self, persist_directory="./db"):
        self.persist_directory = persist_directory
        self.embeddings = SimpleEmbeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        self.client = None
        self.collection = None
        self._init_chroma()

    def _init_chroma(self):
        """初始化Chroma客户端"""
        try:
            self.client = chromadb.PersistentClient(
                path=self.persist_directory,
                settings=Settings(anonymized_telemetry=False)
            )
            # 创建或获取集合
            self.collection = self.client.get_or_create_collection("rag_collection")
        except Exception as e:
            print(f"初始化Chroma失败: {e}")
            self.client = None
            self.collection = None

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
        """嵌入文本"""
        return self.embeddings.embed_documents(texts)

    def create_vector_store(self, documents):
        """创建并保存向量数据库"""
        if self.collection is None:
            print("Chroma未初始化")
            return 0

        texts = self.split_documents(documents)
        text_contents = [t.page_content for t in texts]
        text_metadata = [{"source": t.metadata.get("source", "unknown")} for t in texts]

        # 手动嵌入
        embeddings = self._embed_texts(text_contents)
        
        # 生成唯一ID
        ids = [f"doc_{i}" for i in range(len(text_contents))]

        # 添加到集合
        self.collection.add(
            documents=text_contents,
            embeddings=embeddings,
            metadatas=text_metadata,
            ids=ids
        )

        return len(texts)

    def load_vector_store(self):
        """加载已保存的向量数据库"""
        if os.path.exists(self.persist_directory):
            try:
                self.client = chromadb.PersistentClient(
                    path=self.persist_directory,
                    settings=Settings(anonymized_telemetry=False)
                )
                self.collection = self.client.get_collection("rag_collection")
                return True
            except Exception as e:
                print(f"加载向量库失败: {e}")
                return False
        return False

    def add_documents(self, new_documents):
        """向现有向量库添加新文档"""
        if self.collection is None:
            self.load_vector_store()

        if self.collection is None:
            return self.create_vector_store(new_documents)

        texts = self.split_documents(new_documents)
        text_contents = [t.page_content for t in texts]
        text_metadata = [{"source": t.metadata.get("source", "unknown")} for t in texts]

        # 获取当前文档数量
        count = self.get_doc_count()
        ids = [f"doc_{count + i}" for i in range(len(text_contents))]

        # 手动嵌入
        embeddings = self._embed_texts(text_contents)

        # 添加到集合
        self.collection.add(
            documents=text_contents,
            embeddings=embeddings,
            metadatas=text_metadata,
            ids=ids
        )

        return len(texts)

    def retrieve(self, query, k=3):
        """检索与查询最相关的k个文本块"""
        if self.collection is None:
            self.load_vector_store()

        if self.collection is None:
            return []

        # 嵌入查询
        query_embedding = self.embeddings.embed_query(query)
        
        # 查询
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )

        # 转换结果格式
        docs = []
        if results and 'documents' in results and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                metadata = results['metadatas'][0][i] if results['metadatas'] else {}
                docs.append({
                    'page_content': doc,
                    'metadata': metadata,
                    'distance': results['distances'][0][i] if results['distances'] else 0
                })
        
        return docs

    def get_doc_count(self):
        """获取向量库中文档数量"""
        if self.collection is None:
            self.load_vector_store()

        if self.collection is None:
            return 0

        return self.collection.count()

    def clear_vector_store(self):
        """清空向量数据库"""
        if os.path.exists(self.persist_directory):
            import shutil
            shutil.rmtree(self.persist_directory)
        self.client = None
        self.collection = None
        self._init_chroma()
