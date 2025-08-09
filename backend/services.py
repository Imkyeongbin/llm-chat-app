# backend/services.py

import time
from schemas import ChatRequest

async def get_llm_response(request: ChatRequest) -> str:
    """
    LLM 모델로부터 응답을 받아오는 비즈니스 로직 함수
    """
    print(f"서비스 로직 실행: 받은 메시지 - {request.message}")

    # ===============================================================
    # ✨✨✨
    # TODO: 이 함수 안에 MCP LLM 연동 코드를 집중적으로 구현하세요.
    # ✨✨✨
    # ===============================================================

    # LLM 응답 시뮬레이션
    time.sleep(1.5)
    llm_reply = f"'{request.message}'에 대한 LLM의 답변입니다. (모듈화 완료!)"

    return llm_reply