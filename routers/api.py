from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

import crud, models, schemas
from database import get_db
from services.ai_service import index_document, generate_feedback

router = APIRouter()

@router.post("/documents/", response_model=schemas.DocumentResponse)
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    text_content = content.decode("utf-8")
    
    # Save to DB
    doc_create = schemas.DocumentCreate(filename=file.filename, content=text_content)
    db_doc = crud.create_document(db=db, document=doc_create)
    
    # Index in FAISS
    index_document(text_content)
    
    return db_doc

@router.get("/documents/", response_model=List[schemas.DocumentResponse])
def read_documents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_documents(db, skip=skip, limit=limit)

@router.post("/drafts/", response_model=schemas.DraftResponse)
def create_draft(draft: schemas.DraftCreate, db: Session = Depends(get_db)):
    # Save draft
    db_draft = crud.create_draft(db=db, draft=draft)
    
    # Generate AI Feedback based on draft content
    ai_feedback_text = generate_feedback(draft.content)
    
    # Save Feedback
    feedback_create = schemas.FeedbackCreate(draft_id=db_draft.id, feedback_text=ai_feedback_text)
    crud.create_feedback(db=db, feedback=feedback_create)
    
    # Fetch draft again to include feedbacks relation
    return crud.get_draft(db, draft_id=db_draft.id)

@router.get("/drafts/{draft_id}", response_model=schemas.DraftResponse)
def read_draft(draft_id: int, db: Session = Depends(get_db)):
    db_draft = crud.get_draft(db, draft_id=draft_id)
    if db_draft is None:
        raise HTTPException(status_code=404, detail="Draft not found")
    return db_draft

@router.put("/drafts/{draft_id}", response_model=schemas.DraftResponse)
def update_draft(draft_id: int, draft: schemas.DraftUpdate, db: Session = Depends(get_db)):
    db_draft = crud.update_draft(db, draft_id=draft_id, draft_update=draft)
    if db_draft is None:
        raise HTTPException(status_code=404, detail="Draft not found")
    return db_draft
