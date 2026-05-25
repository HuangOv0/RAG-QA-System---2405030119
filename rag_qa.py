import os
from langchain_classic.chains import ConversationalRetrievalChain
from langchain_ollama import OllamaLLM
from langchain_classic.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate
from knowledge_base import KnowledgeBase

class RAGQA:
    def __init__(self, model_name="deepseek-r1:7b"):
        self.model_name = model_name
        self.kb = KnowledgeBase()
        self.llm = OllamaLLM(model=model_name)
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.qa_chain = None
        
        self.system_prompt = """
基于提供的参考文档回答问题。

规则：
1. 仅使用参考文档中的信息进行回答
2. 如果文档中没有相关信息，请明确说"文档中未找到相关答案"
3. 回答要简洁明了，不要添加文档中没有的信息
4. 如果有多个相关信息，可以综合回答
"""

    def load_knowledge_base(self, folder_path=None):
        if folder_path and os.path.exists(folder_path):
            documents = self.kb.load_documents_from_folder(folder_path)
            if documents:
                self.kb.build_vector_store(documents)
        else:
            self.kb.load_vector_store()
        
        if self.kb.vector_store:
            retriever = self.kb.vector_store.as_retriever(search_kwargs={"k": 3})
            self.qa_chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=retriever,
                memory=self.memory,
                combine_docs_chain_kwargs={"prompt": self._build_prompt()}
            )
            print("RAG问答链初始化完成")
            return True
        return False

    def _build_prompt(self):
        prompt_template = self.system_prompt + """

参考文档：
{context}

问题：{question}

回答："""
        
        return PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )

    def ask(self, question):
        if not self.qa_chain:
            return "知识库未加载，请先构建或加载知识库"
        
        try:
            result = self.qa_chain({"question": question})
            answer = result.get("answer", "")
            
            if not answer.strip():
                return "文档中未找到相关答案"
            
            return answer
        except Exception as e:
            print(f"问答出错: {e}")
            return f"回答时发生错误: {e}"

    def clear_memory(self):
        self.memory.clear()
        print("对话记忆已清除")

    def get_doc_count(self):
        return self.kb.get_doc_count()

if __name__ == "__main__":
    print("初始化RAG问答系统...")
    qa = RAGQA()
    
    print("加载知识库...")
    qa.load_knowledge_base("./docs")
    
    print("\nRAG问答系统已就绪！")
    print("输入 'quit' 或 'exit' 退出")
    print("输入 'clear' 清除对话历史\n")
    
    while True:
        question = input("请输入问题：")
        
        if question.lower() in ["quit", "exit"]:
            print("退出系统")
            break
        
        if question.lower() == "clear":
            qa.clear_memory()
            print("对话历史已清除")
            continue
        
        if not question.strip():
            continue
        
        print("正在思考...")
        answer = qa.ask(question)
        print(f"回答：{answer}\n")