from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column as mc

from src.config.database import Base


class DataSource(Base):
    __tablename__ = "data_source"

    name: Mapped[str] = mc(String(100), unique=True)
    url: Mapped[str] = mc(unique=True)
