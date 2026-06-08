from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from document_processor import DocumentProcessor
import os

class RAGQA:
    def __init__(self, use_llm=False):
        self.use_llm = use_llm
        self.llm = None
        self.document_processor = DocumentProcessor()
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.chain = None
        
        # 初始化LLM
        if use_llm:
            self._init_llm()

    def _init_llm(self):
        """初始化LLM模型"""
        try:
            from langchain_community.chat_models import ChatOllama
            self.llm = ChatOllama(model="deepseek-r1:7b", temperature=0.1)
            print("LLM模型初始化成功")
        except Exception as e:
            print(f"LLM模型初始化失败: {e}")
            self.use_llm = False

    def add_documents(self, documents):
        """添加文档到知识库"""
        count = self.document_processor.add_documents(documents)
        return count

    def load_documents_from_folder(self, folder_path):
        """从文件夹加载所有支持的文档"""
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
        # 检查知识库
        if self.document_processor.get_doc_count() == 0:
            return "知识库为空，请先上传文档并构建知识库"
        
        # 检索相关文档
        results = self.document_processor.retrieve(question, k=3)
        
        if not results:
            return "未找到相关文档"
        
        # 构建上下文
        context = "\n\n".join([f"文档 {i+1} ({r['metadata'].get('source', '未知')}):\n{r['page_content']}" 
                               for i, r in enumerate(results)])
        
        if self.use_llm and self.llm:
            # 使用LLM生成回答
            template = """你是一个智能问答助手，请根据提供的参考文档回答用户的问题。
参考文档如下:
{context}

请基于上述文档内容回答用户的问题。如果文档中没有相关信息，请明确说"文档中未找到相关答案"，不要编造答案。

用户问题:
{question}

请提供详细的回答:"""
            
            prompt = PromptTemplate(
                input_variables=["context", "question"],
                template=template
            )
            
            try:
                from langchain.chains import LLMChain
                chain = LLMChain(llm=self.llm, prompt=prompt)
                result = chain.invoke({"context": context, "question": question})
                answer = result.get("text", "").strip()
                if not answer or "不知道" in answer or "未找到" in answer:
                    return "文档中未找到相关答案"
                return answer
            except Exception as e:
                return f"LLM生成失败: {str(e)}"
        else:
            # 简单基于检索结果的回答
            answer = f"基于知识库找到以下相关信息:\n\n"
            for i, result in enumerate(results):
                source = result['metadata'].get('source', '未知')
                content = result['page_content'][:300]
                answer += f"• 来源: {os.path.basename(source)}\n{content}...\n\n"
            return answer

    def clear_history(self):
        """清空对话历史"""
        self.memory.clear()

    def get_knowledge_base_size(self):
        """获取知识库大小"""
        return self.document_processor.get_doc_count()

    def clear_knowledge_base(self):
        """清空知识库"""
        self.document_processor.clear_vector_store()
        self.chain = None