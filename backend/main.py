# backend/main.py

from dotenv import load_dotenv
load_dotenv()  # 👈 애플리케이션 시작 시 .env 파일에 있는 환경 변수를 가장 먼저 로드합니다.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mcp import FastApiMCP
from routers import chat, agent  # 👈 agent 라우터 추가

from datetime import datetime
import platform
import psutil  # pip install psutil 필요

# -------------------------------------------------------------
# 1. FastAPI 앱 생성 및 기본 설정
# -------------------------------------------------------------
app = FastAPI()

# 개발 환경에서는 전체 허용, 운영에서는 특정 도메인만 허용
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 기존 API 라우터 포함
app.include_router(chat.router)
app.include_router(agent.router)  # 👈 새로 만든 agent 라우터 추가

# -------------------------------------------------------------
# 2. FastAPI-MCP 서버 설정
# -------------------------------------------------------------
mcp = FastApiMCP(
    app,
    name="My Chatbot API Tools",
    include_operations=["send_message_to_chatbot"],
)

# -------------------------------------------------------------
# 3. 사용자 정의 MCP 도구 추가
# -------------------------------------------------------------
async def get_server_status() -> dict:
    """
    현재 API 서버의 상태, OS 정보, 시간, 메모리 사용률을 반환합니다.
    """
    return {
        "status": "ok",
        "server_name": platform.node(),
        "system": platform.system(),
        "release": platform.release(),
        "server_time": datetime.now().isoformat(),
        "memory_percent": psutil.virtual_memory().percent
    }

# MCP 도구 등록
mcp.tools.append(get_server_status)

# -------------------------------------------------------------
# 4. MCP 서버를 FastAPI 앱에 마운트
# -------------------------------------------------------------
mcp.mount()

# -------------------------------------------------------------
# 5. 기본 루트 경로
# -------------------------------------------------------------
@app.get("/")
def read_root():
    return {
        "message": "FastAPI 백엔드 서버가 실행 중입니다. MCP 서버가 /mcp 경로에 마운트되었습니다."
    }
