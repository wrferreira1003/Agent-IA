from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import getenv

# Recupera a URL do banco do .env
SQLALCHEMY_DATABASE_URL = getenv("DATABASE_URL")

# Cria o engine de conexão
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Cria sessão para acesso ao banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base que será usada para os models
Base = declarative_base()
