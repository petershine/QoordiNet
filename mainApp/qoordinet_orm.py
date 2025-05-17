from datetime import date

from typing import List
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, Float, String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase


class QoordiNetBase(DeclarativeBase):
    pass


class QoordiNetActivities(QoordiNetBase):
    __tablename__ = "qoordinetActivities"
    id: Mapped[int] = mapped_column(primary_key=True)

    runDate: Mapped[Optional[date]]
    account: Mapped[Optional[str]]
    activityType: Mapped[Optional[str]]

    ticker: Mapped[Optional[str]]
    detail: Mapped[Optional[str]]
    note: Mapped[Optional[str]]

    premium: Mapped[Optional[float]]
    dividend: Mapped[Optional[float]]
    activityAmount: Mapped[Optional[float]]
    share: Mapped[Optional[float]]

    def __repr__(self) -> str:
        description = f"{self.__tablename__}(id={self.id!r}, runDate={self.runDate!r}, ticker={self.ticker!r}, detail={self.detail!r}, activityType={self.activityType!r}, note={self.note!r})"

        return description