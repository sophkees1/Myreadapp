from typing import TypedDict, Optional, Tuple
from datetime import date
from enum import Enum


class StatusEnum(Enum):
    reading='reading'
    pending='pending'
    complete='complete'


class CreateDataType(TypedDict):
    username: str
    title: str
    description: Optional[str]  # either string or None
    status: StatusEnum
    pct_read: int
    start_read_date: Optional[date]
    end_read_date: Optional[date]


FetchByIdDataType = Tuple[str, str, StatusEnum, int, Optional[date], Optional[date]]