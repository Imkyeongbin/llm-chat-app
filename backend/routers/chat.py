# backend/routers/chat.py

from fastapi import APIRouter
from schemas import ChatRequest, ChatResponse  # 수정된 부분
from services import get_llm_response        # 수정된 부분

router = APIRouter(prefix="/api")

@router.post(
    "/chat",
    response_model=ChatResponse, # 수정된 부분
    operation_id="send_message_to_chatbot",
    tags=["Chatbot"],
)
async def chat_with_llm(request: ChatRequest): # 수정된 부분
    """
    사용자의 메시지를 받아 챗봇에게 전달하고 응답을 반환합니다.
    """
    reply = await get_llm_response(request)
    return ChatResponse(reply=reply) # 수정된 부분