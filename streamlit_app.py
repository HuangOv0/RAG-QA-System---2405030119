import streamlit as st
import os
import tempfile
from rag_qa import RAGQA

def init_session_state():
    if 'qa_system' not in st.session_state:
        st.session_state.qa_system = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'doc_count' not in st.session_state:
        st.session_state.doc_count = 0

def main():
    st.set_page_config(page_title="RAG智能问答系统", layout="wide")
    
    init_session_state()
    
    st.title("📚 RAG智能问答系统")
    st.subheader("基于本地知识库的智能问答")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.sidebar.title("知识库管理")
        
        uploaded_files = st.file_uploader(
            "上传文档",
            type=["pdf", "docx", "txt"],
            accept_multiple_files=True
        )
        
        if st.button("📥 构建知识库"):
            if uploaded_files:
                with st.spinner("正在处理文档..."):
                    with tempfile.TemporaryDirectory() as temp_dir:
                        for uploaded_file in uploaded_files:
                            file_path = os.path.join(temp_dir, uploaded_file.name)
                            with open(file_path, "wb") as f:
                                f.write(uploaded_file.getbuffer())
                        
                        if st.session_state.qa_system is None:
                            st.session_state.qa_system = RAGQA()
                        
                        st.session_state.qa_system.load_knowledge_base(temp_dir)
                        st.session_state.doc_count = st.session_state.qa_system.get_doc_count()
                    
                    st.success(f"知识库构建完成！共 {st.session_state.doc_count} 个文本块")
            else:
                st.warning("请先上传文档")
        
        if st.button("📂 加载本地文档"):
            with st.spinner("正在加载本地知识库..."):
                if st.session_state.qa_system is None:
                    st.session_state.qa_system = RAGQA()
                
                st.session_state.qa_system.load_knowledge_base("./docs")
                st.session_state.doc_count = st.session_state.qa_system.get_doc_count()
            
            st.success(f"本地知识库加载完成！共 {st.session_state.doc_count} 个文本块")
        
        if st.button("🗑️ 清除对话历史"):
            if st.session_state.qa_system:
                st.session_state.qa_system.clear_memory()
            st.session_state.chat_history = []
            st.success("对话历史已清除")
        
        st.info(f"当前知识库文本块数量: **{st.session_state.doc_count}**")
    
    with col2:
        st.header("问答交互")
        
        for i, (question, answer) in enumerate(st.session_state.chat_history):
            with st.chat_message("user"):
                st.write(f"**问题:** {question}")
            with st.chat_message("assistant"):
                st.write(f"**回答:** {answer}")
        
        user_input = st.text_input("请输入您的问题：", key="question_input")
        
        if st.button("提问"):
            if user_input.strip():
                if st.session_state.qa_system is None:
                    st.warning("请先构建或加载知识库")
                else:
                    with st.spinner("正在思考..."):
                        answer = st.session_state.qa_system.ask(user_input)
                    
                    st.session_state.chat_history.append((user_input, answer))
                    
                    with st.chat_message("user"):
                        st.write(f"**问题:** {user_input}")
                    with st.chat_message("assistant"):
                        st.write(f"**回答:** {answer}")
            else:
                st.warning("请输入问题")

if __name__ == "__main__":
    main()