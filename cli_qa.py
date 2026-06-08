"""命令行版本 - RAG智能问答系统"""
from rag_qa import RAGQA
import os

def main():
    print("=== RAG智能问答系统 (命令行版本) ===")
    
    # 初始化RAG问答系统
    qa = RAGQA()
    
    # 加载文档
    docs_folder = "./documents"
    if os.path.exists(docs_folder):
        print(f"\n正在从 {docs_folder} 加载文档...")
        count = qa.load_documents_from_folder(docs_folder)
        print(f"成功加载 {count} 个文档片段")
    else:
        print(f"\n文档目录 {docs_folder} 不存在，请先添加文档")
    
    print("\n请输入您的问题 (输入 'quit' 或 'exit' 退出，输入 'clear' 清空历史)\n")
    
    while True:
        question = input("请输入问题: ")
        
        if question.lower() in ['quit', 'exit']:
            print("再见！")
            break
        elif question.lower() == 'clear':
            qa.clear_history()
            print("历史记录已清空")
            continue
        
        answer = qa.ask(question)
        print(f"\n回答: {answer}\n")

if __name__ == "__main__":
    main()