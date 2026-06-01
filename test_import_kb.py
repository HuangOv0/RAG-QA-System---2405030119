"""测试自然语言处理知识库导入功能"""
from document_processor import DocumentProcessor
import os

def test_import_knowledge_base():
    print("=== 测试自然语言处理知识库导入 ===")
    
    # 初始化文档处理器
    processor = DocumentProcessor()
    print("文档处理器初始化完成")
    
    # 加载文档
    docs_folder = "./documents"
    if os.path.exists(docs_folder):
        print(f"\n从 {docs_folder} 加载文档...")
        
        # 获取所有文档文件
        doc_files = []
        for filename in os.listdir(docs_folder):
            if filename.endswith('.txt'):
                doc_files.append(os.path.join(docs_folder, filename))
        
        print(f"找到 {len(doc_files)} 个文档文件:")
        for doc_file in doc_files:
            print(f"  - {os.path.basename(doc_file)}")
        
        # 加载所有文档
        all_documents = []
        for doc_file in doc_files:
            docs = processor.load_document(doc_file)
            all_documents.extend(docs)
            print(f"    已加载: {doc_file}")
        
        print(f"\n共加载 {len(all_documents)} 个文档")
        
        # 创建向量库
        print("正在创建向量库...")
        count = processor.create_vector_store(all_documents)
        print(f"成功导入 {count} 个文本块到知识库")
        
        # 验证向量库状态
        vector_count = processor.get_doc_count()
        print(f"向量库中共有 {vector_count} 个文档向量")
        
        # 测试检索功能
        print("\n=== 测试检索功能 ===")
        test_query = "什么是BERT？"
        results = processor.retrieve(test_query, k=2)
        print(f"查询: {test_query}")
        print(f"找到 {len(results)} 条相关结果")
        for i, result in enumerate(results):
            print(f"\n结果 {i+1}:")
            print(f"来源: {result['metadata'].get('source', '未知')}")
            print(f"内容摘要: {result['page_content'][:100]}...")
        
        print("\n=== 知识库导入成功 ===")
        return True
    else:
        print(f"错误：文档文件夹 {docs_folder} 不存在")
        return False

if __name__ == "__main__":
    test_import_knowledge_base()
