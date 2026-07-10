import asyncio
import logging

import requests
from requests import Session

from db.crud import change_deal
from filters import build_payload_get
from main import get_login, make_request


from config import settings


async def change_deal_to_sell(source_ids):
    session: Session = requests.Session()
    get_login(session)

    for _id in source_ids:
        payload = build_payload_get(_id)
        data = make_request(session, settings.GET_URL, payload=payload, method="POST")
        if not data:
            continue

        supply = data.get('supply', {})
        deal_type = 1 if supply.get('sell') else 2
        await change_deal(deal_type, _id)
        logging.info(f'{_id} saved.')


if '__main__' == __name__:
    logging.basicConfig(level=logging.INFO)
    asyncio.run(change_deal_to_sell([13703106]))
