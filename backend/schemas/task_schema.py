from pydantic import BaseModel, validator

class TaskCreate(BaseModel):
    title: str

    @validator("title")
    def validate_title(cls, v):
        if not v or not v.strip():
            raise ValueError("Title cannot be empty")
        return v