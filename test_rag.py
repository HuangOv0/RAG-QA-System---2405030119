from rag_qa import RAGQA

print("初始化RAG问答系统...")
qa = RAGQA()

print("加载知识库...")
qa.load_knowledge_base('./docs')

print(f"文档块数量: {qa.get_doc_count()}")

print("\n测试问题1: 什么是Transformer?")
result = qa.ask("什么是Transformer?")
print(f"回答: {result}")

print("\n测试问题2: RAG技术的优势是什么?")
result = qa.ask("RAG技术的优势是什么?")
print(f"回答: {result}")

print("\n测试问题3: 今天天气怎么样?")
result = qa.ask("今天天气怎么样?")
print(f"回答: {result}")