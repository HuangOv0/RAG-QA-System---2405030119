# RAG智能问答系统

基于本地知识库的RAG（检索增强生成）智能问答系统，支持PDF/DOCX文档上传、文本向量化存储和智能问答。

## 功能特性

- 📄 支持PDF和DOCX文档上传
- 📚 自动构建本地向量知识库
- 💬 基于文档内容进行智能问答
- 🧠 支持多轮对话记忆
- 📊 实时显示知识库状态

## 环境要求

- Python 3.10+
- Ollama（用于部署本地大模型）

## 安装步骤

### 1. 安装Ollama

访问 [Ollama官方网站](https://ollama.com/) 下载并安装Ollama。

### 2. 下载大模型

```bash
ollama pull deepseek-r1:7b
ollama pull nomic-embed-text
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

## 使用说明

### 运行Web应用

```bash
streamlit run app.py
```

### 使用流程

1. 在左侧侧边栏上传PDF或DOCX文档
2. 点击"构建/更新知识库"按钮
3. 在主界面输入框中输入问题
4. 点击发送按钮获取回答

### 命令行版本

```bash
python cli_qa.py
```

## 关键技术点

### RAG流程

1. **文档加载**: 使用PyPDFLoader和Docx2txtLoader加载文档
2. **文本分块**: 使用RecursiveCharacterTextSplitter（chunk_size=1000, chunk_overlap=200）
3. **向量化**: 使用Ollama的nomic-embed-text嵌入模型
4. **向量存储**: 使用Chroma向量数据库
5. **检索**: 基于相似性检索返回最相关的3个文本块
6. **生成**: 使用DeepSeek-R1大模型进行回答

### 系统提示词

```
基于提供的参考文档回答用户的问题。
如果文档中没有相关信息，请明确说"文档中未找到相关答案"，不要编造答案。
```

## 项目结构

```
├── app.py              # Streamlit Web应用
├── rag_qa.py           # RAG问答链核心逻辑
├── document_processor.py # 文档处理与向量存储
├── cli_qa.py           # 命令行版本
├── test_ollama.py      # Ollama测试脚本
├── requirements.txt    # 依赖清单
├── .gitignore          # Git忽略配置
└── documents/          # 文档存放目录
```

## 已知问题与改进方向

- [ ] 支持更多文档格式（如TXT、Markdown）
- [ ] 添加夜间模式
- [ ] 支持批量文档上传
- [ ] 添加问答记录导出功能
- [ ] 优化大模型响应速度

## License

MIT License
