from sqlalchemy import Column, Integer, String
from model import BaseModel
from logs import LogRecord


# Модель для таблицы logs
class Log(BaseModel):
    __tablename__ = 'techlegal_logs'
    slice_tag = Column(String(25), nullable=False, index=True)
    tablename = Column(String(25), nullable=False)
    pages = Column(Integer, nullable=False)
    records = Column(Integer, nullable=False)

    @classmethod
    def from_pydantic(cls, pydantic_obj: LogRecord):
        return cls(
            slice_tag=pydantic_obj.slice_tag,
            tablename=pydantic_obj.tablename,
            pages=pydantic_obj.pages,
            records=pydantic_obj.records
        )
