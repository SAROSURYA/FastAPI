from fastapi import FastAPI, Path, Depends, status, Response, HTTPException
import uvicorn
from user import UserReq, UpdateUser
from models import Base, user
from database import engine, SessionLocal
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()
  

@app.get("/")
def index():
  return {"res": "----Application Running----"}

#----------------------------------------------Create User----------------------------------------------------#

@app.post( 
    "/create-user", 
    status_code = status.HTTP_201_CREATED 
)
def create_new_user( 
  user_req: UserReq, 
  db: Session = Depends(get_db)
):
  
  new_user = user(
    first_name = user_req.first_name,
    last_name = user_req.last_name
  )

  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  
  return new_user

#----------------------------------------------Get All User----------------------------------------------------#

@app.get( 
  "/get-all-user",
  status_code = status.HTTP_200_OK
)
def get_all_user( 
  response: Response, 
  db: Session = Depends(get_db) 
):
  
  get_user = db.query(user).all() 

  if not get_user:
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"message": "No Data Found"}
  
  return get_user

#----------------------------------------------Get User By Id----------------------------------------------------#

@app.get( 
  "/get-user-by-id/{user_id}",
  status_code = status.HTTP_200_OK 
)
def get_user_by_id(
  response: Response, 
  user_id: int = Path(description="The ID of the user you want to view", gt=0), 
  db: Session = Depends(get_db)
):
  
  get_user = db.query(user).filter(user.id == user_id).first()
  
  if not get_user:
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"details": "User Not Found"}
  
  return get_user

#----------------------------------------------Get User By First Name----------------------------------------------------#

@app.get( 
  "/get-user-by-firstname/{first_name}",
  status_code = status.HTTP_200_OK 
)
def get_user_by_id(
  response: Response, 
  first_name: str = Path(description="The first name of the user you want to view"), 
  db: Session = Depends(get_db)
):
  
  get_user = db.query(user).filter(user.first_name == first_name).first()

  if not get_user:
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"details": "User Not Found"}
  
  return get_user

#----------------------------------------------Get User By Last Name----------------------------------------------------#

@app.get( "/get-user-by-lastname/{last_name}" )
def get_user_by_id(
  last_name: str = Path(description="The last name of the user you want to view"), 
  db: Session = Depends(get_db)
):
  
  get_user = db.query(user).filter(user.last_name == last_name).first()

  if not get_user:
    raise HTTPException(
      status_code = status.HTTP_404_NOT_FOUND,
      detail = "User Not Found"
    )
  
  return get_user

#----------------------------------------------Update User----------------------------------------------------#

@app.put(
  "/update-user/{user_id}",
  status_code = status.HTTP_202_ACCEPTED
)
def update_user(
  user_id: int, 
  user_req: UpdateUser,
  db: Session = Depends(get_db)
):

  update_user = db.query(user).filter(user.id == user_id)
  get_user = update_user.first()
  
  if not get_user:
    raise HTTPException(
      status_code = status.HTTP_404_NOT_FOUND,
      detail = "User Not Found"
    )
  
  if user_req.first_name is not None:
    get_user.first_name = user_req.first_name
  
  if user_req.last_name is not None:
    get_user.last_name = user_req.last_name

  db.commit()
  db.refresh(get_user)

  return {"detail": "Updated Successfully"}

#----------------------------------------------Delet User----------------------------------------------------#

@app.delete(
  "/delete-user/{user_id}",
  status_code = status.HTTP_204_NO_CONTENT
)
def delete_user(
  response: Response,
  user_id: int,
  db: Session = Depends(get_db)
):
  
  db.query(user).filter(user.id == user_id).delete(synchronize_session = False)
  db.commit()

  return {"details": "Successfully Deleted"}
    
if __name__ == "__main__":
  uvicorn.run(app, host = "127.0.0.1", port = 9000)