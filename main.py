from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import  Session
from models import User, BookLog
from mysql_workbench import SessionLocal
import firebase_admin
from firebase_admin import credentials, firestore
from schemas import Article

# Connecting to Mysql Workbench
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Connecting to Firebase database
cred = credentials.Certificate("D:\Evaluation\evaluation-a73ec-firebase-adminsdk-fbsvc-d5e6d7a4c2.json")
firebase_admin.initialize_app(cred)
db_firestore = firestore.client()

# Fetch user from mysql db using api-key
def get_user_from_api_key(api_key: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.api_key == api_key).first() 
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return user
    
# Logging all endpoint executions in database
def log(endpoint: str, method: str, status_code: int, user_id: int, db: Session = Depends(get_db)):
    new_log = BookLog(
        endpoint = endpoint,
        method = method,
        status_code = status_code,
        user_id = user_id
    ) #Creating a new log 
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return True

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

#Creating new article
@app.post("/articles", status_code=status.HTTP_201_CREATED)
def create_article(new_article: Article, user: User = Depends(get_user_from_api_key), db: Session = Depends(get_db)):
    #Check Role
    if user.role not in ["admin"]:
        log("/articles", "POST", 401, user.id, db)
        raise HTTPException(status_code=401, detail="Permission denied")
    
    #Write on Firebase Database
    new_doc = db_firestore.collection("articles").document()
    new_doc.set(new_article.model_dump())

    #Creating a log
    log("/articles", "POST", 201, user.id, db)
    return {"message": "Article created"}


#Updating existing article
@app.put("/articles/{article_id}", status_code=status.HTTP_200_OK)
def update_article(article_id: str, updated_article: Article, user: User = Depends(get_user_from_api_key), db: Session = Depends(get_db)):
    #Check Role
    if user.role not in ["admin", "editor"]:
        log(f"/articles/{article_id}", "PUT", 401, user.id, db)
        raise HTTPException(status_code=403, detail="Permission denied")
    
    #Fetch Article, if exists update
    document_ref = db_firestore.collection("articles").document(article_id)
    doc = document_ref.get()
    if not doc.exists:
        log(f"/articles/{article_id}", "PUT", 404, user.id, db)
        raise HTTPException(status_code=404, detail="Article not found")
    
    doc_dict = doc.to_dict()
    article_data = updated_article.model_dump()
    article_data["version"]  = doc_dict.get("version", 0) + 1
    document_ref.update(article_data)

    #Logging
    log(f"/articles/{article_id}", "PUT", 200, user.id, db)
    return {"article" : article_data}

#Fetching existing article
@app.get("/articles/{article_id}", status_code=status.HTTP_200_OK)
def get_article(article_id: str, user: User = Depends(get_user_from_api_key), db: Session = Depends(get_db)):
    #Check Role
    if user.role not in ["admin", "editor", "viewer"]:
        log(f"/articles/{article_id}", "GET", 401, user.id, db)
        raise HTTPException(status_code=403, detail="Permission denied")

    #Fetch article, If not exists raise 404 error
    document_ref = db_firestore.collection("articles").document(article_id)
    doc = document_ref.get()
    if not doc.exists:
        log(f"/articles/{article_id}", "GET", 404, user.id, db)
        raise HTTPException(status_code=404, detail="Article not found")
    
    log(f"/articles/{article_id}", "GET", 200, user.id, db)
    # Return the article as a dictionary 
    return {"article": doc.to_dict()}


#Deleting an article
@app.delete("/articles/{article_id}", status_code=status.HTTP_200_OK)
def delete_article(article_id: str, user: User = Depends(get_user_from_api_key), db: Session = Depends(get_db)):
    #Check Role
    if user.role not in ["admin"]:
        log(f"/articles/{article_id}", "DELETE", 401, user.id, db)
        raise HTTPException(status_code=403, detail="Permission denied")
    
    #Check if article exists
    document_ref = db_firestore.collection("articles").document(article_id)
    doc = document_ref.get()
    if not doc.exists:
        log(f"/articles/{article_id}", "DELETE", 404, user.id, db)
        raise HTTPException(status_code=404, detail="Article not found")
    
    #Perform Deletion and log changes
    document_ref.delete()
    log(f"/articles/{article_id}", "DELETE", 200, user.id, db)
    return {"message" : "Deletion Successful"}