"""Streamlit Web界面 - RAG智能问答系统"""
import streamlit as st
from rag_qa import RAGQA
from document_processor import DocumentProcessor
import tempfile
import os

# 页面配置
st.set_page_config(
    page_title="RAG智能问答系统",
    page_icon="📚",
    layout="wide"
)

# 初始化会话状态
if "qa_system" not in st.session_state:
    st.session_state.qa_system = RAGQA()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

def add_documents(uploaded_files):
    """处理上传的文档"""
    if not uploaded_files:
        st.warning("请先上传文档")
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
    
    # 加载文档到知识库
    with st.spinner("正在处理文档..."):
        count = st.session_state.qa_system.load_documents_from_folder(docs_folder)
        st.success(f"成功处理 {len(saved_files)} 个文档，生成 {count} 个文本块")

def clear_knowledge_base():
    """清空知识库"""
    st.session_state.qa_system.clear_knowledge_base()
    st.session_state.chat_history = []
    st.session_state.uploaded_files = []
    st.success("知识库已清空")

# 侧边栏
with st.sidebar:
    st.title("📚 知识库管理")
    
    # 文档上传
    uploaded_files = st.file_uploader(
        "上传文档",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True
    )
    
    if st.button("📥 构建/更新知识库"):
        add_documents(uploaded_files)
    
    st.divider()
    
    # 知识库状态
    kb_size = st.session_state.qa_system.get_knowledge_base_size()
    st.info(f"当前知识库文本块数量: **{kb_size}**")
    
    if st.session_state.uploaded_files:
        st.subheader("已上传文档:")
        for file in st.session_state.uploaded_files:
            st.write(f"- {file}")
    
    st.divider()
    
    if st.button("🗑️ 清空知识库", type="secondary"):
        clear_knowledge_base()

# 主内容区
st.title("💬 RAG智能问答系统")

# 显示对话历史
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 提问输入框
if prompt := st.chat_input("请输入您的问题..."):
    # 显示用户问题
    st.chat_message("user").markdown(prompt)
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    
    # 获取回答
    with st.spinner("正在思考..."):
        answer = st.session_state.qa_system.ask(prompt)
    
    # 显示回答
    st.chat_message("assistant").markdown(answer)
    st.session_state.chat_history.append({"role": "assistant", "content": answer})
