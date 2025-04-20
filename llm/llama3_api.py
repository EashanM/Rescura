# rescura/llm/llama3_api.py
import os
import time
import logging
from typing import Any, Dict, List, Optional, Iterator
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, AIMessageChunk
from langchain_core.outputs import ChatGeneration, ChatGenerationChunk, ChatResult
from langchain_core.callbacks import CallbackManagerForLLMRun
from groq import Groq
import tenacity
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LangChainLlama3Wrapper(BaseChatModel):
    """LangChain-compatible wrapper for Groq's Llama3 API"""
    
    client: Groq = None
    model_name: str = "llama3-70b-8192"
    temperature: float = 0.7
    max_tokens: int = 1024

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable not set")
        self.client = Groq(api_key=api_key)

    @tenacity.retry(
        stop=tenacity.stop_after_attempt(3),
        wait=tenacity.wait_exponential(multiplier=1, min=4, max=10),
        retry=tenacity.retry_if_exception_type(Exception),
        before_sleep=tenacity.before_sleep_log(logger, logging.WARNING),
    )
    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Main method to generate chat completion"""
        formatted_messages = [self._convert_message(m) for m in messages]
        
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=formatted_messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            stop=stop,
            **kwargs
        )
        
        return self._create_chat_result(response)

    def _convert_message(self, message: BaseMessage) -> dict:
        """Convert LangChain message to Groq format"""
        if message.type == "human":
            return {"role": "user", "content": message.content}
        elif message.type == "ai":
            return {"role": "assistant", "content": message.content}
        elif message.type == "system":
            return {"role": "system", "content": message.content}
        else:
            raise ValueError(f"Unsupported message type: {message.type}")

    def _create_chat_result(self, response: Any) -> ChatResult:
        """Convert Groq response to LangChain format"""
        generations = [
            ChatGeneration(message=AIMessageChunk(
                content=choice.message.content,
                response_metadata=getattr(choice, "response_metadata", {})
            ))
            for choice in response.choices
        ]
        
        return ChatResult(
            generations=generations,
            llm_output={
                "model": response.model,
                "usage": dict(response.usage) if response.usage else {}
            }
        )

    @property
    def _llm_type(self) -> str:
        return "groq-llama3-chat"

    def _stream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> Iterator[ChatGenerationChunk]:
        """Streaming implementation"""
        formatted_messages = [self._convert_message(m) for m in messages]
        
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=formatted_messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            stop=stop,
            stream=True,
            **kwargs
        )
        
        for chunk in response:
            content = chunk.choices[0].delta.content or ""
            yield ChatGenerationChunk(message=AIMessageChunk(content=content))
            if run_manager:
                run_manager.on_llm_new_token(content)

# Example usage
if __name__ == "__main__":
    from langchain_core.messages import HumanMessage

    llm = LangChainLlama3Wrapper()
    
    # Test basic generation
    messages = [
        HumanMessage(content="What's the first aid for a snake bite?")
    ]
    response = llm.invoke(messages)
    print("Response:", response.content)
