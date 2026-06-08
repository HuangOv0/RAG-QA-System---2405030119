"""Streamlit Web应用 - RAG智能问答系统"""
import streamlit as st
from rag_qa import RAGQA
from document_processor import DocumentProcessor
import tempfile
import os

# 页面配置
st.set_page_config(
    page_title="RAG智能问答系统",
    page_icon="🤖",
    layout="wide"
)

# 初始化QA系统
if "qa_system" not in st.session_state:
    st.session_state.qa_system = RAGQA()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

def add_documents(uploaded_files):
    """添加文档到知识库"""
    if not uploaded_files:
        st.warning("请先上传文件")
        return
    
    docs_folder = "./documents"
    os.makedirs(docs_folder, exist_ok=True)
    
    saved_files = []
    for uploaded_file in uploaded_files:
        file_path = os.path.join(docs_folder, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        saved_files.append(file_path)
        st.session_state.uploaded_files.append(uploaded_file.name)
    
    # 构建知识库
    with st.spinner("正在构建知识库..."):
        count = st.session_state.qa_system.load_documents_from_folder(docs_folder)
        st.success(f"成功添加 {len(saved_files)} 个文件，共 {count} 个文档片段")

def clear_knowledge_base():
    """清空知识库"""
    st.session_state.qa_system.clear_knowledge_base()
    st.session_state.chat_history = []
    st.session_state.uploaded_files = []
    st.success("知识库已清空")

# 侧边栏
with st.sidebar:
    st.title("🤖 智能问答系统")
    
    # 文档上传
    uploaded_files = st.file_uploader(
        "上传文档",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True
    )
    
    if st.button("📚 构建知识库"):
        add_documents(uploaded_files)
    
    st.divider()
    
    # 知识库状态
    kb_size = st.session_state.qa_system.get_knowledge_base_size()
    st.info(f"📊 知识库状态: **{kb_size}** 个文档片段")
    
    if st.session_state.uploaded_files:
        st.subheader("已上传文件:")
        for file in st.session_state.uploaded_files:
            st.write(f"- {file}")
    
    st.divider()
    
    if st.button("🗑️ 清空知识库", type="secondary"):
        clear_knowledge_base()

# 主界面
st.title("🤖 RAG智能问答系统")

# 显示聊天历史
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 用户输入
if prompt := st.chat_input("请输入您的问题..."):
    # 显示用户消息
    st.chat_message("user").markdown(prompt)
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    
    # 获取回答
    with st.spinner("正在思考..."):
        answer = st.session_state.qa_system.ask(prompt)
    
    # 显示回答
    st.chat_message("assistant").markdown(answer)
    st.session_state.chat_history.append({"role": "assistant", "content": answer})