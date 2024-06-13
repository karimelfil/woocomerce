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


class woocomerseuserIn(BaseModel):
    id : int
    consumer_key : str
    serect_key : str 
    active : bool

class woocomerseuserOut(BaseModel):
    id : int
    consumer_key : str
    serect_key : str 
    active : bool

class integrateIn(BaseModel):
    id : int
    type : str
    consumer_key : str
    serect_key : str 
    active : bool
    name: str
    description: str


class integrateOut(BaseModel):
    id : int
    type : str
    consumer_key : str
    serect_key : str 
    active : bool
    name: str
    description: str