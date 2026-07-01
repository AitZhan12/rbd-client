from dataclasses import dataclass
from datetime import datetime


@dataclass
class SearchFilters:
    city: int = 4
    object_type: int = 1
    source: int = 2
    rooms: str | None = None
    price_from: int | None = None
    price_to: int | None = None
    sell: bool = True
    lease: bool = False
    new: bool = False


def parse_dt(value):
    """rbd отдаёт даты строкой '2026-06-26T08:14:11.000+05:00' или 'None'."""
    if not value or value == "None":
        return None
    return datetime.fromisoformat(value)


def map_item_to_row(item: dict) -> dict:
    """Сырой объект из API -> dict под колонки модели Apartment."""
    return {
        "id": item["id"],
        "source": "rbd",
        "source_id": item["id"],

        # характеристики
        "object_type": item.get("objectType"),
        "room_count": item.get("roomCount"),
        "area": item.get("area"),
        "floor_num": item.get("floorNum"),
        "floor_count": item.get("floorCount"),
        "ceiling_height": item.get("ceilingHeight"),
        "year_built": item.get("yearBuilt"),
        "condition": item.get("condition"),
        "condition_text": item.get("condition__text"),
        "toilet_type": item.get("toiletType"),
        "furniture_type": item.get("furnitureType"),
        "former_dorm": item.get("formerDorm"),
        "bail": item.get("bail"),

        # цена
        "deal_type": 1 if item.get("sell") else 2,
        "price": item.get("sellPrice") or item.get("leasePrice"),
        "price_meter": item.get("sellPriceMeter") or item.get("leasePriceMeter"),
        "currency": item.get("sellCurrency") or item.get("leaseCurrency"),
        "supply_source": item.get("supplySource"),
        "flat_type": item.get("flatType"),
        "lease_price_period": item.get("leasePricePeriod"),

        # локация
        "city": item.get("city"),
        "address_id": item.get("address"),
        "address_name": item.get("addressName"),
        "intersection_name": item.get("intersectionName"),
        "district_id": item.get("district"),
        "district_text": item.get("district__text") or None,
        "coord_x": item.get("coordX"),
        "coord_y": item.get("coordY"),
        "geohash": item.get("geohash"),
        "house_num": item.get("houseNum"),

        # источник
        "krisha_id": item.get("krishaId"),
        "load_source": item.get("loadSource"),
        "photo": item.get("photo"),
        "phone": item.get("phone"),

        # текст
        "memo_public": item.get("memoPublic"),

        # даты с сайта
        "dt_create": parse_dt(item.get("dtCreate")),
        "dt_modify": parse_dt(item.get("dtModify")),
    }