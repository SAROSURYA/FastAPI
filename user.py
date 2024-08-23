from typing import Optional
from pydantic import BaseModel

class UserReq(BaseModel):
   first_name: str
   last_name: str
   password: str
   email: str

class UpdateUserReq(BaseModel):
   first_name: Optional[str] = None
   last_name: Optional[str] = None
   password: Optional[str] = None
   email: Optional[str] = None

class UserRes(UserReq):
   class Config():
      orm_mode = True
