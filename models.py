from sqlalchemy import Column, Integer, String
from database import Base

class user(Base):
  __tablename__ = "user"
  
  id = Column(Integer, primary_key = True, index = True)
  first_name = Column(String)
  last_name = Column(String)