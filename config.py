"""配置文件 - 系统配置"""
import os

class Config:
    """系统配置类"""
    
    # 基础配置
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DOCUMENTS_DIR = os.path.join(BASE_DIR, "documents")
    DATABASE_DIR = os.path.join(BASE_DIR, "db")
    
    # 文档处理配置
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    MAX_DOCUMENTS = 1000
    
    # 向量数据库配置
    VECTOR_DIMENSION = 384
    COLLECTION_NAME = "rag_collection"
    
    # 检索配置
    DEFAULT_RETRIEVAL_K = 3
    MAX_RETRIEVAL_K = 10
    
    # LLM配置
    LLM_MODEL = "deepseek-r1:7b"
    LLM_TEMPERATURE = 0.1
    LLM_MAX_TOKENS = 2000
    
    # 支持的文件格式
    SUPPORTED_FORMATS = [".pdf", ".docx", ".txt", ".md", ".markdown", ".html", ".htm"]
    
    # 界面配置
    APP_TITLE = "RAG智能问答系统"
    APP_ICON = "🤖"
    
    # 导出配置
    EXPORT_FORMATS = ["json", "txt", "csv"]
    
    @classmethod
    def create_directories(cls):
        """创建必要的目录"""
        os.makedirs(cls.DOCUMENTS_DIR, exist_ok=True)
        os.makedirs(cls.DATABASE_DIR, exist_ok=True)
    
    @classmethod
    def get_file_size_limit(cls):
        """获取文件大小限制（MB）"""
        return 50  # 50MB

# 初始化配置
Config.create_directories()