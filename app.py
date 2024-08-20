from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel
import uvicorn

app = FastAPI()

students = {
  1: {
    "name": "sam",
    "age": 23,
    "year": "12 grade"
  }
}

class Student(BaseModel):
   name: str
   age: int
   year: str

class UpdateStudent(BaseModel):
   name: Optional[str] = None
   age: Optional[int] = None
   year: Optional[str] = None

@app.get("/")
def index():
  return {"res": "running"}

@app.get("/get-student/{student_id}")
def get_student(student_id: int = Path(description="The ID of the students you want to view", gt=0)):
    if student_id not in students:
      return {"res": "User Not Found"}
    
    return students[student_id]

@app.get("/get-by-name")
def get_students(*, name: Optional[str] = None, test: int):
  for student_id in students:
    if students[student_id]["name"] == name:
        return students[student_id]
  return {"res": "No Data Found"}

@app.post("/create-student/{student_id}")
def create_student(student_id: int, student: Student):
  if student_id in student:
    return {"res": "User Already Present"}
  
  students[student_id] = student
  return {"res": "Successfully Created"}

@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
  if student_id not in students:
    return {"res": "User Not Found"}
  
  if student.name != None:
    students[student_id].name = student.name
  
  if student.age != None:
    students[student_id].age = student.age

  if student.year != None:
    students[student_id].year = student.year

  return {"res": "Successfully Updated"}

@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
  if student_id not in students:
    return {"res": "User Not Found"}
  
  del students[student_id]
  return {"res": "Successfully Deleted"}
    
if __name__ == "__main__":
  uvicorn.run(app, host = "127.0.0.1", port = 9000)