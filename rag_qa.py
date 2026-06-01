from langchain_community.chat_models import ChatOllama
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from document_processor import DocumentProcessor

class RAGQA:
    def __init__(self, model_name="deepseek-r1:7b"):
        self.model_name = model_name
        self.llm = ChatOllama(model=model_name, temperature=0.1)
        self.document_processor = DocumentProcessor()
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.chain = None
        
        self._init_chain()

    def _init_chain(self):
        """初始化RAG问答链"""
        template = """基于提供的参考文档回答用户的问题。
        如果文档中没有相关信息，请明确说"文档中未找到相关答案"，不要编造答案。
        
        参考文档：
        {context}
        
        对话历史：
        {chat_history}
        
        用户问题：
        {question}
        
        请用中文回答："""
        
        prompt = PromptTemplate(
            input_variables=["context", "chat_history", "question"],
            template=template
        )
        
        if self.document_processor.vector_store is not None:
            retriever = self.document_processor.vector_store.as_retriever(search_kwargs={"k": 3})
            self.chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=retriever,
                memory=self.memory,
                combine_docs_chain_kwargs={"prompt": prompt},
                verbose=True
            )

    def add_documents(self, documents):
        """添加文档到知识库"""
        count = self.document_processor.add_documents(documents)
        self._init_chain()
        return count

    def load_documents_from_folder(self, folder_path):
        """从文件夹加载所有支持的文档"""
        import os
        documents = []
        for filename in os.listdir(folder_path):
            filepath = os.path.join(folder_path, filename)
            if os.path.isfile(filepath):
                ext = os.path.splitext(filename)[1].lower()
                if ext in [".pdf", ".docx", ".txt"]:
                    try:
                        docs = self.document_processor.load_document(filepath)
                        documents.extend(docs)
                    except Exception as e:
                        print(f"加载文件 {filename} 失败: {e}")
        
        if documents:
            return self.add_documents(documents)
        return 0

    def ask(self, question):
        """回答用户问题"""
        if self.chain is None:
            return "知识库尚未构建，请先上传文档并构建知识库。"
        
        try:
            result = self.chain.invoke({"question": question})
            answer = result.get("answer", "").strip()
            if not answer or "不知道" in answer or "无法回答" in answer:
                return "文档中未找到相关答案"
            return answer
        except Exception as e:
            return f"问答过程中出现错误: {str(e)}"

    def clear_history(self):
        """清除对话历史"""
        self.memory.clear()

    def get_knowledge_base_size(self):
        """获取知识库大小"""
        return self.document_processor.get_doc_count()

    def clear_knowledge_base(self):
        """清空知识库"""
        self.document_processor.clear_vector_store()
        self.chain = None
