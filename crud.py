from sqlalchemy.orm import Session
import models, schemas

def get_document(db: Session, document_id: int):
    return db.query(models.Document).filter(models.Document.id == document_id).first()

def get_documents(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Document).offset(skip).limit(limit).all()

def create_document(db: Session, document: schemas.DocumentCreate):
    db_document = models.Document(filename=document.filename, content=document.content)
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

def create_draft(db: Session, draft: schemas.DraftCreate):
    db_draft = models.Draft(title=draft.title, content=draft.content)
    db.add(db_draft)
    db.commit()
    db.refresh(db_draft)
    return db_draft

def get_draft(db: Session, draft_id: int):
    return db.query(models.Draft).filter(models.Draft.id == draft_id).first()

def update_draft(db: Session, draft_id: int, draft_update: schemas.DraftUpdate):
    db_draft = db.query(models.Draft).filter(models.Draft.id == draft_id).first()
    if db_draft:
        if draft_update.title is not None:
            db_draft.title = draft_update.title
        if draft_update.content is not None:
            db_draft.content = draft_update.content
        db.commit()
        db.refresh(db_draft)
    return db_draft

def create_feedback(db: Session, feedback: schemas.FeedbackCreate):
    db_feedback = models.Feedback(draft_id=feedback.draft_id, feedback_text=feedback.feedback_text)
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback
