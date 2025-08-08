# backend/routers/chat.py

from fastapi import APIRouter
from .. import schemas, services # 상위 폴더의 schemas와 services 모듈 임포트

# APIRouter 인스턴스 생성
# prefix="/api" : 이 라우터의 모든 경로 앞에 /api가 자동으로 붙습니다.
router = APIRouter(prefix="/api")


@router.post("/chat", response_model=schemas.ChatResponse)
async def chat_with_llm(request: schemas.ChatRequest):
    """
    프론트엔드와 통신하는 채팅 API 엔드포인트.
    실제 로직은 services.py의 함수를 호출하여 처리합니다.
    """
    reply = await services.get_llm_response(request)
    return schemas.ChatResponse(reply=reply)