from .database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text


class File(Base):
    __tablename__ = "files"

    id = Column(Integer,primary_key=True,nullable=False)
    filename = Column(String,nullable=False)
    content = Column(String,nullable=False)
    partition = Column(Boolean, server_default='TRUE')
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))