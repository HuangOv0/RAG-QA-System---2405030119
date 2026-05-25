# RAG智能问答系统

基于本地知识库的RAG（检索增强生成）智能问答系统，使用Ollama本地大模型、LangChain框架和Streamlit构建。

## 功能特点

- 📚 支持PDF、DOCX、TXT多种文档格式
- 🔍 基于Chroma向量数据库的高效文本检索
- 💬 支持多轮对话和上下文记忆
- 🖥️ 友好的Web交互界面
- 🚀 本地部署，无需联网

## 环境要求

- Python 3.10+
- Ollama（用于运行本地大模型）
- 至少8GB内存（推荐16GB以上）

## 安装步骤

### 1. 安装Ollama

下载并安装Ollama：https://ollama.com/download

### 2. 下载大模型

```bash
ollama pull deepseek-r1:7b
ollama pull nomic-embed-text
```

### 3. 克隆仓库

```bash
git clone <仓库地址>
cd RAG-QA-System
```

### 4. 创建虚拟环境并安装依赖

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# 或
source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
```

## 使用说明

### 运行Web应用

```bash
streamlit run streamlit_app.py
```

### 使用步骤

1. **上传文档**：在左侧栏上传PDF、DOCX或TXT文件
2. **构建知识库**：点击"构建知识库"按钮处理文档
3. **加载本地文档**：或点击"加载本地文档"使用docs目录下的示例文档
4. **提问**：在右侧问答区输入问题并点击"提问"
5. **查看回答**：系统会基于知识库内容给出回答

### 命令行版本

```bash
python rag_qa.py
```

## 项目结构

```
RAG-QA-System/
├── docs/                 # 示例文档目录
├── chroma_db/            # 向量数据库（运行时生成）
├── knowledge_base.py     # 知识库管理模块
├── rag_qa.py             # RAG问答链模块
├── streamlit_app.py      # Streamlit Web应用
├── test_ollama.py        # Ollama测试脚本
├── requirements.txt      # 依赖列表
└── .gitignore            # Git忽略配置
```

## 关键技术点

### RAG流程

1. **文档加载**：支持PDF、DOCX、TXT等多种格式
2. **文本分块**：使用RecursiveCharacterTextSplitter，chunk_size=1000，chunk_overlap=200
3. **向量化**：使用Ollama内置的nomic-embed-text嵌入模型
4. **存储**：使用Chroma向量数据库
5. **检索**：基于相似度检索最相关的3个文本块
6. **生成**：使用deepseek-r1:7b大模型生成回答

### 系统提示词设计

系统要求模型仅使用参考文档中的信息进行回答，如果文档中没有相关信息，需明确说明"文档中未找到相关答案"。

## 测试示例

**相关问题：**
- 什么是Transformer?
- BERT和GPT有什么区别?
- 文本分类的应用场景有哪些?
- RAG技术的优势是什么?
- 情感分析面临哪些挑战?

**无关问题：**
- 今天天气怎么样?
- 中国的首都是哪里?

## 已知问题与改进方向

- 大模型推理速度较慢，建议使用GPU加速
- 文档解析对复杂格式支持有限
- 可增加文档预览和管理功能
- 可支持更多文档格式（如Markdown、Excel等）

## 许可证

MIT License