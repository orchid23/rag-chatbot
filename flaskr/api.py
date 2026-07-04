import os
from flask import Blueprint, request
from .gpt import AssistantAPI
import logging

logger = logging.getLogger(__name__)
bp = Blueprint('api', __name__, url_prefix='/api')

# Chroma 配置
PERSIST_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")
COLLECTION_NAME = os.getenv("VECTOR_DB_COLLECTION", "rag_collection")

assistant = AssistantAPI(persist_dir=PERSIST_DIR, collection_name=COLLECTION_NAME)


@bp.route('/gen', methods=['POST'])
def gen():
    if request.method == 'POST':
        
        chat_request = request.json
        if chat_request:
            try:
                logger.info(str(chat_request[-1]))
                response = assistant.process_user_request(chat_request)
                logger.info(" --> Response: \"" + response + "\"")
                return response, 200
            except Exception as e:
                logger.error(str(chat_request))
                logger.error(str(e))
                return 'Internal Server Error', 500
        else:
            return 'The request of the user is empty', 400
