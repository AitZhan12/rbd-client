from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ApartmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    # source: str
    # source_id: int

    # object_type: int | None = None
    room_count: int | None = None
    area: float | None = None
    floor_num: int | None = None
    # floor_count: int | None = None
    # condition_text: str | None = None

    price: float | None = None
    # price_meter: float | None = None
    # currency: int | None = None
    # deal_type: int | None = None

    city: int | None = None
    address_name: str | None = None
    district_text: str | None = None

    # photo: list | None = None

    memo_public: str | None = None
    # memo_rewritten: str | None = None

    dt_create: datetime | None = None
    updated_at: datetime


class ApartmentListOut(BaseModel):
    total: int
    items: list[ApartmentOut]
