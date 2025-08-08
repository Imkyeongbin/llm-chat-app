# backend/schemas.py

from pydantic import BaseModel

# 프론트엔드 -> 백엔드 요청 데이터 형식
class ChatRequest(BaseModel):
    message: str

# 백엔드 -> 프론트엔드 응답 데이터 형식
class ChatResponse(BaseModel):
    reply: str