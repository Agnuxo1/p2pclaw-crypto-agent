"""
NVIDIA NIM API Client for OpenCLAW Nebula-Crypto.
Optimized for Llama-3.3-Nemotron-70B.
"""

import os
import httpx
import asyncio
import logging

logger = logging.getLogger(__name__)

# Fallback tokens if not in env
NVIDIA_TOKENS = [
    os.getenv("NVIDIA_TOKEN_1", "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"),
    os.getenv("NVIDIA_TOKEN_2", "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"),
    os.getenv("NVIDIA_TOKEN_3", "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"),
]
NVIDIA_TOKENS = [t for t in NVIDIA_TOKENS if t and t.startswith("nvapi-")]

DEFAULT_MODEL = os.getenv("NVIDIA_MODEL", "nvidia/llama-3.3-nemotron-70b-instruct")
BASE_URL = "https://integrate.api.nvidia.com/v1/chat/completions"

class NVIDIAClusterClient:
    def __init__(self):
        self.tokens = NVIDIA_TOKENS
        self.current_idx = 0

    def _get_token(self):
        token = self.tokens[self.current_idx]
        self.current_idx = (self.current_idx + 1) % len(self.tokens)
        return token

    async def complete(
        self,
        messages: list,
        max_tokens: int = 4000,
        temperature: float = 0.7,
        fast: bool = False,
    ) -> str:
        """
        Asynchronous completion with token rotation.
        """
        if not self.tokens:
            raise RuntimeError("No NVIDIA tokens found.")

        async with httpx.AsyncClient(timeout=120.0) as client:
            for attempt in range(len(self.tokens) * 2):
                token = self._get_token()
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "model": DEFAULT_MODEL,
                    "messages": messages,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "stream": False
                }

                try:
                    r = await client.post(BASE_URL, headers=headers, json=payload)
                    
                    if r.status_code == 429:
                        await asyncio.sleep(10 * (attempt + 1))
                        continue
                        
                    r.raise_for_status()
                    data = r.json()
                    return data["choices"][0]["message"]["content"].strip()
                    
                except Exception as e:
                    if attempt == (len(self.tokens) * 2) - 1:
                        raise RuntimeError(f"NVIDIA API failed all tokens: {e}")
                    await asyncio.sleep(2)

        raise RuntimeError("NVIDIA NIM: retries exhausted")

llm_client = NVIDIAClusterClient()

async def complete(messages, max_tokens=4000, temperature=0.7, fast=False):
    return await llm_client.complete(messages, max_tokens, temperature, fast)
