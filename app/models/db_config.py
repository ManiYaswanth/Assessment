from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_URI = "postgresql://postgres:mani123@localhost:5432/demo_project"

engine = create_engine(SQLALCHEMY_URI, pool_size=20, max_overflow=0)

Session = sessionmaker(bind=engine)


def getSession():
    return Session()


if __name__ == "__main__":
    getSession()