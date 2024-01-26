from pydantic import BaseModel, Field


class FileBase(BaseModel):
    filename: str
    content: str
    partition: str

    class Config:
        orm_mode = True


class CreateFile(FileBase):
    class Config:
        orm_mode = True

class UploadItem(BaseModel):
    pages: list[str] = Field(default=[])
    should_filter: bool = Field(default=True)
    chunk_size: int = Field(default=0)