import logging, os, requests

MAX_REQUESTS_PER_DAY = 2000
MAX_LENGTH_TEXT = 300
logger = logging.getLogger(__name__)


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class AssistantAPI(metaclass=SingletonMeta):

    def __init__(self, persist_dir: str, collection_name: str):
        from rag.embeddings import MyEmbedding
        from rag.vectorstores import ChromaVectorStore
        from rag.pipelines import RAGQueryPipeline

        logger.debug("Initializing Assistant API with Chroma + DashScope.")
        self.total_requests = 0

        self.embedding = MyEmbedding()
        logger.debug("1/3 Connected to DashScope embedding model (text-embedding-v4)")

        self.vector_store_interface = ChromaVectorStore(
            embedding=self.embedding,
            persist_dir=persist_dir,
            collection_name=collection_name
        )
        logger.debug("2/3 Connected to Chroma Vector Store")

        self.query_api = RAGQueryPipeline(self.vector_store_interface)
        logger.debug("3/3 RAG pipeline Ready!")

    def process_user_request(self, chat_request):
        if self.total_requests >= MAX_REQUESTS_PER_DAY:
            raise Exception("Max requests limit reached.")

        if len(chat_request) > 20:
            chat_request = chat_request[20:]

        # RAG 检索
        retrieved_docs = self.query_api.query(chat_request[-1]['content'], k=4)
        docs_content = "\n\n".join([doc.page_content for doc in retrieved_docs])

        for chat in chat_request:
            if len(chat['content']) > MAX_LENGTH_TEXT:
                chat['content'] = chat['content'][:MAX_LENGTH_TEXT]

        # 系统提示词
        try:
            fetched_system_prompt = open('system.prompt', 'r', encoding='utf-8').readlines()
            system_prompt = ''.join(fetched_system_prompt)
        except Exception:
            raise Exception("System prompt error")

        # 组装消息
        messages = [{"role": "system", "content": system_prompt}]
        if docs_content:
            messages.append({"role": "user", "content": f"Relevant context:\n{docs_content}"})
        for chat_unit in chat_request:
            messages.append({"role": chat_unit['role'], "content": chat_unit['content']})

        # 使用 DashScope OpenAI 兼容模式 API
        dashscope_key = os.getenv("DASHSCOPE_API_KEY")
        base_url = os.getenv("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
        model_name = os.getenv("CHAT_MODEL_NAME", "qwen-plus")

        response = requests.post(
            url=f"{base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {dashscope_key}",
                "Content-Type": "application/json",
            },
            json={"model": model_name, "messages": messages}
        )

        self.total_requests += 1
        return str(response.json()["choices"][0]["message"]["content"])
