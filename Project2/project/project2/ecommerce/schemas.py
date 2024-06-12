from pydantic import BaseModel

class CategoryIn(BaseModel):
    id : int
    name: str
    description : str 

class CategoryOut(BaseModel):
    id : int
    name: str
    description : str 

class TagIn(BaseModel):
    id : int
    name: str
    description : str 

class TagOut(BaseModel):
    id : int
    name: str
    description : str 

class ItemIn(BaseModel):
    id : int
    name: str
    description: str
    tag_id: int
    category_id:int
    weight : float
    brand : str

class ItemOut(BaseModel):
    id : int
    name: str
    description: str
    tag_id: int
    weight : float
    brand : str
    category_id: int