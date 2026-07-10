from dataclass import SearchFilters


def build_payload(filters: SearchFilters, page=1):
    demand = {
        "sell": {"type": "boolean", "value": filters.sell},
        "city": {"type": "number", "value": filters.city},
        "sellCurrency": {"type": "number", "value": 1},
        "leaseCurrency": {"type": "number", "value": 1},
        "areaMeasureType": {"type": "number", "value": 1},
        "landMeasureType": {"type": "number", "value": 2},
        "objectType": {"type": "number", "value": filters.object_type},
        "sortType": {"type": "number", "value": 1},
        "viewType": {"type": "number", "value": 3},
        "external": {"type": "boolean", "value": True},
        "areaLandMeasure": {"type": "number", "value": 2},
        "label": {"type": "number", "value": 1},
        "searchMine": {"type": "boolean", "value": True},
        "searchGlobal": {"type": "boolean", "value": True},
        "searchAgency": {"type": "boolean", "value": True},
        "searchOther": {"type": "boolean", "value": True},
        "searchArchive": {"type": "boolean", "value": False},
        "search": {"type": "boolean", "value": True},
        "supplySource": {"type": "number", "value": filters.source},
        "lead": {"type": "boolean", "value": False},
        "clientType": {"type": "number", "value": 1},
    }

    if filters.lease:
        demand["lease"] = {"type": "boolean", "value": True}

    return {
        "type": "databox",
        "value": {
            "filter": {"type": "databox", "value": {
                "address": {"type": "list", "value": []},
                "district": {"type": "list", "value": []},
                "complexOrBCenterAddress": {"type": "list", "value": []},
                "phone": {"type": "list", "value": []},
                "tags": {"type": "list", "value": []},
                "demand": {"type": "databox", "value": demand},
            }},
            "pageNum": {"type": "number", "value": page},
            "filterChanged": {"type": "boolean", "value": True},
            "external": {"type": "number", "value": 1},
        },
    }


def build_payload_get(apartment_id: int):
    return {"type":"databox","value":{"id":{"type":"number","value":apartment_id}}}