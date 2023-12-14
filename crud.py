from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from models import  Customer
from schemas import  CustomerLogin, CustomerLoginResponse, ErrorResponse, CustomerCreate, CustomerUpdate, ResponseModel
from datetime import datetime, timedelta
import jwt
import models
import schemas
from passlib.context import CryptContext
from passlib.hash import bcrypt


SECRET_KEY = "techapth"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# FOR CUSTOMER


# def create_customer(db: Session, customer: CustomerCreate):
#     hashed_password = pwd_context.hash(customer.password)
#     db_customer = Customer(**customer.dict(), password=hashed_password)
#     db.add(db_customer)
#     db.commit()
#     return ResponseModel(message="User registered successfully")


def create_customer(db: Session, customer: CustomerCreate):
    hashed_password = pwd_context.hash(customer.password)
    db_customer = Customer(
        first_name=customer.first_name,
        last_name=customer.last_name,
        email=customer.email,
        password=hashed_password,
        shipping_address=customer.shipping_address,
        billing_address=customer.billing_address
    )
    db.add(db_customer)
    db.commit()
    return ResponseModel(message="User registered successfully")



def get_user_by_email(db: Session, email: str):
    return db.query(Customer).filter(Customer.email == email).first()

def get_user_by_password(db: Session, password: str):
    return db.query(Customer).filter(Customer.password == password).first()


def get_customer(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.customer_id == customer_id).first()

# without token
# def customer_login(db: Session, login: CustomerLogin):
#     customer = db.query(Customer).filter(Customer.email == login.email).first()
#     if customer and customer.password == login.password:
#         return CustomerLoginResponse(
#             user_id=customer.customer_id,
#             first_name=customer.first_name,
#             last_name=customer.last_name,
#             email=customer.email,
#             token=" "  # Generate and return token here
#         )
#     else:
#         return ErrorResponse(error="Invalid credentials")
    

# with token

def customer_login(db: Session, login: CustomerLogin):
    customer = db.query(Customer).filter(Customer.email == login.email).first()
    if customer and pwd_context.verify(login.password, customer.password):
        token = create_access_token({"sub": customer.customer_id})
        # Update the customer's token in the database
        customer.token = token
        db.commit()
        return CustomerLoginResponse(
            user_id=customer.customer_id,
            first_name=customer.first_name,
            last_name=customer.last_name,
            email=customer.email,
            token=token
        )
    else:
        return ErrorResponse(error="Invalid credentials")

    
# fast api docs

# def update_customer(db: Session, customer_id: int, customer: CustomerUpdate):
#     db_customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
#     if db_customer:
#         for key, value in customer.dict().items():
#             setattr(db_customer, key, value)
#         db.commit()
#         db.refresh(db_customer)
#         return db_customer
#     return None



# def update_customer(db: Session, customer_id: int, customer: CustomerUpdate):
#     db_customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
#     if db_customer:
#         # Exclude email and password fields from the update
#         updated_data = customer.dict(exclude={"email", "password"})
        
#         for key, value in updated_data.items():
#             setattr(db_customer, key, value)
#         db.commit()
#         db.refresh(db_customer)
#         return db_customer
#     return None



# def update_customer(db: Session, customer_id: int, customer: CustomerUpdate):
#     db_customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
#     if db_customer:
#         updated_data = customer.dict()
        
#         for key, value in updated_data.items():
#             setattr(db_customer, key, value)
#         db.commit()
#         db.refresh(db_customer)
#         return db_customer
#     return None


# hased pasword update_database

def update_customer(db: Session, customer_id: int, customer: CustomerUpdate):
    db_customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if db_customer:
        # Check if password is being updated, and if so, hash it
        if "password" in customer.dict():
            hashed_password = pwd_context.hash(customer.password)
            setattr(db_customer, "password", hashed_password)

        updated_data = customer.dict(exclude={"password"})  # Exclude password from the update
        
        for key, value in updated_data.items():
            setattr(db_customer, key, value)
        db.commit()
        db.refresh(db_customer)
        return db_customer
    return None









def delete_customer(db: Session, customer_id: int):
    db_customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if db_customer:
        db.delete(db_customer)
        db.commit()
        return db_customer
    return None

# for token


def get_customer(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.customer_id == customer_id).first()

def get_customer_by_email(db: Session, email: str):
    return db.query(Customer).filter(Customer.email == email).first()


# def create_access_token(data: dict, expires_delta: timedelta):
#     expire = datetime.utcnow() + expires_delta
#     data_to_encode = data.copy()
#     data_to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# def authenticate_user(credentials: HTTPBasicCredentials = Depends()):
#     user = customer_login.get(credentials.username)
#     if user is None or user["password"] != credentials.password:
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     return credentials.username
# used_tokens = set()






# def create_access_token(data: dict):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


# This function creates an access token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.JWTError:
        return None
    

def get_current_user(token: str): 
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        return user_id
    except jwt.PyJWTError:
        return None



# FOR PRODUCT
def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()    
    return ResponseModel(message="Product registered successfully")

def get_products(db: Session):
    return db.query(models.Product).all()

def get_product_by_id(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.product_id == product_id).first()










