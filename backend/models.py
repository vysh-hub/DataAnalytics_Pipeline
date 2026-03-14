from sqlalchemy import Column, Integer, String, Float
from database import Base

class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    rows = Column(Integer)
    columns = Column(Integer)
    missing_values = Column(Integer)