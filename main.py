import csv
import uvicorn 
from fastapi import FastAPI, Request, File, UploadFile, Depends,HTTPException
from fastapi.templating import Jinja2Templates # Jinja2-Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel, Field # Import your Pydantic Base model and Fields
import codecs 
import models # Import your SQLAlchemy models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import starlette.status as status


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

def get_db():
    try:
        # Creating a session.
        db = SessionLocal()
        yield db
    finally:
        # Closing the session.
        db.close()
        
class User(BaseModel):
    name: str = Field(max_length=25) # Represents the name of the user
    age: int = Field() # Represents the age of the user

def create_user(db: Session, user: User, data: dict):
    """Create user from provided data."""

    # Initialize user model with data
    user_model = models.Users(**data)

    # Add user model to database session
    db.add(user_model)

    # Commit changes to database
    db.commit()

    # Refresh user model with latest data from database
    db.refresh(user_model)


@app.get("/details")
def index(request: Request, db: Session = Depends(get_db)):
    # Retrieve all users from the database
    data = db.query(models.Users).all()
    # Return an HTML response with the retrieved data
    return templates.TemplateResponse("index.html", {"request": request, "data": data })

@app.post("/parse_csv", response_class=HTMLResponse)
async def upload(request: Request, file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Try parsing CSV
    try:
        csv_reader = csv.DictReader(codecs.iterdecode(file.file, 'utf-8'))

        # Create user for each row
        for rows in csv_reader:
            create_user(db=db, user=User(**rows), data=rows)
        
        # Close file
        file.file.close()
        
        # Redirect to details page
        return RedirectResponse(url="/details", status_code=status.HTTP_303_SEE_OTHER)
    
    # Handle exceptions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Function to render the form page    
@app.get("/", response_class=HTMLResponse)
def get_form(request:Request):
    return templates.TemplateResponse("form.html", {"request": request})
    
    
if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", reload=True )