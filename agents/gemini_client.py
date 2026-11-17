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

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

CANDIDATE_MODELS = [
    "gemini-3.1-flash-lite",
    "gemini-3.8-flash",
    "gemini-3.5-flash"
]

def call_agent_llm(prompt: str, system_instruction: str, temperature: float = 0.2) -> str:
    """Invokes LLM with automated fallback across available Gemini models."""
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
