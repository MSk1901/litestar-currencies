from litestar.plugins.sqlalchemy import base
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column as mc


class Currency(base.UUIDAuditBase):
    __tablename__ = "currency"

    code: Mapped[str] = mc(String(10), unique=True)
    name: Mapped[str] = mc(String(100))
    symbol: Mapped[str] = mc(String(10), nullable=True)
