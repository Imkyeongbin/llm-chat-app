# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mcp import FastApiMCP
from routers import chat
from datetime import datetime

# -------------------------------------------------------------
# 1. FastAPI 앱 생성 및 기본 설정
# -------------------------------------------------------------
app = FastAPI()

origins = ["http://localhost:3000", "localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 기존 API 라우터 포함
app.include_router(chat.router)

# -------------------------------------------------------------
# 2. FastAPI-MCP 서버 설정
# -------------------------------------------------------------
mcp = FastApiMCP(
    app,
    name="My Chatbot API Tools",
    include_operations=["send_message_to_chatbot"],
)

# 3. 사용자 정의 MCP 도구 추가 (수정된 방식)
# 3.1. 도구로 사용할 함수를 먼저 정의합니다.
async def get_server_status() -> dict:
    """
    현재 API 서버의 상태와 시간을 반환합니다.
    """
    return {
        "status": "ok",
        "server_time": datetime.now().isoformat()
    }

# 3.2. 정의한 함수를 .tools 리스트에 append 합니다.
mcp.tools.append(get_server_status)


# 4. MCP 서버를 FastAPI 앱에 마운트
mcp.mount()


# 루트 경로
@app.get("/")
def read_root():
    return {"message": "FastAPI 백엔드 서버가 실행 중입니다. MCP 서버가 /mcp 경로에 마운트되었습니다."}