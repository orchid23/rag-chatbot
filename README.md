# 📚 RAG Chatbot API — 智能文档问答后端服务

[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-black)](https://flask.palletsprojects.com/)
[![LangChain](https://img.shields.io/badge/LangChain-0.3-orange)](https://github.com/langchain-ai/langchain)
[![Chroma](https://img.shields.io/badge/Chroma-0.5+-brightgreen)](https://github.com/chroma-core/chroma)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED)](https://www.docker.com/)

> 基于 Flask + LangChain + Chroma + DashScope 构建的 RAG 智能文档问答后端服务。支持 PDF/TXT 文档批量导入、向量化存储、语义检索与多轮对话上下文管理，提供 RESTful API 接口。

---

## 为什么做这个

把 RAG 的完整链路跑通——从文档加载、分块、向量化、存入 Chroma，到检索、拼上下文、喂给 LLM 生成回答。用 Flask 包了一层 RESTful API，方便前端或别的服务调用。

架构上用了 Interface → Implementation 的设计模式，Loader、Splitter、VectorStore 都抽象了接口，后面想换 Pinecone、Milvus 或者其他 Embedding 模型只需要新增实现类就行。

---

## 能干什么

- 把 PDF / TXT 文档灌入 Chroma 向量库
- 用户发消息 → 自动检索相关文档片段 → 拼入上下文 → LLM 生成回答
- 支持多轮对话（前端传完整消息历史）
- 支持 Docker 部署
- 接口风格的设计，方便扩展

---

## 怎么跑起来

### 1. 装依赖

```bash
git clone https://github.com/orchid23/rag-chatbot-api.git
cd rag-chatbot-api

python -m venv venv
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

pip install -r requirements_chroma.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 2. 配置 `.env`

填上你的 DashScope API Key：

```
DASHSCOPE_API_KEY=sk-你的key
DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
CHAT_MODEL_NAME=qwen-plus
VECTOR_DB_COLLECTION=rag_collection
```

Key 在这里申请：[DashScope 控制台](https://dashscope.console.aliyun.com/apiKey)

### 3. 导入文档

把 PDF 或 TXT 文件丢到 `data/` 目录，然后：

```bash
python scripts/rag_ingest.py
```

也可以指定文件：

```bash
python scripts/rag_ingest.py docs/简历.pdf docs/项目说明.txt
```

### 4. 启动

```bash
# 开发模式
venv\Scripts\python.exe -m flask --app flaskr run --host=0.0.0.0 --port=5000 --debug

# Windows 直接双击
start.bat

# 生产模式
gunicorn -w 4 -b 0.0.0.0:5000 "flaskr:create_app()"
```

浏览器打开：
- 前端页面：**http://localhost:5000/index**
- API 接口：**http://localhost:5000/api/gen**（POST）

---

## API 接口

### `POST /api/gen`

多轮对话问答接口。

**请求：**

```json
[
  {"role": "user", "content": "你熟悉 Python 吗？"},
  {"role": "assistant", "content": "是的，我有多年的 Python 开发经验。"},
  {"role": "user", "content": "那你用过 Flask 吗？"}
]
```

**返回：**

```
是的，我使用 Flask 构建过多个 RESTful API 服务...
```

---

## 项目结构

```
.
├── flaskr/
│   ├── __init__.py          # Flask 应用工厂
│   ├── api.py               # /api/gen 接口
│   ├── frontend.py          # /index 前端页面
│   └── gpt.py               # RAG 问答核心逻辑（单例）
├── rag/
│   ├── embeddings.py        # DashScope Embedding 封装
│   ├── loaders.py           # 文档加载器（PDF/TXT/自动识别）
│   ├── splitters.py         # 文本分块器
│   ├── vectorstores.py      # Chroma 向量存储（单例）
│   ├── pipelines.py         # 摄入管道 + 查询管道
│   └── tests/
├── scripts/
│   ├── rag_ingest.py        # 文档导入脚本
│   └── test_rag_query.py    # 检索测试脚本
├── data/                    # 知识库文档目录
├── chroma_db/               # Chroma 持久化目录
├── .env                     # 环境配置
├── system.prompt            # LLM 系统提示词
├── Dockerfile               # Docker 镜像
├── start.bat                # Windows 一键启动
├── requirements_chroma.txt  # 依赖清单
└── README.md
```

---

## 设计上的一些想法

**1. 接口驱动设计**

Loader、Splitter、VectorStore 都定义了抽象接口，具体实现可以随意替换。比如想从 Chroma 换成 Pinecone，只需要新增一个 `PineconeVectorStore` 实现 `VectorStoreInterface` 就行，Pipeline 层零改动。

**2. 单例模式**

`ChromaVectorStore` 和 `AssistantAPI` 都用了单例，避免每次请求都重新连接向量库和初始化 Embedding 模型。

**3. OpenAI 兼容模式调用 LLM**

不走 LangChain 的 LLM 抽象，直接用 `requests` 调 DashScope 的 OpenAI 兼容接口。更轻量，也方便后续换成其他兼容 OpenAI API 的服务（Ollama、vLLM 等）。

**4. 自动文件类型识别**

`AutoLoader` 会根据文件后缀自动选 PDF 还是 TXT 加载器，批量导入时不用手动区分。

---

## 技术栈

| 层 | 用的什么 |
|----|----------|
| 后端框架 | Flask 3.x |
| RAG 框架 | LangChain 0.3 |
| LLM | 通义千问 Qwen-Plus（DashScope OpenAI 兼容模式） |
| Embedding | text-embedding-v4 |
| 向量库 | Chroma |
| 文档解析 | PyPDF + LangChain Loaders |
| 部署 | Docker + Gunicorn |

---

## Docker 部署

```bash
docker build -t rag-chatbot-api .
docker run -p 5000:5000 --env-file .env rag-chatbot-api
```

---

## 后续想做的

- [ ] 支持更多文件格式（Word、Markdown、CSV）
- [ ] 流式响应（SSE）
- [ ] 对话历史持久化
- [ ] 前端聊天界面改造
- [ ] 支持多知识库切换

---

## License

MIT

---

## 作者

**orchid23**

如果这个项目对你有点用，欢迎 Star ⭐ 或者提 Issue 交流。
