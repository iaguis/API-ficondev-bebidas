# -*- coding: utf-8 -*-
from sqlalchemy import Table, MetaData, create_engine, Column, ForeignKey
from sqlalchemy.types import Integer, String, Float, DateTime, Boolean
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from config import SQL_PASS, SQL_USER
from datetime import datetime

_engine = create_engine('mysql+mysqldb://' + SQL_USER + ':' + SQL_PASS + '@localhost/bebidas', echo=True, pool_recycle=3600)

_Base = declarative_base(_engine)
_metadata = MetaData(bind=_engine)

class Distributor(_Base):
    __tablename__ = 'distributor'

    dist_id = Column(Integer, primary_key=True)
    name = Column(String(length=100))
    email = Column(String(length=255))
    password = Column(String(length=200))
    telephone = Column(String(length=15))
    session_id = Column(String(length=40))

    def __init__(self, name, email, password, telephone, session_id):
        self.name = name
        self.email = email
        self.password = password
        self.telephone = telephone
        self.session_id = session_id

    def __repr__(self):
        return "<Distributor('%s', '%s')>" % (self.name, self.email)

class Discount(_Base):
    __tablename__ = 'discounts'

    disc_id = Column(Integer, primary_key=True)
    minAumont = Column(Integer)
    disc_amount = Column(Float)

    def __init__(self, minAmount, disc_amount):
        self.minAmount = minAmount
        self.disc_amount = disc_amount

    def __repr__(self):
        return "<Discount('%s', '%d', '%d')>" % (self.product_id, self.minAmount, self.disc_amount)

class Order(_Base):
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    amount = Column(Integer)
    distributor_id = Column(Integer, ForeignKey('distributor.dist_id'))
    # change this when a lot of products
    product_id = Column(Integer, ForeignKey('products.product_id'))
    date_ready = Column(DateTime)
    date_ordered = Column(DateTime)

    distributor = relationship("Distributor", backref=backref('orders'))
    products = relationship("Product", backref=backref('orders'))

    def __init__(self, date, amount):
        self.date = date
        self.amount = amount
        self.date_ordered = datetime.utcnow()

    def __repr__(self):
        return "<Order('%d', '%s')>" % (self.order_id, self.amount)

class Product(_Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True)
    name = Column(String(length=255))
    description = Column(String(length=255))
    price = Column(Float)

    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price

    def __repr(self):
        return "<Product('%s')>" % (self.name)

#class Product_Order(_Base):
    #__tablename__ = 'product_order'

    #product_order_id = Column(Integer, primary_key=True)
    #product_id = Column(Integer, ForeignKey('products.product_id'))
    #order_id = Column(Integer, ForeignKey('orders.order_id'))
    #product = relationship("Product", backref=backref('orders'))
    #order = relationship("Order", backref=backref('products'))

def loadSession():
    Session = sessionmaker(bind=_engine)
    session = Session()
    return session
