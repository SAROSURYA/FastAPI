from typing import Optional
from pydantic import BaseModel

class UserReq(BaseModel):
   first_name: str
   last_name: str

class UpdateUser(BaseModel):
   first_name: Optional[str] = None
   last_name: Optional[str] = None