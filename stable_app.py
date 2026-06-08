"""稳定版RAG智能问答系统"""
import streamlit as st
import os
import json
from datetime import datetime

st.set_page_config(
    page_title="RAG智能问答系统",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化会话状态
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []
if "kb_ready" not in st.session_state:
    st.session_state.kb_ready = False
if "doc_count" not in st.session_state:
    st.session_state.doc_count = 0
if "docs_content" not in st.session_state:
    st.session_state.docs_content = []

def simple_qa(question, documents):
    """简单的基于关键词匹配的问答"""
    if not documents:
        return "知识库为空，请先上传文档"
    
    question_lower = question.lower()
    results = []
    
    for doc in documents:
        content_lower = doc.lower()
        if any(keyword in content_lower for keyword in question_lower.split()):
            results.append(doc[:500] + "..." if len(doc) > 500 else doc)
    
    if results:
        answer = "基于知识库找到以下相关信息：\n\n"
        for i, result in enumerate(results[:3], 1):
            answer += f"【{i}】{result}\n\n"
        return answer
    else:
        return "未找到相关文档"

def add_documents(uploaded_files):
    """添加文档到知识库"""
    if not uploaded_files:
        st.warning("请先上传文件")
        return
    
    docs_folder = "./documents"
    os.makedirs(docs_folder, exist_ok=True)
    
    saved_files = []
    for uploaded_file in uploaded_files:
        try:
            file_path = os.path.join(docs_folder, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # 读取文件内容并保存到会话状态
            with open(file_path, "r", encoding='utf-8', errors='ignore') as f:
                content = f.read()
                st.session_state.docs_content.append(content)
            
            saved_files.append(file_path)
            if uploaded_file.name not in st.session_state.uploaded_files:
                st.session_state.uploaded_files.append(uploaded_file.name)
        
        except Exception as e:
            st.error(f"处理文件 {uploaded_file.name} 失败: {str(e)}")
    
    if saved_files:
        st.session_state.kb_ready = True
        st.session_state.doc_count = len(st.session_state.docs_content)
        st.success(f"成功添加 {len(saved_files)} 个文件，共 {st.session_state.doc_count} 个文档")

def clear_knowledge_base():
    """清空知识库"""
    st.session_state.docs_content = []
    st.session_state.chat_history = []
    st.session_state.uploaded_files = []
    st.session_state.kb_ready = False
    st.session_state.doc_count = 0
    
    import shutil
    if os.path.exists("./db"):
        try:
            shutil.rmtree("./db")
        except:
            pass
    if os.path.exists("./documents"):
        try:
            shutil.rmtree("./documents")
        except:
            pass
    
    st.success("知识库已清空")

def export_chat_history():
    """导出聊天记录"""
    if not st.session_state.chat_history:
        st.warning("没有聊天记录可导出")
        return
    
    export_data = {
        "export_time": datetime.now().isoformat(),
        "total_messages": len(st.session_state.chat_history),
        "chat_history": st.session_state.chat_history
    }
    
    json_str = json.dumps(export_data, ensure_ascii=False, indent=2)
    
    st.download_button(
        label="📥 下载聊天记录",
        data=json_str,
        file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json"
    )

# 侧边栏
with st.sidebar:
    st.title("🤖 智能问答系统")
    
    st.divider()
    
    uploaded_files = st.file_uploader(
        "上传文档 (支持TXT/MD/PDF/DOCX)",
        type=["txt", "md", "pdf", "docx"],
        accept_multiple_files=True
    )
    
    if st.button("📚 构建知识库"):
        add_documents(uploaded_files)
    
    st.divider()
    
    st.info(f"📊 知识库状态: {'✅ 已就绪' if st.session_state.kb_ready else '❌ 未就绪'}")
    st.info(f"📄 文档数量: {st.session_state.doc_count}")
    
    if st.session_state.uploaded_files:
        st.subheader("已上传文件:")
        for file in st.session_state.uploaded_files:
            st.write(f"- {file}")
    
    st.divider()
    
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
    st.chat_message("user").markdown(prompt)
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    
    with st.spinner("正在思考..."):
        answer = simple_qa(prompt, st.session_state.docs_content)
    
    st.chat_message("assistant").markdown(answer)
    st.session_state.chat_history.append({"role": "assistant", "content": answer})

st.divider()
st.caption("💡 提示：支持TXT、Markdown、PDF、DOCX等文档格式")
