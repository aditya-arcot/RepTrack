from pydantic import BaseModel


class StoredFile(BaseModel):
    original_name: str
    size: int
    path: str
