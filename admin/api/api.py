from fastapi import APIRouter,Request,status,Depends,Form,UploadFile,File
from . models import *
from . pydantic import User,Token,Login,Info,Update,categoryitem,Catupdate,Subcategoryitem,Branddetail,Updatebrand
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
from json import JSONEncoder
import typing
import passlib
from slugify import slugify
import os
from datetime import datetime,timedelta


app = APIRouter()
SECRET = b'your-secret-key'
manager = LoginManager(SECRET, token_url='/user_login')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



manager = LoginManager(SECRET, token_url='/login')

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


@app.post('/')
async def register(data:User):
    if await Userr.exists(phone=data.phone):
        return{"status":False,"message":"mobile number already exist"}
    elif await Userr.exists(email=data.email):
        return{"status":False,"message":"email already exist"}
    else:
        user_obj=await Userr.create(name=data.name,email=data.email,phone=data.phone,password=get_password_hash(data.password),shopname=data.shopname,
                                      gst=data.gst,)
        return user_obj
    

@app.get('/all/')
async def all():
    user_obj=await Userr.all()
    return user_obj


@app.post('/daata/')
async def daata(data:Info):
    user_obj = await Userr.filter(id=data.id)
    return user_obj


@app.delete('/delete/')
async def delete(data:Info):
    user_obj= await Userr.filter(id=data.id).delete()
    return {"message":"user deleted"}


@app.put('/update/')
async def update(data:Update):
    user_obj= await Userr.get(id=data.id)
    if not user_obj:
        return{"status":False,"message":"user not register"}
    else:
        user_obj=await Userr.filter(id=data.id).update(name=data.name,email=data.email,phone=data.phone,
                                                       shopname=data.shopname,gst=data.gst)
        return user_obj


@manager.user_loader() # type: ignore
async def load_user(email: str):
    if await Userr.exists(email=email):
        user = await Userr.get(email=email)
        return user

@app.post('/login/')
async def login(data: Login):
    email = data.email
    user = await load_user(email)
 
    if not user:
        return JSONResponse({'status': False, 'message': 'User not Registered'}, status_code=403)
    elif not verify_password(data.password, user.password):
        return JSONResponse({'status': False, 'message': 'Invalid password'}, status_code=403)
    access_token = manager.create_access_token(data={'sub': {'id': user.id}})
    new_dict = jsonable_encoder(user)
    new_dict.update({'access_token': access_token})
    return Token(access_token=access_token, token_type='bearer')


@app.post("/category/")
async def create_category(data: categoryitem = Depends(), category_image: UploadFile = File(...)):
    if await Category.exists(name=data.name):
        return {"status": False, "message": "categosy already Exista"}
        
    else:
        slug = slugify(data.name)
        # print(slug)
        FILEPATH = "static/images/category/"

        if not os.path.isdir(FILEPATH):
            os.makedirs(FILEPATH)

        filename = category_image.filename
        extension = filename.split(".")[1]
        imagename = filename.split(".")[0]

        if extension not in ["png", "jpg", "jpeg"]:
            return {"status": "error", "detials": "file Extension not allowed"}

        dt = datetime.now()
        dt_timestamp = round(datetime.timestamp(dt))

        modified_image_name = imagename+"-"+str(dt_timestamp)+"."+extension
        genrated_name = FILEPATH + modified_image_name
        file_content = await category_image.read()

        with open(genrated_name, "wb") as file:
            file.write(file_content)
            file.closed

        category_obj = await Category.create(
            category_image=genrated_name,
            description=data.description,
            name=data.name,
            slug=slug
        )

        return category_obj
    


@app.get('/category_all/')
async def category_all():
    cat_obj=await Category.filter(is_activate=True)
    return cat_obj


@app.post('/categoryy/')
async def category(data:Info):
    cat_obj = await Category.filter(id=data.id)
    return cat_obj


@app.delete('/cat_delete/')
async def cat_delete(data:Info):
    cat_obj= await Category.filter(id=data.id).delete()
    return {"message":" category deleted"}


@app.put('/category_update/')
async def update_category(data: Catupdate = Depends(), category_image: UploadFile = File(...)):
    cat_obj= await Category.get(id=data.id)
    if not cat_obj:
        return{"status":False,"message":"category doesnot exist"}
    else:
        cat_obj=await Category.filter(id=data.id).update(name=data.name,description=data.description)
        return cat_obj
    


@app.post("/subcategory/")
async def create_subcategory(data: Subcategoryitem = Depends(), subcategory_image: UploadFile = File(...)):
    if await Category.exists(id=data.category_id):
     category_obj=await Category.get(id=data.category_id)
     if await SubCategoryy.exists(name=data.name):
        return {"status": False, "message": "subcategosy already Exista"}
        
     else:
        slug = slugify(data.name)
        # print(slug)
        FILEPATH = "static/images/subcategory/"

        if not os.path.isdir(FILEPATH):
            os.makedirs(FILEPATH)

        filename = subcategory_image.filename
        extension = filename.split(".")[1]
        imagename = filename.split(".")[0]

        if extension not in ["png", "jpg", "jpeg"]:
            return {"status": "error", "detials": "file Extension not allowed"}

        dt = datetime.now()
        dt_timestamp = round(datetime.timestamp(dt))

        modified_image_name = imagename+"-"+str(dt_timestamp)+"."+extension
        genrated_name = FILEPATH + modified_image_name
        file_content = await subcategory_image.read()

        with open(genrated_name, "wb") as file:
            file.write(file_content)
            file.closed

        category_obj = await SubCategoryy.create(
            category=category_obj,
            subcategory_image=genrated_name,
            description=data.description,
            name=data.name,
            slug=slug
        )

        return category_obj
     


@app.get('/subcategory_all/')
async def subcategory_all():
    cat_obj=await SubCategoryy.filter(is_active=True)
    return cat_obj


@app.post('/subcategoryy/')
async def subcategory(data:Info):
    cat_obj = await SubCategoryy.filter(id=data.id)
    return cat_obj


@app.delete('/subcat_delete/')
async def subcat_delete(data:Info):
    cat_obj= await SubCategoryy.filter(id=data.id).delete()
    return {"message":" subcategory deleted"}


@app.put('/subcategory_update/')
async def update_subcategory(data: Catupdate = Depends(), category_image: UploadFile = File(...)):
    cat_obj= await SubCategoryy.get(id=data.id)
    if not cat_obj:
        return{"status":False,"message":"subcategory doesnot exist"}
    else:
        cat_obj=await SubCategoryy.filter(id=data.id).update(name=data.name,description=data.description)
        return cat_obj
    


@app.post('/addbrand/')
async def addbrand(data:Branddetail):
    if await AddBrand.exists(brand_name=data.brand_name):
        return{"status":False,"message":"brand already exist"}
    else:
        brand_obj=await AddBrand.create(brand_name=data.brand_name)
        return brand_obj
    

@app.get('/allbrand/')
async def all_brand():
    brand_obj=await AddBrand.all()
    return brand_obj


@app.post('/getbrand/')
async def get_brand(data:Info):
    brand_obj = await AddBrand.filter(id=data.id)
    return brand_obj


@app.delete('/branddelete/')
async def delete_brand(data:Info):
    brand_obj= await AddBrand.filter(id=data.id).delete()
    return {"message":"brand deleted"}


@app.put('/update_brand/')
async def update_brand(data:Updatebrand):
    brand_obj= await AddBrand.get(id=data.id)
    if not brand_obj:
        return{"status":False,"message":"brand not exist"}
    else:
        brand_obj=await AddBrand.filter(id=data.id).update(brand_name=data.brand_name)
        return brand_obj