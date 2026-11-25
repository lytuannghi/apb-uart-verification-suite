# ============================================================================
# Gemini Multi-Agent Core Engine
# Author: Lý Tuấn Nghi (lytuannghi) & Multi-Agent IC Design Team
# ============================================================================

import os
import re
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

_client = None


def get_client():
    """Lazily initialize Gemini API client only when LLM inference is invoked."""
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is not set; run with --offline or configure .env")
        _client = genai.Client(api_key=api_key)
    return _client


CANDIDATE_MODELS = [
    "gemini-3.1-flash-lite",
    "gemini-3.8-flash",
    "gemini-3.5-flash"
]

def call_agent_llm(prompt: str, system_instruction: str, temperature: float = 0.2) -> str:
    """Invokes LLM with automated fallback across available Gemini models."""
    client = get_client()
    last_err = None
    for model in CANDIDATE_MODELS:
        try:
            resp = client.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=temperature
                )
            )
            if resp and resp.text:
                return resp.text.strip()
        except Exception as e:
            last_err = e
            time.sleep(1)
            continue
    raise RuntimeError(f"All models exhausted. Last error: {last_err}")

def extract_code(text: str, lang: str = "verilog") -> str:
    """Extracts raw code from markdown code blocks."""
    pattern = rf"```{lang}?\s*(.*?)```"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return text.strip()
