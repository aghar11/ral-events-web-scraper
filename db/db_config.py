from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Replace with your actual PostgreSQL connection string
DATABASE_URL = "postgresql+psycopg2://eventsUser:event123@localhost:5433/RAL_EVENTS"

# Create engine
engine = create_engine(DATABASE_URL)

# Create a configured session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
