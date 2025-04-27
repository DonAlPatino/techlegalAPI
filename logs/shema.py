from pydantic import BaseModel


class LogRecord(BaseModel):
    slice_tag: str
    tablename: str = ""
    pages: int = 0
    records: int = 0
    has_error: bool = False
