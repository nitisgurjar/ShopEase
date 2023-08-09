from tortoise.models import Model
from tortoise import Tortoise,fields


class Userr(Model):
    id=fields.IntField(pk=True)
    name=fields.CharField(100)
    email=fields.CharField(100)
    phone=fields.CharField(10)
    password=fields.CharField(100)
    shopname=fields.CharField(50)
    gst=fields.IntField()
    is_active = fields.BooleanField(default=True)
    last_login = fields.DatetimeField(auto_now_add=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class Category(Model):
    id=fields.IntField(pk=True)
    name=fields.CharField(200,unique=True)
    slug=fields.CharField(200)
    category_image=fields.TextField()
    description=fields.TextField()
    is_activate=fields.BooleanField(default=True)
    updated_at = fields.DatetimeField(auto_now=True)
    created_at = fields.DatetimeField(auto_now_add=True)



class SubCategoryy(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(200, unique=True)
    subcategory_image = fields.TextField()
    description = fields.TextField()
    category = fields.ForeignKeyField(
    "models.Category", related_name="subcategory", on_delete="CASCADE")
    is_active = fields.BooleanField(default=True)
    updated_at = fields.DatetimeField(auto_now=True)
    created_at = fields.DatetimeField(auto_now_add=True)


class AddBrand(Model):
    id=fields.IntField(pk=True)
    brand_name=fields.CharField(200,unique=True)
    is_active = fields.BooleanField(default=True)
    updated_at = fields.DatetimeField(auto_now=True)
    created_at = fields.DatetimeField(auto_now_add=True)


class Product(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(200, unique=True)
    manufacturer_sku = fields.CharField(30)
    product_image = fields.TextField()
    product_code = fields.IntField()
    model_no = fields.CharField(200)
    description = fields.TextField()
    mrp = fields.IntField()
    base_price = fields.IntField()
    gst = fields.IntField()
    offer_price = fields.IntField()
    category = fields.ForeignKeyField(
        "models.Category", related_name="category", on_delete="CASCADE")
    subcategory = fields.ForeignKeyField(
        "models.SubCategoryy", related_name="subcategory", on_delete="CASCADE")
    addbrand = fields.ForeignKeyField(
        "models.AddBrand", related_name="brand", on_delete="CASCADE")
    is_active = fields.BooleanField(default=True)
    updated_at = fields.DatetimeField(auto_now=True)
    created_at = fields.DatetimeField(auto_now_add=True)



Tortoise.init_models(['api.models'],'models')