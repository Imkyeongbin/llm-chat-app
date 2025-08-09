# backend/routers/agent.py

import os
import inspect
import json
from fastapi import APIRouter, HTTPException
from schemas import ChatRequest, ChatResponse
from openai import OpenAI
import asyncio

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY가 .env 파일에 설정되지 않았습니다.")

client = OpenAI(api_key=OPENAI_API_KEY)
router = APIRouter(prefix="/api/agent")


def format_tools_for_openai(mcp_tools):
    if not mcp_tools:
        return None
    
    formatted_tools = []
    for tool in mcp_tools:
        if isinstance(tool, dict):
            formatted_tools.append({"type": "function", "function": tool})
        elif inspect.isfunction(tool) or inspect.iscoroutinefunction(tool):
            tool_schema = {
                "name": tool.__name__,
                "description": inspect.getdoc(tool),
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            }
            formatted_tools.append({"type": "function", "function": tool_schema})
    return formatted_tools


async def execute_tool(mcp_tools, tool_name, args):
    """MCP 도구 실행"""
    for tool in mcp_tools:
        if inspect.isfunction(tool) or inspect.iscoroutinefunction(tool):
            if tool.__name__ == tool_name:
                if inspect.iscoroutinefunction(tool):
                    return await tool(**args)
                else:
                    return tool(**args)
    raise ValueError(f"'{tool_name}' MCP 도구를 찾을 수 없습니다.")


@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    from main import mcp

    print(f"[Agent] 받은 메시지: {request.message}")
    
    mcp_tools = mcp.tools
    openai_tools = format_tools_for_openai(mcp_tools)

    if not openai_tools:
        raise HTTPException(status_code=500, detail="MCP 도구를 찾을 수 없습니다.")

    try:
        # 1차 모델 호출
        response = client.chat.completions.create(
            model="gpt-5-nano",
            messages=[{"role": "user", "content": request.message}],
            tools=openai_tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        # 도구 호출 감지
        if message.tool_calls:
            tool_call = message.tool_calls[0]
            tool_name = tool_call.function.name
            tool_args = tool_call.function.arguments or {}

            # arguments가 문자열(JSON)로 올 수 있으니 dict로 변환
            if isinstance(tool_args, str):
                try:
                    tool_args = json.loads(tool_args)
                except json.JSONDecodeError:
                    print(f"[Agent] tool_args JSON 파싱 실패. 받은 값: {tool_args}")
                    tool_args = {}

            print(f"[Agent] '{tool_name}' MCP 도구 실행 시도. args={tool_args}")

            # 도구 실행
            try:
                result = await execute_tool(mcp_tools, tool_name, tool_args)
            except Exception as e:
                result = {"error": str(e)}

            print(f"[Agent] MCP 도구 실행 결과: {result}")

            # 모델에 도구 실행 결과 전달하여 최종 응답 생성
            followup = client.chat.completions.create(
                model="gpt-5-nano",
                messages=[
                    {"role": "user", "content": request.message},
                    message,  # 모델의 tool call 메시지
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result),
                    }
                ]
            )

            final_content = followup.choices[0].message.content or "응답을 생성하지 못했습니다."
            return ChatResponse(reply=final_content)

        # 도구 호출이 없으면 그냥 모델 답변 반환
        final_response = message.content or "응답을 생성하지 못했습니다."
        return ChatResponse(reply=final_response)

    except Exception as e:
        print(f"[Agent] OpenAI API 호출 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))
