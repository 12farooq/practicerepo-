from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# DATABASE_URL = "mysql+pymysql://root:@localhost/test"
DATABASE_URL = "mysql+pymysql://sanjeev:sanjeev-techpath@202.176.1.150/fast_api_ecom"
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
