from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Boolean, Date, ForeignKey, Index, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column as mc
from sqlalchemy.orm import relationship

from src.config.database import Base

if TYPE_CHECKING:
    from src.apps.currency.models import Currency
    from src.apps.datasource.models import DataSource


class CurrencyRate(Base):
    __tablename__ = "currency_rate"

    currency_id: Mapped[UUID] = mc(ForeignKey("currency.id"))
    date: Mapped[date] = mc(Date, nullable=False)
    value: Mapped[Decimal] = mc(Numeric(10, 2), nullable=False)
    base_currency_id: Mapped[UUID] = mc(ForeignKey("currency.id"))
    data_source_id: Mapped[UUID] = mc(ForeignKey("data_source.id"), nullable=True)
    is_actual: Mapped[bool] = mc(Boolean, default=False, nullable=False)

    base_currency: Mapped["Currency"] = relationship("Currency", foreign_keys=[base_currency_id])
    currency: Mapped["Currency"] = relationship("Currency", foreign_keys=[currency_id])
    data_source: Mapped["DataSource"] = relationship("DataSource")

    __table_args__ = (
        UniqueConstraint("currency_id", "date", "base_currency_id", name="uix_currency_date_base"),
        Index("ix_currency_rate_currency_date", "currency_id", "date"),
    )
