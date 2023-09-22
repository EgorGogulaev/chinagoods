from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Index, Integer, ForeignKey, Text, VARCHAR
import psycopg2
import configparser



Base = declarative_base()
engine = create_engine("sqlite:///chinagoods.db")

class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, nullable=False)
    site_id = Column(VARCHAR(50))
    category = Column(VARCHAR(70))
    sub_category = Column(VARCHAR(70))
    name = Column(Text)
    price = Column(VARCHAR(50))
    description = Column(Text)
    patterns = Column(Text)
    colours = Column(Text)
    sort = Column(VARCHAR(50))
    place_of_origin = Column(VARCHAR(75))
    material = Column(VARCHAR(70))
    packing_qty = Column(VARCHAR(30))
    meas = Column(VARCHAR(30))
    cbm = Column(VARCHAR(30))
    gw = Column(VARCHAR(20))
    nw = Column(VARCHAR(20))

class Photo(Base):
    __tablename__ = "photo"

    id = Column(Integer, primary_key=True, nullable=False)

    photo = Column(Text)

    product = Column(Integer, ForeignKey('product.id', ondelete="CASCADE", onupdate="CASCADE"))

if __name__ == '__main__':
    Base.metadata.create_all(engine)