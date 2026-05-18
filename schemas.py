from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DocumentBase(BaseModel):
    filename: str
    content: str

class DocumentCreate(DocumentBase):
    pass

class DocumentResponse(DocumentBase):
    id: int
    uploaded_at: datetime

    class Config:
        from_attributes = True

class FeedbackBase(BaseModel):
    feedback_text: str

class FeedbackCreate(FeedbackBase):
    draft_id: int

class FeedbackResponse(FeedbackBase):
    id: int
    draft_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class DraftBase(BaseModel):
    title: str
    content: str

class DraftCreate(DraftBase):
    pass

class DraftUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class DraftResponse(DraftBase):
    id: int
    created_at: datetime
    updated_at: datetime
    feedbacks: List[FeedbackResponse] = []

    class Config:
        from_attributes = True
