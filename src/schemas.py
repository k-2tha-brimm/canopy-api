from pydantic import BaseModel


class FileBase(BaseModel):
    filename: str
    content: str
    partition: str

    class Config:
        orm_mode = True


class CreateFile(FileBase):
    class Config:
        orm_mode = True