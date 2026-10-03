"""LLM client wrapper - support multi provider gratis via HTTP (gak butuh SDK berat)."""
import os
import json
import requests
from typing import Optional
from .config import GOOGLE_API_KEY, GROQ_API_KEY, GEMINI_MODEL, GROQ_MODEL


class LLMClient:
    """Client LLM ringan pakai requests (HTTP langsung, no SDK heavy)."""

    def __init__(self):
        self.google_key = GOOGLE_API_KEY if GOOGLE_API_KEY != "your_gemini_api_key_here" else None
        self.groq_key = GROQ_API_KEY if GROQ_API_KEY != "your_groq_api_key_here" else None
        self.gemini_model = GEMINI_MODEL
        self.groq_model = GROQ_MODEL

    def _call_gemini(self, prompt: str, system: str, temperature: float) -> Optional[str]:
        """Call Google Gemini API langsung via REST."""
        if not self.google_key:
            return None

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.gemini_model}:generateContent"
        headers = {"Content-Type": "application/json"}
        params = {"key": self.google_key}

        full_prompt = f"{system}\n\n{prompt}" if system else prompt

        body = {
            "contents": [{"parts": [{"text": full_prompt}]}],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": 8192,
            },
        }

        # Retry 3x kalau timeout/network error
        last_error = None
        for attempt in range(3):
            try:
                resp = requests.post(url, headers=headers, params=params, json=body, timeout=180)
                if resp.status_code == 200:
                    data = resp.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        content = candidates[0].get("content", {})
                        parts = content.get("parts", [])
                        if parts:
                            return parts[0].get("text", "")
                elif resp.status_code in (429, 503):  # Rate limit / overloaded
                    print(f"[Gemini] {resp.status_code} (attempt {attempt+1}/3), retry...")
                    last_error = f"HTTP {resp.status_code}"
                    continue
                else:
                    print(f"[Gemini] HTTP {resp.status_code}: {resp.text[:200]}")
                    return None
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                print(f"[Gemini] Timeout/Connection (attempt {attempt+1}/3): {e}")
                last_error = str(e)
                continue
            except Exception as e:
                print(f"[Gemini] Error: {e}")
                return None

        if last_error:
            print(f"[Gemini] Gagal setelah 3 percobaan: {last_error}")
        return None

    def _call_groq(self, prompt: str, system: str, temperature: float) -> Optional[str]:
        """Call Groq API langsung via REST."""
        if not self.groq_key:
            return None

        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.groq_key}",
            "Content-Type": "application/json",
        }

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        body = {
            "model": self.groq_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 8192,
        }

        try:
            resp = requests.post(url, headers=headers, json=body, timeout=60)
            if resp.status_code == 200:
                data = resp.json()
                choices = data.get("choices", [])
                if choices:
                    return choices[0].get("message", {}).get("content", "")
            else:
                print(f"[Groq] HTTP {resp.status_code}: {resp.text[:200]}")
                return None
        except Exception as e:
            print(f"[Groq] Error: {e}")
            return None

        return None

    def generate(self, prompt: str, system: str = "", temperature: float = 0.7) -> str:
        """Generate teks. Otomatis fallback ke provider lain jika primary error."""
        # Try Gemini dulu
        if self.google_key:
            result = self._call_gemini(prompt, system, temperature)
            if result:
                return result
            print("[LLM] Gemini gagal, coba Groq...")

        # Fallback ke Groq
        if self.groq_key:
            result = self._call_groq(prompt, system, temperature)
            if result:
                return result

        # Tidak ada provider yang berhasil
        return self._mock_response(prompt)

    def _mock_response(self, prompt: str) -> str:
        """Response placeholder jika belum ada API key yang valid."""
        return f"""⚠️ [API KEY BELUM VALID]

Prompt diterima: {prompt[:200]}...

Kemungkinan masalah:
1. API key salah / expired
2. API key tidak punya akses ke model {self.gemini_model}
3. Rate limit tercapai

Cara fix:
1. Cek API key di https://aistudio.google.com/apikey
2. Pastikan model '{self.gemini_model}' tersedia untuk key kamu
3. Coba buat API key baru

Lihat README.md section 'API Key Gratis' untuk detail."""


# Singleton instance
_client = None

def get_llm() -> LLMClient:
    """Ambil instance LLM client (singleton)."""
    global _client
    if _client is None:
        _client = LLMClient()
    return _client