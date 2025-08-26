import os
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_deepseek import ChatDeepSeek
from langchain_openai import ChatOpenAI


def get_llm(model_name: str = "gpt-4o") -> BaseChatModel:
    if model_name.startswith("deepseek"):
        api_key = os.environ.get("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY is not set")
        return ChatDeepSeek(
            model=model_name,
            api_key=api_key,
            temperature=0,
            streaming=True,
        )

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set")
    return ChatOpenAI(
        model=model_name,
        api_key=api_key,
        temperature=0,
        streaming=True,
    )
