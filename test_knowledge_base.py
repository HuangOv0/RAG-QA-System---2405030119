"""测试知识库导入和问答功能"""
from rag_qa import RAGQA
import os

def test_knowledge_base():
    print("=== 测试知识库导入 ===")
    
    # 初始化RAG问答系统
    qa = RAGQA()
    
    # 清空旧的知识库
    qa.clear_knowledge_base()
    
    # 加载文档
    docs_folder = "./documents"
    if os.path.exists(docs_folder):
        print(f"从 {docs_folder} 加载文档...")
        count = qa.load_documents_from_folder(docs_folder)
        print(f"成功加载 {count} 个文本块")
    else:
        print(f"错误：文档文件夹 {docs_folder} 不存在")
        return False
    
    # 测试问答
    print("\n=== 测试问答功能 ===")
    
    test_questions = [
        "什么是自然语言处理？",
        "BERT是什么？",
        "Transformer有哪些核心组件？",
        "深度学习对NLP有什么影响？",
        "BERT在哪些任务上取得了突破？",
        "什么是计算机视觉？",  # 无关问题
        "苹果的价格是多少？"   # 无关问题
    ]
    
    for question in test_questions:
        print(f"\n问题: {question}")
        answer = qa.ask(question)
        print(f"回答: {answer}")
    
    print("\n=== 测试完成 ===")
    return True

if __name__ == "__main__":
    test_knowledge_base()
