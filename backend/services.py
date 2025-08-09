# backend/services.py

import os
from openai import OpenAI
from schemas import ChatRequest

# 환경 변수는 main.py에서 이미 로드되었으므로 여기서 바로 사용합니다.
API_KEY = os.getenv("OPENAI_API_KEY") # .env 파일에 OPENAI_API_KEY 또는 MCP_API_KEY 등이 설정되어 있어야 합니다.
MODEL_NAME = os.getenv("LLM_MODEL_NAME")

# 클라이언트 초기화
if not API_KEY:
    # 이 에러는 서버 시작 시 발생하여 문제를 바로 알 수 있게 합니다.
    raise ValueError("API_KEY가 환경 변수에 설정되지 않았습니다. .env 파일을 확인하세요.")

try:
    # 사용하는 라이브러리에 맞게 클라이언트를 초기화합니다. (여기는 OpenAI 예시)
    from openai import OpenAI
    client = OpenAI(api_key=API_KEY)
except Exception as e:
    print(f"LLM 클라이언트 초기화 실패: {e}")
    client = None


async def get_llm_response(request: ChatRequest) -> str:
    """
    LLM 모델로부터 직접 응답을 받아오는 서비스 함수.
    'send_message_to_chatbot' 도구의 실제 로직입니다.
    """
    if not client:
        return "LLM 서비스 클라이언트가 초기화되지 않았습니다. 서버 로그를 확인하세요."

    print(f"LLM 서비스 직접 호출: 모델({MODEL_NAME}), 메시지({request.message})")

    try:
        # 사용하는 LLM 라이브러리의 API 호출 방식에 맞게 작성합니다.
        response = client.chat.completions.create(
            model=MODEL_NAME or "gpt-3.5-turbo", # .env에 모델이 없으면 기본값 사용
            messages=[
                {"role": "user", "content": request.message}
            ]
        )
        
        reply = response.choices[0].message.content
        return reply

    except Exception as e:
        print(f"LLM 서비스 호출 중 에러 발생: {e}")
        return "죄송합니다. LLM 서비스와 통신하는 중 오류가 발생했습니다."