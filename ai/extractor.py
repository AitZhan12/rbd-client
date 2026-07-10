import json
import requests

from config import settings

OLLAMA_URL = settings.OLLAMA_URL
MODEL = settings.MODEL

EXTRACT_PROMPT = """Ты помощник по поиску квартир. Извлеки параметры из запроса в JSON.

Поля (если не указано — null):
- district: название района (строка) — например "Абайский", "Аль-Фарабийский"
- landmark: ориентир/достопримечательность (строка) — площадь, ТРЦ, парк, вокзал
- rooms: количество комнат (число)
- floor_min, floor_max: этаж от/до (число)
- price_min, price_max: цена от/до (число, тенге)
- area_min, area_max: площадь от/до (число, м²)
- good_condition: true если просят хороший ремонт/состояние
- deal_type: 1=продажа, 2=аренда

Правила маппинга:
- "нижние этажи" → floor_max: 3
- "высокие этажи" → floor_min: 5
- "не первый этаж" → floor_min: 2
- "хороший ремонт", "с ремонтом" → good_condition: true
- "снять", "аренда" → deal_type: 2, иначе deal_type: 1

ВАЖНО про локацию:
- Если указан РАЙОН (Абайский, Каратауский и т.п.) → поле district
- Если указан ОРИЕНТИР (площадь, парк, ТРЦ, вокзал, аэропорт) → поле landmark
- "площадь Аль-Фараби", "возле Дендропарка", "рядом с вокзалом" → это landmark, НЕ district

Верни ТОЛЬКО JSON без пояснений.

Запрос: {query}"""


def extract_params(user_query: str) -> dict:
    prompt = EXTRACT_PROMPT.format(query=user_query)
    r = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
    }, timeout=120)
    text = r.json()["response"]
    # чистим от возможных ```json обёрток
    text = text.replace("```json", "").replace("```", "").strip()
    return json.loads(text)