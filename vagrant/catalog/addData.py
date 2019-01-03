from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, CategoryItem, Base

engine = create_engine('sqlite:///category.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

category1 = Category(name="American Food")
session.add(category1)
session.commit()

category2 = Category(name="Italian Food")
session.add(category2)
session.commit()

category2 = Category(name="Saudi Food")
session.add(category2)
session.commit()

category2 = Category(name="Armani Food")
session.add(category2)
session.commit()

print("Items added successfully!")
