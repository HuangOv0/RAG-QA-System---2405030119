"""增强版Streamlit应用 - 支持夜间模式和导出功能"""
import streamlit as st
from rag_qa import RAGQA
from enhanced_document_processor import EnhancedDocumentProcessor
import tempfile
import os
import json
from datetime import datetime

# 页面配置
st.set_page_config(
    page_title="RAG智能问答系统",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS
def apply_custom_theme():
    """应用自定义主题"""
    if st.session_state.get('dark_mode', False):
        # 夜间模式
        st.markdown("""
        <style>
        .stApp {
            background-color: #1e1e1e;
            color: #ffffff;
        }
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            background-color: #2d2d2d;
            color: #ffffff;
        }
        .stButton > button {
            background-color: #4a4a4a;
            color: #ffffff;
        }
        </style>
        """, unsafe_allow_html=True)

# 初始化会话状态
if "qa_system" not in st.session_state:
    # 使用增强版文档处理器
    qa_system = RAGQA()
    qa_system.document_processor = EnhancedDocumentProcessor()
    st.session_state.qa_system = qa_system

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# 应用主题
apply_custom_theme()

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

def export_chat_history():
    """导出聊天记录"""
    if not st.session_state.chat_history:
        st.warning("没有聊天记录可导出")
        return
    
    # 创建导出数据
    export_data = {
        "export_time": datetime.now().isoformat(),
        "total_messages": len(st.session_state.chat_history),
        "chat_history": st.session_state.chat_history
    }
    
    # 转换为JSON
    json_str = json.dumps(export_data, ensure_ascii=False, indent=2)
    
    # 提供下载
    st.download_button(
        label="📥 下载聊天记录",
        data=json_str,
        file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json"
    )

def toggle_dark_mode():
    """切换夜间模式"""
    st.session_state.dark_mode = not st.session_state.dark_mode
    st.rerun()

# 侧边栏
with st.sidebar:
    st.title("🤖 智能问答系统")
    
    # 夜间模式切换
    if st.button("🌙 切换夜间模式"):
        toggle_dark_mode()
    
    st.divider()
    
    # 文档上传 - 支持更多格式
    supported_formats = st.session_state.qa_system.document_processor.get_supported_formats()
    format_str = ", ".join([f[1:].upper() for f in supported_formats])
    
    uploaded_files = st.file_uploader(
        f"上传文档 ({format_str})",
        type=[f[1:] for f in supported_formats],
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
    
    # 导出功能
    if st.button("📥 导出聊天记录"):
        export_chat_history()
    
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

# 底部信息
st.divider()
st.caption("💡 提示：支持PDF、DOCX、TXT、Markdown、HTML等多种文档格式 | 可切换夜间模式 | 支持导出聊天记录")