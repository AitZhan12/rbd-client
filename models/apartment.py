from datetime import datetime
from sqlalchemy import String, Integer, Float, Boolean, DateTime, BigInteger, JSON
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.schema import UniqueConstraint

from models.base import Base


class Apartment(Base):
    __tablename__ = "apartments"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    source: Mapped[str] = mapped_column(String, nullable=False)
    source_id: Mapped[int] = mapped_column(BigInteger, nullable=False)

    object_type: Mapped[int | None] = mapped_column(Integer)
    room_count: Mapped[int | None] = mapped_column(Integer)
    area: Mapped[float | None] = mapped_column(Float)
    floor_num: Mapped[int | None] = mapped_column(Integer)
    floor_count: Mapped[int | None] = mapped_column(Integer)
    ceiling_height: Mapped[float | None] = mapped_column(Float)
    year_built: Mapped[int | None] = mapped_column(Integer)
    condition: Mapped[int | None] = mapped_column(Integer)
    condition_text: Mapped[str | None] = mapped_column(String)
    toilet_type: Mapped[int | None] = mapped_column(Integer)
    furniture_type: Mapped[int | None] = mapped_column(Integer)
    former_dorm: Mapped[bool | None] = mapped_column(Boolean)
    bail: Mapped[bool | None] = mapped_column(Boolean)

    price: Mapped[float | None] = mapped_column(Float)
    price_meter: Mapped[float | None] = mapped_column(Float)
    currency: Mapped[int | None] = mapped_column(Integer)
    deal_type: Mapped[int | None] = mapped_column(Integer)
    supply_source: Mapped[int | None] = mapped_column(Integer)
    flat_type: Mapped[int | None] = mapped_column(Integer)
    lease_price_period: Mapped[int | None] = mapped_column(Integer)

    city: Mapped[int | None] = mapped_column(Integer)
    address_id: Mapped[int | None] = mapped_column(Integer)
    address_name: Mapped[str | None] = mapped_column(String)
    district_id: Mapped[int | None] = mapped_column(Integer)
    district_text: Mapped[str | None] = mapped_column(String)
    house_num: Mapped[str | None] = mapped_column(String)
    intersection_name: Mapped[str | None] = mapped_column(String)
    coord_x: Mapped[float | None] = mapped_column(Float)
    coord_y: Mapped[float | None] = mapped_column(Float)
    geohash: Mapped[str | None] = mapped_column(String)

    photo: Mapped[list | None] = mapped_column(JSON)
    phone: Mapped[list | None] = mapped_column(JSON)

    krisha_id: Mapped[str | None] = mapped_column(String)
    load_source: Mapped[int | None] = mapped_column(Integer)

    memo_public: Mapped[str | None] = mapped_column(String)

    dt_create: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    dt_modify: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    scraped_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now, onupdate=datetime.now
    )

    __table_args__ = (
        UniqueConstraint("source", "source_id", name="uq_source_sourceid"),
    )