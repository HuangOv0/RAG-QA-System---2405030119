# RAG智能问答系统

基于本地知识库的RAG（检索增强生成）智能问答系统，支持多种文档格式上传、文本向量化存储和智能问答。

## 功能特性

📄 **多格式支持**: 支持PDF、DOCX、TXT、Markdown、HTML等多种文档格式
📚 **自动构建**: 自动构建本地向量知识库
💬 **智能问答**: 基于文档内容进行智能问答
🧠 **对话记忆**: 支持多轮对话记忆
📊 **实时状态**: 实时显示知识库状态
🌙 **夜间模式**: 支持夜间模式切换
📥 **导出功能**: 支持导出聊天记录
🚀 **批量处理**: 支持批量文档上传

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

### Web应用

运行Streamlit Web应用：

```bash
streamlit run app.py
```

或使用增强版应用（支持更多功能）：

```bash
streamlit run enhanced_app.py
```

### 使用流程

1. 在左侧侧边栏上传文档（支持PDF、DOCX、TXT、MD、HTML等格式）
2. 点击"构建知识库"按钮
3. 在主界面输入框中输入问题
4. 点击发送按钮获取回答

### 命令行版本

```bash
python cli_qa.py
```

### 测试Ollama连接

```bash
python test_ollama.py
```

## 项目结构

```
├── app.py                          # Streamlit Web应用
├── enhanced_app.py                 # 增强版Web应用
├── rag_qa.py                       # RAG问答链核心逻辑
├── document_processor.py           # 文档处理与向量存储
├── enhanced_document_processor.py  # 增强版文档处理器
├── cli_qa.py                       # 命令行版本
├── test_ollama.py                  # Ollama测试脚本
├── config.py                       # 系统配置
├── utils.py                        # 工具函数
├── requirements.txt                # 依赖清单
├── .gitignore                      # Git忽略配置
├── README.md                       # 项目说明
└── documents/                      # 文档存放目录
```

## 技术架构

### RAG流程

1. **文档加载**: 使用PyPDFLoader、Docx2txtLoader、TextLoader等加载器
2. **文本分块**: 使用RecursiveCharacterTextSplitter（chunk_size=1000, chunk_overlap=200）
3. **向量化**: 使用TF-IDF向量化（可扩展为Ollama嵌入模型）
4. **向量存储**: 使用Chroma向量数据库
5. **检索**: 基于相似性检索返回最相关的3个文本块
6. **生成**: 使用DeepSeek-R1大模型进行回答

### 系统提示词

```
你是一个智能问答助手，请根据提供的参考文档回答用户的问题。
参考文档如下:
{context}

请基于上述文档内容回答用户的问题。如果文档中没有相关信息，请明确说"文档中未找到相关答案"，不要编造答案。

用户问题:
{question}

请提供详细的回答:
```

## 配置说明

### 系统配置 (config.py)

- `CHUNK_SIZE`: 文档分块大小（默认1000）
- `CHUNK_OVERLAP`: 分块重叠大小（默认200）
- `DEFAULT_RETRIEVAL_K`: 默认检索数量（默认3）
- `LLM_MODEL`: 使用的LLM模型（默认deepseek-r1:7b）

### 支持的文件格式

- PDF文档 (.pdf)
- Word文档 (.docx)
- 纯文本 (.txt)
- Markdown文件 (.md, .markdown)
- HTML文件 (.html, .htm)

## 功能增强

### 相比原版本的改进

1. ✅ 支持更多文档格式（Markdown、HTML）
2. ✅ 添加夜间模式
3. ✅ 支持批量文档上传
4. ✅ 添加问答记录导出功能（JSON、TXT、CSV）
5. ✅ 优化代码结构和模块化
6. ✅ 添加配置文件管理
7. ✅ 添加工具函数库
8. ✅ 改进错误处理和用户提示

## 常见问题

### Q: Ollama连接失败怎么办？

A: 请确保：
1. Ollama服务正在运行
2. 已下载所需模型（deepseek-r1:7b）
3. 网络连接正常

### Q: 支持哪些文档格式？

A: 目前支持PDF、DOCX、TXT、Markdown、HTML格式。

### Q: 如何清空知识库？

A: 在Web界面侧边栏点击"清空知识库"按钮，或在命令行中输入'clear'命令。

### Q: 聊天记录如何导出？

A: 在增强版应用中，点击侧边栏的"导出聊天记录"按钮，支持JSON、TXT、CSV格式。

## 性能优化建议

1. **文档大小**: 建议单个文档不超过50MB
2. **文档数量**: 建议知识库中文档片段不超过1000个
3. **检索数量**: 可根据需要调整检索的文档块数量
4. **模型选择**: 可根据硬件配置选择合适的模型大小

## 开发路线图

- [ ] 支持更多文档格式（Excel、PPT等）
- [ ] 添加用户认证功能
- [ ] 支持多语言
- [ ] 添加文档预处理功能
- [ ] 支持分布式部署
- [ ] 添加API接口
- [ ] 支持自定义提示词模板

## License

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 联系方式

如有问题或建议，请通过GitHub Issues联系。