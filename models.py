from sqlalchemy import Column, Integer, String
from database import Base

#Create User Model
class Users(Base):
    """Users table definition"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    """Primary key and auto incremented id"""
    name = Column(String)
    """Name of the user"""
    age = Column(Integer)
    """Age of the user in years"""
    