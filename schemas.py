from pydantic import BaseModel,EmailStr, validator
from typing import Optional, List

# FOR CUSTOMER
def alphabetic_string(value: str) -> str:
    if not value.isalpha():
        raise ValueError("Must contain only alphabetic characters")
    return value




class CustomerBase(BaseModel):
    # first_name: constr(strip_whitespace=True, regex=r"^[A-Za-z]+$")  # Alphabetic characters only
    # last_name: constr(strip_whitespace=True, regex=r"^[A-Za-z]+$")  # Alphabetic characters only
    first_name: str = ...
    last_name: str = ...
    email: EmailStr
    password: str
    shipping_address: Optional[str] = None  # Make it optional with default None
    billing_address: Optional[str] = None  # Make it optional with default None

    @validator("password")
    def validate_password(cls, value):
        if not value.isalnum():
            raise ValueError("Must contain only alphanumeric characters")
        return value
    
    @validator("first_name", "last_name")
    def validate_last_name(cls, value):
        if not value.isalpha():
            raise ValueError("Must contain only alphabetic characters")
        return value
    
   
validate = {
        "first_name": (alphabetic_string, "alphabetic string"),
        "last_name": (alphabetic_string, "alphabetic string"),
    }    


class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass

class ResponseModel(BaseModel):
    message: str

class Customer(CustomerBase):
    customer_id: int


class CustomerLogin(BaseModel):
    email: str
    password: str

class CustomerLoginResponse(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    email: str
    token: str

class ErrorResponse(BaseModel):
    error: str

class LoginCredentials(BaseModel):
    email: str
    password: str    


class Customer(BaseModel):
    customer_id: int
    first_name: str
    last_name: str
    email: EmailStr


class CustomerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


# schema.py


class ProductBase(BaseModel):
    product_name: str
    description: str
    price: float
    stock_quantity: int
    image_url: str
    #category_id: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    product_id: int

class CategoryBase(BaseModel):
    category_name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    category_id: int
    products: List[Product] = []

class ResponseModel(BaseModel):
    message: str

















