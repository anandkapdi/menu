import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
Base = declarative_base()

class Restaurant(Base):
    __tablename__ = 'restaurant'
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)


class MenuItem(Base):
    __tablename__ = 'menu_item'
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
# print(session.query(Restaurant).all())
# items = session.query(MenuItem).all()
# for item in items:
#     print(item.name)


UrbanVeggieBurger = session.query(MenuItem).filter_by(id = 2).one()
# UrbanVeggieBurger2 = session.query(MenuItem).filter_by(restaurant_id = 8).one()
#
# print(UrbanVeggieBurger.price)
# print(UrbanVeggieBurger2.price)
UrbanVeggieBurger.price = "$2.99"
session.add(UrbanVeggieBurger)
session.commit()

veggieBurgers = session.query(MenuItem).filter_by(name= "Veggie Burger")

for veggieBurger in veggieBurgers:
    if veggieBurger.price != '$2.99':
        veggieBurger.price = '$2.99'
        session.add(veggieBurger)
        session.commit

# for veggieBurger in veggieBurgers:
#     print(veggieBurger.id)
#     print(veggieBurger.price)
#     print(veggieBurger.restaurant.name)
#     print("\n")

spinach = session.query(MenuItem).filter_by(name = 'Spinach Ice Cream').one()
session.delete(spinach)
session.commit()
spinach = session.query(MenuItem).filter_by(name = 'Spinach Ice Cream').one()
# print spinach.restaurant.name