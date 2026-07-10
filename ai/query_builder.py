from sqlalchemy import select

from ai.landmarks import LANDMARKS
from models.apartment import Apartment


def build_query(params: dict):
    stmt = select(Apartment)
    if params.get("deal_type"):
        stmt = stmt.where(Apartment.deal_type == params["deal_type"])
    if params.get("rooms"):
        stmt = stmt.where(Apartment.room_count == params["rooms"])
    if params.get("floor_min"):
        stmt = stmt.where(Apartment.floor_num >= params["floor_min"])
    if params.get("floor_max"):
        stmt = stmt.where(Apartment.floor_num <= params["floor_max"])
    if params.get("price_min"):
        stmt = stmt.where(Apartment.price >= params["price_min"])
    if params.get("price_max"):
        stmt = stmt.where(Apartment.price <= params["price_max"])
    if params.get("area_min"):
        stmt = stmt.where(Apartment.area >= params["area_min"])
    if params.get("area_max"):
        stmt = stmt.where(Apartment.area <= params["area_max"])
    if params.get("good_condition"):
        stmt = stmt.where(Apartment.condition == 1)
    if params.get("landmark"):
        stmt = add_landmark_filter(stmt, params["landmark"])
        stmt = exclude_fake_coords(stmt)
    elif params.get("district"):
        stmt = stmt.where(Apartment.district_text.ilike(f"%{params['district']}%"))
    return stmt.order_by(Apartment.dt_create.desc()).limit(20)


FAKE_COORDS = [
    (69.586907, 42.315514),  # городская заглушка (1241 шт)
    (1, 1),                   # битые координаты (241 шт)
]

def exclude_fake_coords(stmt):
    for lon, lat in FAKE_COORDS:
        stmt = stmt.where(
            ~((Apartment.coord_x == lon) & (Apartment.coord_y == lat))
        )
    return stmt


def add_landmark_filter(stmt, landmark: str, radius_km: float = 2.0):
    coords = LANDMARKS.get(landmark.lower().strip())
    if not coords:
        return stmt
    lat, lon = coords
    lat_delta = radius_km / 111
    lon_delta = radius_km / 82
    return stmt.where(
        Apartment.coord_y.between(lat - lat_delta, lat + lat_delta),
        Apartment.coord_x.between(lon - lon_delta, lon + lon_delta),
    )