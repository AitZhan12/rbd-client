import logging
import time

import requests

from config import settings


OLLAMA_URL = settings.OLLAMA_URL
MODEL = settings.MODEL


def query_llm(prompt: str) -> str:
    try:
        r = requests.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
        }, timeout=300)
        return r.json()["response"]
    except (requests.ConnectionError, requests.Timeout) as e:
        logging.warning(f"LLM: {e}")
    return ""


async def process_item_llm(item):
    prompt = f"""Перепиши объявление другими словами, сохранив весь смысл.
                 Меняй формулировки и порядок предложений, но НЕ добавляй новых фактов и характеристик.
                 Верни ТОЛЬКО переписанный текст.
                 Текст: {item}"""
    response = query_llm(prompt)
    return response