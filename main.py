from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi import Header
import crud, schemas
from typing import List
from schemas import ResponseModel
from crud import verify_token, get_current_user
from database import SessionLocal, engine
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from passlib.hash import bcrypt
app = FastAPI()

# Create database tables
from models import Base
Base.metadata.create_all(bind=engine)

used_tokens = set()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#FOR CUSTOMERS

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# get profile with token verify token


# CORS ORIGIN HANDLING
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8081",
    "http://localhost:3000",
]

 

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

 




@app.get("/profile/",  response_model=schemas.Customer)
def protected_endpoint(db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):

    # Check if the token is in used_tokens set
    if token in used_tokens:
        raise HTTPException(status_code=401, detail="Access denied. Token has been used for logout.")

    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload["sub"]
    db_user = crud.get_customer(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return db_user

# @app.get("/profile/",  response_model=schemas.Customer)
# def protected_endpoint(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
#     # Check if the token is in used_tokens set
#     if token in used_tokens:
#         raise HTTPException(status_code=401, detail="Access denied. Token has been used for logout.")
    
#     payload = verify_token(token)
#     if payload is None:
#         raise HTTPException(status_code=401, detail="Invalid token")
    
#     user_id = payload["sub"]
#     db_user = crud.get_customer(db, user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     return db_user




# only authontication user update

# @app.put("/api/profile", response_model=schemas.ResponseModel)
# def update_profile(
#     updated_profile: schemas.CustomerUpdate,
#     db: Session = Depends(get_db),
#     token: str = Header()  # Use Header to get the token from the Authorization header
# ):
#     if token is None:
#         raise HTTPException(status_code=401, detail="Token not provided")
    
#     user_id = get_current_user(token)  # Get the user_id from the token
    
#     # Check if the user exists
#     db_user = crud.get_customer(db, user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     # Update the user's profile
#     updated_user = crud.update_customer(db, user_id, updated_profile)
#     if updated_user is None:
#         raise HTTPException(status_code=404, detail="Failed to update user profile")
    
#     return ResponseModel(message="Profile updated successfully")

# same above code again past in below


@app.put("/api/profile_update", response_model=schemas.ResponseModel)
def update_profile(
    updated_profile: schemas.CustomerUpdate,
    db: Session = Depends(get_db),
    token: str = Header()   # Use Header to get the token from the Authorization header
):
    if token in used_tokens:
        raise HTTPException(status_code=401, detail="Access denied. Token has been used for logout.")

    if not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")

    user_id = get_current_user(token[len("Bearer "):])  # Get the user_id from the token
    
    # Check if the user exists
    db_user = crud.get_customer(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update the user's profile
    updated_user = crud.update_customer(db, user_id, updated_profile)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="Failed to update user profile")
    
    return ResponseModel(message="Profile updated successfully")
 



@app.post("/login/", response_model=schemas.CustomerLoginResponse)
def customer_login(login: schemas.CustomerLogin, db: Session = Depends(get_db)):
    return crud.customer_login(db, login)

@app.post("/api/logout", response_model=schemas.ResponseModel)
def logout(token: str = Header(None)):
    if token is None:
        raise HTTPException(status_code=401, detail="Token not provided")    
    
    # Add the token to the used_tokens set
    used_tokens.add(token)
    
    return ResponseModel(message="Profile LOGOUT successfully")

 


# for fastapidocs

@app.post("/register/", response_model=schemas.ResponseModel)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    existing_user = crud.get_user_by_email(db, customer.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    existing_password = crud.get_user_by_password(db, customer.password)
    if existing_password:
        raise HTTPException(status_code=400, detail="Password already used")
    #db_user = crud.register_user(db, customer)
    db_user = crud.create_customer(db, customer)
    return db_user




# @app.get("/customers/{customer_id}", response_model=schemas.Customer)
# def read_customer(customer_id: int, db: Session = Depends(get_db)):
#     customer = crud.get_customer(db, customer_id)
#     if customer is None:
#         raise HTTPException(status_code=404, detail="Customer not found")
#     return customer

# @app.put("/customers/{customer_id}", response_model=schemas.Customer)
# def update_customer(customer_id: int, customer: schemas.CustomerUpdate, db: Session = Depends(get_db)):
#     updated_customer = crud.update_customer(db, customer_id, customer)
#     if updated_customer is None:
#         raise HTTPException(status_code=404, detail="Customer not found")
#     return updated_customer

# @app.delete("/customers/{customer_id}", response_model=schemas.Customer)
# def delete_customer(customer_id: int, db: Session = Depends(get_db)):
#     deleted_customer = crud.delete_customer(db, customer_id)
#     if deleted_customer is None:
#         raise HTTPException(status_code=404, detail="Customer not found")
#     return deleted_customer



# @app.get("/login")
# def login(username: str = Depends(authenticate_user)):
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     tokens = create_access_token({"sub": username}, access_token_expires)
#     return {"access_token": tokens, "token_type": "bearer"}

# @app.post("/logout")
# def logout(request: Request):
#     authorization_header = request.headers.get("Authorization")
#     if authorization_header is None or not authorization_header.startswith("Bearer "):
#         return "Invalid or missing token"
#     else:
#         encoded_token = authorization_header.replace("Bearer ", "")
#         used_tokens.add(encoded_token)
#         return {"Message":"Logout successful", "Token is going into used_tokens": used_tokens }

# @app.post("/verify_token")
# def verify_token(request: Request):
#     try:
#         authorization_header = request.headers.get("Authorization")
#         if authorization_header is None or not authorization_header.startswith("Bearer "):
#             raise HTTPException(status_code=401, detail="Invalid token or missing token")       
#         encoded_token = authorization_header.replace("Bearer ", "")
#         if encoded_token in used_tokens:
#             return "Session expired"
#         else:
#             decoded_token = jwt.decode(encoded_token, SECRET_KEY, algorithms=['HS256'])
#             expiration_time = datetime.utcfromtimestamp(decoded_token["exp"])
#             current_time = datetime.utcnow()
#             if current_time >= expiration_time:
#                 raise HTTPException(status_code=401, detail="Token time expired")
#             else:
#                 return {"Your token is valid": decoded_token}
#     except Exception as e:
#         return str(e)





# FOR PRODUCT
@app.post("/api/products", response_model=schemas.ResponseModel)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = crud.create_product(db, product)
    return db_product
    #return 

@app.get("/api/products", response_model=List[schemas.Product])
def retrieve_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    products = crud.get_products(db, skip, limit)
    return products

@app.get("/api/products/{product_id}", response_model=schemas.Product)
def retrieve_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product_by_id(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)



