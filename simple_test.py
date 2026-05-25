from rag_qa import RAGQA

qa = RAGQA()
qa.load_knowledge_base('./docs')

print(f"文档块数量: {qa.get_doc_count()}")
print("\n=== 测试问答 ===")

questions = [
    "什么是Transformer?",
    "RAG技术的优势是什么?",
    "今天天气怎么样?"
]

for q in questions:
    print(f"\n问题: {q}")
    ans = qa.ask(q)
    print(f"回答: {ans}")