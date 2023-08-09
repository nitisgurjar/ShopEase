from pydantic import BaseModel


class User(BaseModel):
    name:str
    email:str
    phone:str
    password:str
    shopname:str
    gst:int
   

class Login(BaseModel):
    email : str
    password : str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class Info(BaseModel):
    id:int

class Update(BaseModel):
    id:int
    name:str
    email:str
    phone:str
    shopname:str
    gst:int

class categoryitem(BaseModel):
    name:str
    description:str


class Catupdate(BaseModel):
    id:int
    name:str
    description:str

class Subcategoryitem(BaseModel):
    category_id:int
    name:str
    description:str

class Branddetail(BaseModel):
    brand_name:str

class Updatebrand(BaseModel):
    id:int
    brand_name:str


class Productdetail(BaseModel):
    category_id:int
    subcategory_id:int
    addbrand_id:int
    name:str
    manufacturer_sku:str
    product_code:int
    model_n:str
    description :str
    mrp:int
    base_price :int
    gst :int
    offer_price:int


class UpdateProduct(BaseModel):
    id:int
    name:str
    manufacturer_sku:str
    product_code:int
    model_no:str
    description :str
    mrp:int
    base_price :int
    gst :int
    offer_price:int