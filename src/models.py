from .database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, text


class File(Base):
    __tablename__ = "files"

    id = Column(Integer,primary_key=True,nullable=False)
    filename = Column(String,nullable=False)
    content = Column(String,nullable=False)
    partition = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))