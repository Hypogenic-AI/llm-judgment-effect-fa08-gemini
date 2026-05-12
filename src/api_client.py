import os
import json
import time
from typing import List, Dict, Any, Optional
from openai import OpenAI
from anthropic import Anthropic
from tenacity import retry, wait_exponential, stop_after_attempt
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self, provider: str = "openai", model: str = "gpt-4o-mini"):
        self.provider = provider
        self.model = model
        if provider == "openai":
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        elif provider == "anthropic":
            self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        elif provider == "openrouter":
            self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=os.getenv("OPENROUTER_API_KEY"),
            )
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    @retry(wait=wait_exponential(min=1, max=60), stop=stop_after_attempt(5))
    def call(self, system_prompt: str, user_prompt: str, temperature: float = 0.0) -> Dict[str, Any]:
        start_time = time.time()
        if self.provider in ["openai", "openrouter"]:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=temperature,
            )
            content = response.choices[0].message.content
            usage = {
                "input_tokens": response.usage.prompt_tokens,
                "output_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            }
        elif self.provider == "anthropic":
            response = self.client.messages.create(
                model=self.model,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt},
                ],
                max_tokens=4096,
                temperature=temperature,
            )
            content = response.content[0].text
            usage = {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
                "total_tokens": response.usage.input_tokens + response.usage.output_tokens,
            }
        
        latency = time.time() - start_time
        return {
            "content": content,
            "usage": usage,
            "latency": latency,
            "model": self.model,
            "provider": self.provider
        }
