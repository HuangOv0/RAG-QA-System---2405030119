"""测试Streamlit应用"""
import streamlit as st

st.title("测试应用")
st.write("Hello, Streamlit!")

# 测试文档处理
try:
    from document_processor import DocumentProcessor
    dp = DocumentProcessor()
    st.success("文档处理器初始化成功")
except Exception as e:
    st.error(f"文档处理器初始化失败: {e}")

# 测试RAG
try:
    from rag_qa import RAGQA
    qa = RAGQA()
    st.success("RAG系统初始化成功")
except Exception as e:
    st.error(f"RAG系统初始化失败: {e}")
