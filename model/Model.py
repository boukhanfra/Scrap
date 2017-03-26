from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm  import sessionmaker
Base = declarative_base()

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    label = Column(String(150), nullable=False)

class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    label = Column(String(150), nullable=False)

class Offer(Base):
    __tablename__ = 'offer'
    id = Column(Integer, primary_key=True)
    link = Column(String(1024), nullable=False)
    title = Column(String(255), nullable=False)
    price = Column(Float, nullable=True)
    post_code = Column(String(5), nullable=True)
    description = Column(String(1024), nullable=True)
    city = relationship(City)
    city_id = Column(Integer, ForeignKey('city.id'))
    category = relationship(Category)
    category_id = Column(Integer, ForeignKey('category.id'))

class Image(Base):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    link = Column(String(1024), nullable=False)
    offer_id = Column(Integer, ForeignKey('offer.id'))
    offer = relationship(Offer)

engine = create_engine('mysql+pymysql://root:root@127.0.0.1:3306/leboncoin')
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)