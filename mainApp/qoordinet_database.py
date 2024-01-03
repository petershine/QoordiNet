from .qoordinet_orm import *

from sqlalchemy import text, select
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import Table, Column, Integer, Float, String, Boolean


class QoordiNetSQLiteManager:
    def prepareEngine(self, sqlitePath: str, shouldEcho: bool = False):
        from sqlalchemy import create_engine
        self.engine = create_engine(sqlitePath, echo=shouldEcho)

        from .qoordinet_orm import QoordiNetBase
        QoordiNetBase.metadata.create_all(self.engine)

    